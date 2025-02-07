from dash import Dash, html, dcc, Input, Output, State
from dash import dash_table
import plotly.express as px
from model import IntegratedPneumoniaSystem
from io import BytesIO
from PIL import Image
import base64

import json

from PIL import Image
import io

import os

# Initialize the IntegratedPneumoniaSystem
pneumonia_system = IntegratedPneumoniaSystem()

# Initialize Dash
external_scripts = [
    'http://localhost:8000/copilot/index.js'
]

app = Dash(__name__, external_scripts=external_scripts)

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H2('Analysis Results'),
            html.Div(id='analysis-content', className='analysis-section', style={
                'border': '1px solid #d6d6d6',
                'padding': '5px',
                'borderRadius': '5px',
                'backgroundColor': '#f9f9f9',
                'minHeight': '200px',
                'marginBottom': '20px'
            }),
            html.H2('Patient History'),
            html.Div(id='history-content', className='history-section', style={
                'border': '1px solid #d6d6d6',
                'padding': '10px',
                'borderRadius': '5px',
                'backgroundColor': '#f9f9f9',
                'minHeight': '200px'
            }),
        ], className='sidebar', style={'width': '25%', 'padding': '20px'}),

        html.Div([
            html.Div([
                dcc.Upload(
                    id='upload-image',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select X-Ray Image')
                    ]),
                    style={
                        'width': '300px',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    }
                ),
                html.Div('Supported formats: DICOM, PNG, JPEG', style={'color': 'gray'})
            ], className='top-bar'),

            html.Div(id='image-viewer', className='main-content', style={'padding': '20px'}),
        ], style={'width': '100%', 'padding': '20px'})
    ], style={'display': 'flex'})
])

@app.callback(
    [Output('analysis-content', 'children'), Output('history-content', 'children'), Output('image-viewer', 'children')],
    [Input('upload-image', 'contents')]
)

def get_analysis_results(contents):
    if contents is None:
        return html.Div("No image uploaded"), html.Div("No patient history available"), html.Div()

    try:
        # Decode the uploaded image contents
        content_type, content_string = contents.split(',')
        image_data = base64.b64decode(content_string)
        image = Image.open(BytesIO(image_data)).convert('L')  # Ensure grayscale if needed

        # Convert image to tensor for model
        image_tensor = pneumonia_system.preprocess(image).unsqueeze(0)
        result = pneumonia_system.predict_image(image_tensor)

        # Convert the image for displaying in Dash
        encoded_image = base64.b64encode(image_data).decode('utf-8')
        image_element = html.Img(src='data:image/png;base64,{}'.format(encoded_image), style={'width': '100%', 'height': 'auto'})

        # Get patient history
        patient_history = get_patient_history(result.get('image_path', ''))
        analysis_content = format_analysis_results(result)
        history_content = format_patient_history(patient_history)
        
        return analysis_content, history_content, image_element

    except Exception as e:
        print(f"Error processing image: {e}")
        return html.Div("Error processing image"), html.Div("Error fetching patient history"), html.Div()

def get_patient_history(image_name):
    with open('demo_dataset/clinical_dataset.json', 'r') as file:
        patient_data = json.load(file)
    
    for patient in patient_data:
        if patient['image_path'].split('\\')[-1].startswith(image_name):
            return patient
    
    return None

def format_patient_history(history):
    if history is None:
        return html.Div("No patient history available")
    
    return html.Div([
        html.H3(f"Patient ID: {history['patient_id']}"),
        html.P(f"Age: {history['basic_info']['age']}"),
        html.P(f"Gender: {history['basic_info']['gender']}"),
        html.H4("Vital Signs"),
        html.Ul([
            html.Li(f"Temperature: {history['vitals']['temperature']}°C"),
            html.Li(f"Heart Rate: {history['vitals']['heart_rate']} bpm"),
            html.Li(f"Respiratory Rate: {history['vitals']['respiratory_rate']} /min"),
            html.Li(f"Blood Pressure: {history['vitals']['blood_pressure']}"),
            html.Li(f"Oxygen Saturation: {history['vitals']['oxygen_saturation']}%")
        ]),
        html.H4("Symptoms"),
        html.Ul([html.Li(symptom) for symptom in history['symptoms']]),
        html.H4("Medications"),
        html.Ul([html.Li(f"{med['name']} - Dosage: {med['dosage']}, Frequency: {med['frequency']}") for med in history['medications']]),
        html.H4("Comorbidities"),
        html.Ul([html.Li(comorbidity) for comorbidity in history['comorbidities']]),
        html.H4("Diagnosis"),
        html.P(history['diagnosis']),
        html.H4("Note"),
        html.Pre(history['note_text'])
    ])

def format_analysis_results(results):
    return html.Div([
        html.H3('Analysis Results'),
        html.Ul([
            html.Li(f'Is It Pneumonia?: {results["prediction"]["is_pneumonia"]}'),
            html.Li(f'Standard Deviation: {results["uncertainty"]["standard_deviation"] * 100}'),
            html.Li(f'Mean Probability: {results["uncertainty"]["mean_probability"] * 100}'),
            html.Li(f'High Confidence: {results["uncertainty"]["high_confidence"]}')
        ])
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
