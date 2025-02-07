import torch
import torch.nn as nn
import torchvision.models as models
from typing import Dict, Any, List
import numpy as np
from PIL import Image
from torchvision import transforms
import json
from io import BytesIO


class IntegratedPneumoniaSystem:
    def __init__(self, clinical_data_path: str = "demo_dataset/clinical_dataset.json"):
        # Load models
        self.setup_models()
        # Initialize clinical data
        self.clinical_data = []
        # Load clinical data if available
        self.load_clinical_data(clinical_data_path)

    def load_clinical_data(self, clinical_data_path: str):
        """Load clinical data from JSON file"""
        try:
            with open(clinical_data_path, 'r') as f:
                self.clinical_data = json.load(f)
            print(f"Loaded clinical data for {len(self.clinical_data)} patients")
        except FileNotFoundError:
            print(f"Warning: Clinical data file not found at {clinical_data_path}")
        except json.JSONDecodeError:
            print(f"Warning: Error decoding clinical data JSON file")
        except Exception as e:
            print(f"Warning: Error loading clinical data: {str(e)}")

    def setup_models(self):
        """Setup both production and uncertainty models"""
        # Production model - modify first conv layer for grayscale
        self.production_model = models.densenet121(pretrained=True)
        # Modify first conv layer to accept 1 channel input
        self.production_model.features.conv0 = nn.Conv2d(1, 64, kernel_size=7, stride=2,
                                                        padding=3, bias=False)
        
        # Modify classifier for binary output
        num_features = self.production_model.classifier.in_features
        self.production_model.classifier = nn.Sequential(
            nn.Linear(num_features, 1),
            nn.Sigmoid()
        )
        
        # Uncertainty model - same modifications
        self.uncertainty_model = models.densenet121(pretrained=True)
        self.uncertainty_model.features.conv0 = nn.Conv2d(1, 64, kernel_size=7, stride=2,
                                                         padding=3, bias=False)
        self.uncertainty_model.classifier = nn.Sequential(
            nn.Dropout(p=0.3),
            nn.Linear(num_features, 1),
            nn.Sigmoid()
        )
        
        # Initialize weights for the modified conv layers
        nn.init.kaiming_normal_(self.production_model.features.conv0.weight)
        nn.init.kaiming_normal_(self.uncertainty_model.features.conv0.weight)
        
        try:
            weights = torch.load('densenet121-pneumonia.pth', weights_only=True)
            # Remove the conv0 weights from pretrained state dict as it's for 3 channels
            weights.pop('features.conv0.weight', None)
            # Load the rest of the weights
            self.production_model.load_state_dict(weights, strict=False)
            self.uncertainty_model.load_state_dict(weights, strict=False)
        except:
            print("Warning: Using initialized weights")
            
        self.production_model.eval()
        
        # Setup preprocessing
        self.preprocess = transforms.Compose([
            transforms.Resize(224),
            transforms.CenterCrop(224),
            transforms.Grayscale(num_output_channels=1),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485], std=[0.229])
        ])
        
    def analyze_case(self, image, patient_id: str = None) -> Dict[str, Any]:
        """
        Analyze a single case with both image and clinical data
        """
        # Get model predictions
        if isinstance(image, str):
            prediction_results = self.predict_image(image)
        elif isinstance(image, Image.Image):
            # Save the PIL Image temporarily for prediction
            temp_image_path = "temp_image.jpg"
            image.save(temp_image_path)
            prediction_results = self.predict_image(temp_image_path)
        else:
            raise ValueError("Invalid image type. Expected a file path or a PIL Image.")
        
        # Get clinical data if available
        clinical_info = self.get_clinical_info(patient_id) if patient_id else None
        
        # Combine results
        analysis = {
            'image_analysis': prediction_results,
            'clinical_data': clinical_info,
            'integrated_assessment': self.generate_integrated_assessment(
                prediction_results,
                clinical_info
            )
        }
        
        return analysis
    
    # def analyze_case(self, image_path: str, patient_id: str = None) -> Dict[str, Any]:
    #     """
    #     Analyze a single case with both image and clinical data
    #     """
    #     # Get model predictions
    #     prediction_results = self.predict_image(image_path)
        
    #     # Get clinical data if available
    #     clinical_info = self.get_clinical_info(patient_id) if patient_id else None
        
    #     # Combine results
    #     analysis = {
    #         'image_analysis': prediction_results,
    #         'clinical_data': clinical_info,
    #         'integrated_assessment': self.generate_integrated_assessment(
    #             prediction_results,
    #             clinical_info
    #         )
    #     }
        
    #     return analysis
        
    def predict_image(self, image_tensor, num_samples: int = 30) -> Dict[str, Any]:
        """Predict pneumonia probability with uncertainty"""
        try:
            # if isinstance(image, str):
            #     # If image is a file path, open it using PIL
            #     image = Image.open(image)
            # elif not isinstance(image, Image.Image):
            #     raise ValueError("Invalid image type. Expected a file path or a PIL Image.")

            # if image.mode != 'L':
            #     image = image.convert('L')
            # image_tensor = self.preprocess(image).unsqueeze(0)
            
            # Debug info
            # print(f"Input tensor shape: {image_tensor.shape}")
            # print(f"Input tensor range: [{image_tensor.min():.2f}, {image_tensor.max():.2f}]")
            
            # Get production model prediction
            with torch.no_grad():  # Disable gradient tracking
                official_pred = self.production_model(image_tensor)
                official_pred = official_pred.detach().cpu().numpy()  # Detach and convert to numpy
            
            # Get uncertainty predictions
            uncertainty_preds = []
            self.uncertainty_model.train()
            
            with torch.no_grad():  # Disable gradient tracking for uncertainty predictions
                for _ in range(num_samples):
                    pred = self.uncertainty_model(image_tensor)
                    uncertainty_preds.append(pred.detach().cpu().numpy())  # Detach and convert to numpy
                
            uncertainty_preds = np.stack(uncertainty_preds)
            
            # Calculate statistics
            mean_pred = np.mean(uncertainty_preds)
            std_dev = np.std(uncertainty_preds)
            conf_intervals = np.percentile(uncertainty_preds, [2.5, 97.5])
            
            return {
                'prediction': {
                    'pneumonia_probability': float(official_pred[0][0]),  # Access the single prediction value
                    'is_pneumonia': float(official_pred[0][0]) > 0.5
                },
                'uncertainty': {
                    'mean_probability': float(mean_pred),
                    'standard_deviation': float(std_dev),
                    'confidence_interval': {
                        'lower': float(conf_intervals[0]),
                        'upper': float(conf_intervals[1])
                    },
                    'high_confidence': float(std_dev) < 0.1
                }
            }
            
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            raise
        
    def get_clinical_info(self, patient_id: str) -> Dict[str, Any]:
        """Get clinical information for patient"""
        if not self.clinical_data:
            return None
            
        for case in self.clinical_data:
            if case['patient_id'] == patient_id:
                return case
        return None
        
    def generate_integrated_assessment(self, 
                                    prediction_results: Dict[str, Any],
                                    clinical_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate integrated assessment using both image and clinical data"""
        pred_prob = prediction_results['prediction']['pneumonia_probability']
        uncertainty = prediction_results['uncertainty']['standard_deviation']
        
        assessment = {
            'risk_level': self._calculate_risk_level(pred_prob, clinical_info),
            'confidence': self._assess_confidence(uncertainty, clinical_info),
            'recommendations': self._generate_recommendations(
                pred_prob,
                uncertainty,
                clinical_info
            )
        }
        
        return assessment
        
    def _calculate_risk_level(self, 
                            pred_prob: float, 
                            clinical_info: Dict[str, Any]) -> str:
        """Calculate risk level based on all available information"""
        if clinical_info:
            # Adjust risk based on clinical factors
            risk_factors = len(clinical_info.get('comorbidities', []))
            age = clinical_info.get('basic_info', {}).get('age', 50)
            
            # Increase risk for elderly or those with comorbidities
            risk_modifier = 0.1 * (risk_factors + (1 if age > 65 else 0))
            adjusted_prob = min(1.0, pred_prob + risk_modifier)
        else:
            adjusted_prob = pred_prob
            
        if adjusted_prob > 0.8:
            return "High"
        elif adjusted_prob > 0.5:
            return "Moderate"
        else:
            return "Low"
            
    def _assess_confidence(self, 
                          uncertainty: float, 
                          clinical_info: Dict[str, Any]) -> str:
        """Assess confidence in prediction"""
        if uncertainty > 0.2:
            return "Low"
        elif uncertainty > 0.1:
            return "Moderate"
        else:
            return "High"
            
    def _generate_recommendations(self,
                                pred_prob: float,
                                uncertainty: float,
                                clinical_info: Dict[str, Any]) -> List[str]:
        """Generate clinical recommendations"""
        recommendations = []
        
        # Basic recommendation based on prediction
        if pred_prob > 0.8:
            recommendations.append("Urgent clinical review recommended")
        elif pred_prob > 0.5:
            recommendations.append("Clinical review recommended")
        
        # Add uncertainty-based recommendations
        if uncertainty > 0.2:
            recommendations.append("Consider additional imaging due to high uncertainty")
            
        # Add clinical-based recommendations
        if clinical_info:
            if len(clinical_info.get('comorbidities', [])) > 0:
                recommendations.append("Monitor closely due to existing comorbidities")
            if clinical_info.get('basic_info', {}).get('age', 0) > 65:
                recommendations.append("Close monitoring advised due to age risk factor")
                
        return recommendations

def test_model(contents):
    """Test function to verify model and input pipeline"""
    system = IntegratedPneumoniaSystem()
    
    # Load and preprocess image
    image = Image.open(BytesIO(contents))
    if image.mode != 'L':
        image = image.convert('L')
    
    # Display image info
    print(f"\nImage Info:")
    print(f"Mode: {image.mode}")
    print(f"Size: {image.size}")
    
    # Preprocess and check tensor
    image_tensor = system.preprocess(image).unsqueeze(0)
    print(f"\nTensor Info:")
    print(f"Shape: {image_tensor.shape}")
    print(f"Range: [{image_tensor.min():.2f}, {image_tensor.max():.2f}]")
    
    try:
        # Try prediction
        result = system.predict_image(contents)
        print("\nPrediction successful!")
        print(f"Pneumonia probability: {result['prediction']['pneumonia_probability']:.2f}")
        return result
    except Exception as e:
        print(f"\nError during prediction: {str(e)}")
        return None

# if __name__ == "__main__":
#     # Test with a sample image
#     image_path = "demo_dataset/NORMAL/IM-0084-0001.jpeg"
#     result = test_model(image_path)
#     if result:
#         print("\nFull results:")
#         print(result)