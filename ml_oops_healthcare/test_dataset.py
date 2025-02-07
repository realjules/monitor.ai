import os
import random
import shutil
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Dict, List, Tuple

class ChestXrayDataSampler:
    def __init__(self, source_dir: str, destination_dir: str = "demo_dataset", sample_size: int = 200):
        self.source_dir = Path(source_dir)
        self.destination_dir = Path(destination_dir)
        self.sample_size = sample_size
        self.test_dir = self.source_dir / 'test'
        
    def verify_dataset_structure(self) -> bool:
        """Verify the dataset directory structure and print status"""
        if not self.source_dir.exists():
            print(f"Error: Source directory '{self.source_dir}' does not exist")
            return False
            
        if not self.test_dir.exists():
            print(f"Error: Test directory '{self.test_dir}' does not exist")
            return False
            
        normal_dir = self.test_dir / 'NORMAL'
        pneumonia_dir = self.test_dir / 'PNEUMONIA'
        
        if not normal_dir.exists():
            print(f"Error: NORMAL directory '{normal_dir}' does not exist")
            return False
            
        if not pneumonia_dir.exists():
            print(f"Error: PNEUMONIA directory '{pneumonia_dir}' does not exist")
            return False
            
        # Count images
        normal_images = list(normal_dir.glob('*.jpeg')) + list(normal_dir.glob('*.jpg'))
        pneumonia_images = list(pneumonia_dir.glob('*.jpeg')) + list(pneumonia_dir.glob('*.jpg'))
        
        print("\nDataset Structure:")
        print(f"Source directory: {self.source_dir}")
        print(f"Normal images found: {len(normal_images)}")
        print(f"Pneumonia images found: {len(pneumonia_images)}")
        
        if len(normal_images) == 0 and len(pneumonia_images) == 0:
            print("Error: No images found in the dataset")
            return False
            
        return True
        
    def setup_directories(self):
        """Create destination directories"""
        os.makedirs(self.destination_dir, exist_ok=True)
        self.dest_normal = self.destination_dir / 'NORMAL'
        self.dest_pneumonia = self.destination_dir / 'PNEUMONIA'
        
        os.makedirs(self.dest_normal, exist_ok=True)
        os.makedirs(self.dest_pneumonia, exist_ok=True)
        
    def get_image_paths(self) -> Dict[str, List[Path]]:
        """Get paths of all images in test directory"""
        normal_dir = self.test_dir / 'NORMAL'
        pneumonia_dir = self.test_dir / 'PNEUMONIA'
        
        # Include both .jpeg and .jpg extensions
        normal_images = list(normal_dir.glob('*.jpeg')) + list(normal_dir.glob('*.jpg'))
        pneumonia_images = list(pneumonia_dir.glob('*.jpeg')) + list(pneumonia_dir.glob('*.jpg'))
        
        return {
            'NORMAL': normal_images,
            'PNEUMONIA': pneumonia_images
        }
        
    def sample_images(self, paths: Dict[str, List[Path]]) -> Dict[str, List[Path]]:
        """Randomly sample images maintaining class distribution"""
        total_normal = len(paths['NORMAL'])
        total_pneumonia = len(paths['PNEUMONIA'])
        total_images = total_normal + total_pneumonia
        
        if total_images == 0:
            raise ValueError("No images found in the dataset")
            
        # Calculate proportions
        normal_prop = total_normal / total_images
        
        # Calculate number of samples for each class
        normal_samples = min(int(self.sample_size * normal_prop), total_normal)
        pneumonia_samples = min(self.sample_size - normal_samples, total_pneumonia)
        
        # Adjust sample size if necessary
        if normal_samples + pneumonia_samples < self.sample_size:
            print(f"Warning: Could only find {normal_samples + pneumonia_samples} images")
            
        return {
            'NORMAL': random.sample(paths['NORMAL'], normal_samples),
            'PNEUMONIA': random.sample(paths['PNEUMONIA'], pneumonia_samples)
        }
        
    def copy_samples(self, sampled_paths: Dict[str, List[Path]]) -> Dict[str, int]:
        """Copy sampled images to destination directory"""
        counts = {'NORMAL': 0, 'PNEUMONIA': 0}
        
        for label, paths in sampled_paths.items():
            dest_dir = self.dest_normal if label == 'NORMAL' else self.dest_pneumonia
            
            for path in paths:
                try:
                    shutil.copy2(path, dest_dir / path.name)
                    counts[label] += 1
                except Exception as e:
                    print(f"Error copying {path}: {str(e)}")
                    
        return counts
        
    def analyze_distribution(self, counts: Dict[str, int]) -> pd.DataFrame:
        """Analyze class distribution"""
        total = sum(counts.values())
        distribution = {
            'Class': [],
            'Count': [],
            'Percentage': []
        }
        
        for label, count in counts.items():
            distribution['Class'].append(label)
            distribution['Count'].append(count)
            distribution['Percentage'].append(round(count/total * 100, 2))
            
        return pd.DataFrame(distribution)
        
    def plot_distribution(self, df: pd.DataFrame):
        """Plot class distribution"""
        plt.figure(figsize=(12, 5))
        
        # Bar plot
        plt.subplot(1, 2, 1)
        sns.barplot(x='Class', y='Count', data=df, palette='viridis')
        plt.title('Distribution of Classes')
        plt.ylabel('Number of Images')
        
        # Pie chart
        plt.subplot(1, 2, 2)
        plt.pie(df['Count'], labels=df['Class'], autopct='%1.1f%%',
                colors=sns.color_palette('viridis'))
        plt.title('Class Distribution (%)')
        
        plt.tight_layout()
        plt.savefig(self.destination_dir / 'distribution.png')
        plt.close()
        
    def process(self) -> pd.DataFrame:
        """Main processing function"""
        print("Verifying dataset structure...")
        if not self.verify_dataset_structure():
            raise ValueError("Invalid dataset structure")
            
        print("\nSetting up directories...")
        self.setup_directories()
        
        print("Getting image paths...")
        paths = self.get_image_paths()
        
        print(f"\nSampling {self.sample_size} images...")
        sampled_paths = self.sample_images(paths)
        
        print("Copying sampled images...")
        counts = self.copy_samples(sampled_paths)
        
        print("\nAnalyzing distribution...")
        distribution_df = self.analyze_distribution(counts)
        
        print("Creating visualizations...")
        self.plot_distribution(distribution_df)
        
        return distribution_df

def sample_chest_xray_dataset(source_dir: str, destination_dir: str = "demo_dataset", sample_size: int = 200):
    """Main function to sample and analyze the dataset"""
    try:
        sampler = ChestXrayDataSampler(source_dir, destination_dir, sample_size)
        distribution = sampler.process()
        
        print("\nSampling Complete!")
        print("\nDistribution Summary:")
        print(distribution.to_string(index=False))
        print(f"\nResults saved to: {destination_dir}")
        
        return distribution
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nPlease ensure your dataset follows this structure:")
        print("chest_xray/")
        print("├── test/")
        print("│   ├── NORMAL/")
        print("│   │   └── (normal images)")
        print("│   └── PNEUMONIA/")
        print("│       └── (pneumonia images)")
        return None

if __name__ == "__main__":
    # Get the current directory
    current_dir = Path.cwd()
    print(f"Current directory: {current_dir}")
    
    # Replace with your dataset path
    source_directory = ""  # or provide full path
    print(f"Looking for dataset in: {current_dir / source_directory}")
    
    distribution = sample_chest_xray_dataset(
        source_dir=source_directory,
        destination_dir="demo_dataset",
        sample_size=200
    )