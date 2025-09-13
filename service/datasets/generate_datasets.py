#!/usr/bin/env python3
"""
Generate synthetic medical datasets for RAG-Anything service testing.
Creates both small Excel files and medium CSV files with realistic medical data.
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def create_medical_symptoms_excel():
    """Create small Excel file with medical symptoms data."""
    
    # Define symptom categories and data
    symptoms = [
        "Chest pain", "Shortness of breath", "Fever", "Headache", "Nausea", 
        "Dizziness", "Fatigue", "Cough", "Abdominal pain", "Back pain",
        "Joint pain", "Muscle weakness", "Skin rash", "Swelling", "Palpitations",
        "Blurred vision", "Difficulty swallowing", "Memory loss", "Confusion", "Tremor",
        "Numbness", "Tingling", "Weight loss", "Weight gain", "Loss of appetite",
        "Difficulty sleeping", "Excessive thirst", "Frequent urination", "Bruising", "Bleeding"
    ]
    
    categories = [
        "Cardiovascular", "Respiratory", "Neurological", "Gastrointestinal", 
        "Musculoskeletal", "Dermatological", "Endocrine", "Hematological",
        "Psychiatric", "Genitourinary"
    ]
    
    urgency_levels = ["Low", "Medium", "High", "Critical"]
    age_ranges = ["0-18", "19-35", "36-50", "51-65", "65+", "All ages"]
    
    data = []
    for i, symptom in enumerate(symptoms[:25]):  # Keep it small - 25 rows
        data.append({
            "symptom_id": f"SYM_{i+1:03d}",
            "symptom_name": symptom,
            "severity": random.randint(1, 10),
            "category": random.choice(categories),
            "typical_age_range": random.choice(age_ranges),
            "urgency_level": random.choice(urgency_levels),
            "description": f"Patient presents with {symptom.lower()}, commonly associated with {random.choice(categories).lower()} conditions.",
            "common_causes": f"May be caused by various {random.choice(categories).lower()} disorders or acute conditions."
        })
    
    df = pd.DataFrame(data)
    return df

def create_patient_records_excel():
    """Create small Excel file with anonymized patient records."""
    
    conditions = [
        "Hypertension", "Diabetes Type 2", "Asthma", "COPD", "Depression",
        "Anxiety", "Arthritis", "Migraine", "Sleep Apnea", "Gastritis",
        "Allergic Rhinitis", "Lower Back Pain", "Osteoporosis", "Anemia", "Insomnia"
    ]
    
    comorbidities = [
        "None", "Obesity", "High Cholesterol", "Kidney Disease", "Heart Disease",
        "Stroke History", "Cancer History", "Liver Disease", "Thyroid Disorder"
    ]
    
    treatment_responses = ["Excellent", "Good", "Fair", "Poor", "No Change"]
    age_groups = ["20-30", "31-40", "41-50", "51-60", "61-70", "71-80", "80+"]
    genders = ["M", "F", "Other"]
    
    data = []
    for i in range(200):  # 200 patient records
        data.append({
            "patient_id": f"PT_{i+1:05d}",
            "age_group": random.choice(age_groups),
            "gender": random.choice(genders),
            "primary_condition": random.choice(conditions),
            "comorbidities": random.choice(comorbidities),
            "treatment_response": random.choice(treatment_responses),
            "visit_count": random.randint(1, 12),
            "last_visit_date": (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d"),
            "risk_score": random.randint(1, 100),
            "care_plan": f"Standard care protocol for {random.choice(conditions)}"
        })
    
    df = pd.DataFrame(data)
    return df

def create_medical_abstracts_csv():
    """Create medium CSV file with medical research abstracts."""
    
    # Sample medical research topics and templates
    topics = [
        "cardiovascular disease", "diabetes management", "cancer treatment", "mental health",
        "infectious diseases", "neurology", "pediatrics", "geriatrics", "orthopedics",
        "dermatology", "ophthalmology", "immunology", "pharmacology", "radiology"
    ]
    
    journals = [
        "New England Journal of Medicine", "The Lancet", "JAMA", "BMJ", 
        "Nature Medicine", "Cell", "Science", "PLOS Medicine",
        "American Journal of Medicine", "Journal of Clinical Investigation"
    ]
    
    abstract_templates = [
        "Background: {topic} is a significant health concern. Objective: To evaluate {intervention}. Methods: We conducted a {study_type} involving {participants} patients. Results: {findings}. Conclusion: {conclusion}.",
        "Introduction: Recent advances in {topic} have shown promise. Methods: A {study_type} was performed with {participants} subjects. Results: Our findings demonstrate {findings}. Discussion: {conclusion}.",
        "Objective: To assess the efficacy of {intervention} in {topic}. Design: {study_type} with {participants} participants. Main outcomes: {findings}. Conclusions: {conclusion}."
    ]
    
    study_types = ["randomized controlled trial", "cohort study", "case-control study", "systematic review", "meta-analysis"]
    interventions = ["novel therapy", "drug treatment", "surgical intervention", "lifestyle modification", "diagnostic tool"]
    
    data = []
    for i in range(5000):  # 5000 abstracts for medium size
        topic = random.choice(topics)
        template = random.choice(abstract_templates)
        
        abstract = template.format(
            topic=topic,
            intervention=random.choice(interventions),
            study_type=random.choice(study_types),
            participants=random.randint(50, 10000),
            findings=f"significant improvement in {topic} outcomes with p<0.05",
            conclusion=f"The intervention shows promise for {topic} treatment"
        )
        
        # Generate realistic publication date (last 10 years)
        pub_date = datetime.now() - timedelta(days=random.randint(1, 3650))
        
        data.append({
            "abstract_id": f"PMID_{i+1000000}",
            "title": f"A {random.choice(study_types)} of {random.choice(interventions)} in {topic}",
            "abstract": abstract,
            "keywords": f"{topic}, {random.choice(interventions)}, clinical trial, medicine",
            "publication_date": pub_date.strftime("%Y-%m-%d"),
            "journal": random.choice(journals),
            "doi": f"10.{random.randint(1000, 9999)}/{random.randint(100000, 999999)}",
            "authors": f"Smith J, Johnson A, Brown M, et al.",
            "citation_count": random.randint(0, 500)
        })
    
    df = pd.DataFrame(data)
    return df

def create_clinical_trials_csv():
    """Create medium CSV file with clinical trials metadata."""
    
    conditions = [
        "Alzheimer's Disease", "Parkinson's Disease", "Multiple Sclerosis", "Diabetes Type 1",
        "Diabetes Type 2", "Hypertension", "Heart Failure", "Coronary Artery Disease",
        "Breast Cancer", "Lung Cancer", "Prostate Cancer", "Colorectal Cancer",
        "Depression", "Bipolar Disorder", "Schizophrenia", "ADHD", "Asthma", "COPD",
        "Rheumatoid Arthritis", "Osteoarthritis", "Lupus", "Psoriasis", "HIV/AIDS",
        "Hepatitis C", "Chronic Kidney Disease", "Obesity", "Sleep Apnea"
    ]
    
    interventions = [
        "Novel pharmaceutical compound", "Combination therapy", "Immunotherapy",
        "Gene therapy", "Stem cell therapy", "Behavioral intervention", 
        "Dietary supplement", "Medical device", "Surgical procedure", "Vaccine"
    ]
    
    phases = ["I", "II", "III", "IV"]
    statuses = ["Not yet recruiting", "Recruiting", "Active, not recruiting", "Completed", "Terminated", "Suspended"]
    sponsors = ["NIH", "Pfizer", "Novartis", "Roche", "Johnson & Johnson", "Merck", "GSK", "Academic Medical Center"]
    
    data = []
    for i in range(10000):  # 10,000 trials for medium size
        condition = random.choice(conditions)
        start_date = datetime.now() - timedelta(days=random.randint(1, 2555))  # Last 7 years
        duration = random.randint(180, 1825)  # 6 months to 5 years
        
        data.append({
            "trial_id": f"NCT{random.randint(10000000, 99999999)}",
            "title": f"A Phase {random.choice(phases)} Study of {random.choice(interventions)} in {condition}",
            "condition": condition,
            "intervention": random.choice(interventions),
            "phase": random.choice(phases),
            "status": random.choice(statuses),
            "start_date": start_date.strftime("%Y-%m-%d"),
            "estimated_completion": (start_date + timedelta(days=duration)).strftime("%Y-%m-%d"),
            "sponsor": random.choice(sponsors),
            "enrollment_target": random.randint(20, 5000),
            "primary_endpoint": f"Safety and efficacy of intervention in {condition}",
            "location": random.choice(["United States", "Europe", "Global", "Asia-Pacific"]),
            "inclusion_criteria": f"Adults aged 18-75 with confirmed {condition}",
            "exclusion_criteria": "Pregnancy, severe comorbidities, previous treatment failure"
        })
    
    df = pd.DataFrame(data)
    return df

def main():
    """Generate all medical datasets."""
    
    # Create datasets directory if it doesn't exist
    datasets_dir = "/Users/laansdole/Projects/RAG-Anything/service/datasets"
    os.makedirs(datasets_dir, exist_ok=True)
    
    print("🏥 Generating synthetic medical datasets...")
    
    # Generate small Excel files
    print("📊 Creating medical_symptoms_small.xlsx...")
    symptoms_df = create_medical_symptoms_excel()
    symptoms_df.to_excel(os.path.join(datasets_dir, "medical_symptoms_small.xlsx"), index=False)
    print(f"   ✅ Created with {len(symptoms_df)} symptom records")
    
    print("👥 Creating patient_records_small.xlsx...")
    patients_df = create_patient_records_excel()
    patients_df.to_excel(os.path.join(datasets_dir, "patient_records_small.xlsx"), index=False)
    print(f"   ✅ Created with {len(patients_df)} patient records")
    
    # Generate medium CSV files
    print("📚 Creating medical_abstracts_medium.csv...")
    abstracts_df = create_medical_abstracts_csv()
    abstracts_df.to_csv(os.path.join(datasets_dir, "medical_abstracts_medium.csv"), index=False)
    print(f"   ✅ Created with {len(abstracts_df)} research abstracts")
    
    print("🧪 Creating clinical_trials_medium.csv...")
    trials_df = create_clinical_trials_csv()
    trials_df.to_csv(os.path.join(datasets_dir, "clinical_trials_medium.csv"), index=False)
    print(f"   ✅ Created with {len(trials_df)} clinical trial records")
    
    # Print summary statistics
    print("\n📈 Dataset Summary:")
    print(f"   Small Excel files: 2 files (~{(len(symptoms_df) + len(patients_df))} total records)")
    print(f"   Medium CSV files: 2 files (~{(len(abstracts_df) + len(trials_df))} total records)")
    print("\n🎉 All medical datasets generated successfully!")
    print("📍 Files saved to: service/datasets/")

if __name__ == "__main__":
    main()
