import json
from langchain_anthropic import ChatAnthropic
from model import IntegratedPneumoniaSystem
import chainlit as cl
from PIL import Image
import base64
from io import BytesIO

# Initialize the IntegratedPneumoniaSystem
pneumonia_system = IntegratedPneumoniaSystem()

# Initialize Claude
llm = ChatAnthropic(
    model_name="claude-3-sonnet-20240229",  # or your preferred Claude model
    anthropic_api_key="anthropic_api_key"  # Replace with your actual key
)

def get_analysis_results(contents):
    if contents is None:
        return "No image data provided."
    
    try:
        # Decode and process the uploaded image
        content_type, content_string = contents.split(',')
        image_data = base64.b64decode(content_string)
        image = Image.open(BytesIO(image_data)).convert('L')  # Convert to grayscale if needed

        # Convert image to tensor for the model
        image_tensor = pneumonia_system.preprocess(image).unsqueeze(0)
        findings = pneumonia_system.predict_image(image_tensor)  # Assuming this returns a finding description
        return findings  # Return findings
    except Exception as e:
        return str(e)  # Return error message

def get_patient_history(image_name):
    with open('demo_dataset/clinical_dataset.json', 'r') as file:
        patient_data = json.load(file)
    
    for patient in patient_data:
        if patient['image_path'].split('\\')[-1].startswith(image_name):
            return patient
    
    return None

@cl.on_message
async def handle_message(message: cl.Message):
    try:
        prediction_data = message.content.strip()
        if not prediction_data:
            await cl.Message(content="Please provide valid image data for analysis.").send()
            return

        print (prediction_data)
        # Get analysis results
        findings = get_analysis_results(prediction_data)
        print(findings)
        if findings is None:
            await cl.Message(content="Error in analyzing the image. Please check the image format and try again.").send()
            return
        
        # Extract the image name from the prediction_data (assuming it contains this information)
        # image_name = prediction_data.split(',')[0]  # Adjust as needed to extract image name
        patient_history = get_patient_history(findings.get('image_path', ''))
        
        # Combine findings and patient history for the output
        combined_output = f"**Findings:** {findings}\n\n"
        if patient_history:
            combined_output += f"**Patient History:** {json.dumps(patient_history, indent=2)}"
        else:
            combined_output += "No patient history found."

        await cl.Message(content=combined_output).send()
        print(combined_output)
    except Exception as e:
        print(f"Error: {str(e)}")
        await cl.Message(content="An error occurred during analysis.").send()
