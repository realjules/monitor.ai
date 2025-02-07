import random
import json
import pandas as pd
from datetime import datetime, timedelta
import os
from typing import Dict, List
from pathlib import Path

class ClinicalNotesGenerator:
    def __init__(self):
        # Common symptoms for pneumonia
        self.symptoms = {
            'respiratory': [
                'cough', 'dyspnea', 'chest pain', 'sputum production',
                'wheezing', 'tachypnea', 'shallow breathing'
            ],
            'systemic': [
                'fever', 'fatigue', 'chills', 'sweating', 'malaise',
                'muscle aches', 'decreased appetite'
            ]
        }
        
        # Common medications
        self.medications = {
            'antibiotics': [
                {'name': 'Amoxicillin', 'dosage': '500mg', 'frequency': 'three times daily'},
                {'name': 'Azithromycin', 'dosage': '500mg', 'frequency': 'once daily'},
                {'name': 'Ceftriaxone', 'dosage': '1g', 'frequency': 'daily'},
                {'name': 'Levofloxacin', 'dosage': '750mg', 'frequency': 'once daily'},
                {'name': 'Doxycycline', 'dosage': '100mg', 'frequency': 'twice daily'}
            ],
            'supportive': [
                {'name': 'Acetaminophen', 'dosage': '650mg', 'frequency': 'every 6 hours as needed'},
                {'name': 'Ibuprofen', 'dosage': '400mg', 'frequency': 'every 6 hours as needed'},
                {'name': 'Guaifenesin', 'dosage': '400mg', 'frequency': 'every 4 hours as needed'}
            ]
        }
        
        # Comorbidities
        self.comorbidities = [
            'Hypertension', 'Diabetes Type 2', 'COPD', 'Asthma', 
            'Coronary Artery Disease', 'Obesity', 'Chronic Kidney Disease'
        ]
        
        # Vital signs ranges
        self.vital_ranges = {
            'temperature': (37.5, 39.5),  # Celsius
            'heart_rate': (80, 120),
            'respiratory_rate': (20, 30),
            'blood_pressure_systolic': (110, 140),
            'blood_pressure_diastolic': (60, 90),
            'oxygen_saturation': (88, 95)
        }
        
    def generate_vitals(self) -> Dict:
        """Generate realistic vital signs"""
        return {
            'temperature': round(random.uniform(*self.vital_ranges['temperature']), 1),
            'heart_rate': round(random.uniform(*self.vital_ranges['heart_rate'])),
            'respiratory_rate': round(random.uniform(*self.vital_ranges['respiratory_rate'])),
            'blood_pressure': f"{round(random.uniform(*self.vital_ranges['blood_pressure_systolic']))}/{round(random.uniform(*self.vital_ranges['blood_pressure_diastolic']))}",
            'oxygen_saturation': round(random.uniform(*self.vital_ranges['oxygen_saturation']))
        }
        
    def generate_symptoms(self, is_pneumonia: bool) -> List[str]:
        """Generate symptom list based on condition"""
        num_respiratory = random.randint(3, 5) if is_pneumonia else random.randint(1, 3)
        num_systemic = random.randint(2, 4) if is_pneumonia else random.randint(1, 2)
        
        symptoms = (
            random.sample(self.symptoms['respiratory'], num_respiratory) +
            random.sample(self.symptoms['systemic'], num_systemic)
        )
        return symptoms
        
    def generate_medications(self, is_pneumonia: bool) -> List[Dict]:
        """Generate medication list"""
        medications = []
        
        if is_pneumonia:
            # Add 1-2 antibiotics
            medications.extend(random.sample(self.medications['antibiotics'], 
                                          random.randint(1, 2)))
                                          
        # Add 1-2 supportive medications
        medications.extend(random.sample(self.medications['supportive'], 
                                      random.randint(1, 2)))
        return medications
        
    def generate_clinical_note(self, patient_id: str, is_pneumonia: bool) -> Dict:
        """Generate complete clinical note"""
        # Generate basic patient data
        age = random.randint(20, 85)
        gender = random.choice(['Male', 'Female'])
        
        # Generate admission date
        admission_date = datetime.now() - timedelta(days=random.randint(1, 14))
        
        # Generate vitals
        vitals = self.generate_vitals()
        
        # Generate symptoms
        symptoms = self.generate_symptoms(is_pneumonia)
        
        # Generate medications
        medications = self.generate_medications(is_pneumonia)
        
        # Randomly assign comorbidities
        num_comorbidities = random.randint(0, 3)
        comorbidities = random.sample(self.comorbidities, num_comorbidities)
        
        # Generate clinical note text
        note_text = self.format_clinical_note(
            patient_id=patient_id,
            age=age,
            gender=gender,
            admission_date=admission_date,
            vitals=vitals,
            symptoms=symptoms,
            medications=medications,
            comorbidities=comorbidities,
            is_pneumonia=is_pneumonia
        )
        
        return {
            'patient_id': patient_id,
            'basic_info': {
                'age': age,
                'gender': gender,
                'admission_date': admission_date.strftime('%Y-%m-%d')
            },
            'vitals': vitals,
            'symptoms': symptoms,
            'medications': medications,
            'comorbidities': comorbidities,
            'diagnosis': 'Pneumonia' if is_pneumonia else 'Normal',
            'note_text': note_text
        }
        
    def format_clinical_note(self, **kwargs) -> str:
        """Format clinical note in standard medical format"""
        note_template = """
CLINICAL NOTE
============
Patient ID: {patient_id}
Date: {admission_date}

PATIENT INFORMATION
------------------
Age: {age}
Gender: {gender}
Admission Date: {admission_date}

VITAL SIGNS
----------
Temperature: {temp}°C
Heart Rate: {hr} bpm
Respiratory Rate: {rr} /min
Blood Pressure: {bp} mmHg
O2 Saturation: {o2}%

PRESENTING SYMPTOMS
-----------------
{symptoms}

MEDICAL HISTORY
-------------
Comorbidities: {comorbidities}

MEDICATIONS
----------
{medications}

ASSESSMENT
---------
{assessment}

PLAN
----
{plan}
"""
        
        # Format symptoms
        symptoms_text = "\n".join([f"- {s}" for s in kwargs['symptoms']])
        
        # Format medications
        medications_text = "\n".join([
            f"- {med['name']} {med['dosage']} {med['frequency']}"
            for med in kwargs['medications']
        ])
        
        # Format comorbidities
        comorbidities_text = "None" if not kwargs['comorbidities'] else \
                            ", ".join(kwargs['comorbidities'])
        
        # Generate assessment and plan
        if kwargs['is_pneumonia']:
            assessment = "Patient presents with clinical and radiological findings consistent with pneumonia."
            plan = """1. Continue current antibiotic regimen
2. Monitor vital signs and oxygen saturation
3. Encourage deep breathing exercises
4. Follow-up chest X-ray in 2 weeks
5. Return if symptoms worsen"""
        else:
            assessment = "Chest X-ray shows no active pulmonary disease."
            plan = """1. Symptomatic treatment as needed
2. Return if symptoms worsen
3. Regular health maintenance"""
            
        return note_template.format(
            patient_id=kwargs['patient_id'],
            age=kwargs['age'],
            gender=kwargs['gender'],
            admission_date=kwargs['admission_date'].strftime('%Y-%m-%d'),
            temp=kwargs['vitals']['temperature'],
            hr=kwargs['vitals']['heart_rate'],
            rr=kwargs['vitals']['respiratory_rate'],
            bp=kwargs['vitals']['blood_pressure'],
            o2=kwargs['vitals']['oxygen_saturation'],
            symptoms=symptoms_text,
            comorbidities=comorbidities_text,
            medications=medications_text,
            assessment=assessment,
            plan=plan
        )

def generate_clinical_dataset(image_dir: str, output_dir: str):
    """Generate clinical notes for all images in directory"""
    generator = ClinicalNotesGenerator()
    
    # Create output directories
    notes_dir = Path(output_dir) / 'clinical_notes'
    os.makedirs(notes_dir, exist_ok=True)
    
    # Process each category
    all_notes = []
    for category in ['NORMAL', 'PNEUMONIA']:
        category_dir = Path(image_dir) / category
        if category_dir.exists():
            for img_path in category_dir.glob('*.*'):
                patient_id = f"P{len(all_notes):04d}"
                
                # Generate note
                note = generator.generate_clinical_note(
                    patient_id=patient_id,
                    is_pneumonia=(category == 'PNEUMONIA')
                )
                
                # Save individual note
                note_path = notes_dir / f"{patient_id}_clinical_note.txt"
                with open(note_path, 'w') as f:
                    f.write(note['note_text'])
                    
                # Add to collection
                note['image_path'] = str(img_path)
                all_notes.append(note)
                
    # Save complete dataset
    dataset = pd.DataFrame(all_notes)
    dataset.to_csv(Path(output_dir) / 'clinical_dataset.csv', index=False)
    
    # Save as JSON for easy access
    with open(Path(output_dir) / 'clinical_dataset.json', 'w') as f:
        json.dump(all_notes, f, indent=2, default=str)
        
    return dataset

if __name__ == "__main__":
    # Generate clinical notes for the demo dataset
    dataset = generate_clinical_dataset(
        image_dir="demo_dataset",
        output_dir="demo_dataset"
    )
    
    print("\nClinical Dataset Generated:")
    print(f"Total cases: {len(dataset)}")
    print(f"Pneumonia cases: {len(dataset[dataset['diagnosis'] == 'Pneumonia'])}")
    print(f"Normal cases: {len(dataset[dataset['diagnosis'] == 'Normal'])}")