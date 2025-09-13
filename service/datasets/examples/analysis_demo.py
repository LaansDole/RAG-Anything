#!/usr/bin/env python3
"""
Data analysis demonstrations for medical datasets.
Shows statistical analysis, visualization, and insights from the synthetic medical data.
"""

import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime, timedelta

def analyze_symptoms_data():
    """Analyze medical symptoms dataset."""
    
    print("🔬 Medical Symptoms Analysis")
    print("=" * 40)
    
    datasets_dir = os.path.join(os.path.dirname(__file__), '..')
    symptoms_path = os.path.join(datasets_dir, "medical_symptoms_small.xlsx")
    
    if not os.path.exists(symptoms_path):
        print("❌ Symptoms dataset not found. Run generate_datasets.py first.")
        return
    
    df = pd.read_excel(symptoms_path)
    
    print(f"📊 Dataset Overview:")
    print(f"   Total symptoms: {len(df)}")
    print(f"   Categories: {df['category'].nunique()}")
    print(f"   Urgency levels: {df['urgency_level'].nunique()}")
    
    print(f"\n📈 Category Distribution:")
    category_dist = df['category'].value_counts()
    for category, count in category_dist.items():
        percentage = (count / len(df)) * 100
        print(f"   {category}: {count} ({percentage:.1f}%)")
    
    print(f"\n🚨 Urgency Level Analysis:")
    urgency_dist = df['urgency_level'].value_counts()
    for urgency, count in urgency_dist.items():
        percentage = (count / len(df)) * 100
        print(f"   {urgency}: {count} ({percentage:.1f}%)")
    
    print(f"\n📊 Severity Analysis:")
    print(f"   Average severity: {df['severity'].mean():.1f}/10")
    print(f"   Median severity: {df['severity'].median():.1f}/10")
    print(f"   High severity (≥8): {len(df[df['severity'] >= 8])} symptoms")
    
    # Critical symptoms analysis
    critical_symptoms = df[df['urgency_level'] == 'Critical']
    if len(critical_symptoms) > 0:
        print(f"\n🚑 Critical Symptoms Analysis:")
        print(f"   Count: {len(critical_symptoms)}")
        print(f"   Average severity: {critical_symptoms['severity'].mean():.1f}/10")
        print(f"   Categories: {', '.join(critical_symptoms['category'].unique())}")

def analyze_patient_data():
    """Analyze patient records dataset."""
    
    print("\n\n👥 Patient Records Analysis")
    print("=" * 40)
    
    datasets_dir = os.path.join(os.path.dirname(__file__), '..')
    patients_path = os.path.join(datasets_dir, "patient_records_small.xlsx")
    
    if not os.path.exists(patients_path):
        print("❌ Patient dataset not found. Run generate_datasets.py first.")
        return
    
    df = pd.read_excel(patients_path)
    
    print(f"📊 Dataset Overview:")
    print(f"   Total patients: {len(df)}")
    print(f"   Conditions: {df['primary_condition'].nunique()}")
    print(f"   Age groups: {df['age_group'].nunique()}")
    
    print(f"\n📈 Age Group Distribution:")
    age_dist = df['age_group'].value_counts().sort_index()
    for age_group, count in age_dist.items():
        percentage = (count / len(df)) * 100
        print(f"   {age_group}: {count} ({percentage:.1f}%)")
    
    print(f"\n⚕️ Top Medical Conditions:")
    condition_dist = df['primary_condition'].value_counts().head(10)
    for condition, count in condition_dist.items():
        percentage = (count / len(df)) * 100
        print(f"   {condition}: {count} ({percentage:.1f}%)")
    
    print(f"\n🏥 Treatment Response Analysis:")
    response_dist = df['treatment_response'].value_counts()
    for response, count in response_dist.items():
        percentage = (count / len(df)) * 100
        print(f"   {response}: {count} ({percentage:.1f}%)")
    
    # Comorbidity analysis
    comorbidity_dist = df['comorbidities'].value_counts()
    no_comorbidities = comorbidity_dist.get('None', 0)
    with_comorbidities = len(df) - no_comorbidities
    
    print(f"\n🔗 Comorbidity Analysis:")
    print(f"   Patients with comorbidities: {with_comorbidities} ({(with_comorbidities/len(df))*100:.1f}%)")
    print(f"   Patients without comorbidities: {no_comorbidities} ({(no_comorbidities/len(df))*100:.1f}%)")
    
    # Risk score analysis
    print(f"\n⚠️ Risk Score Analysis:")
    print(f"   Average risk score: {df['risk_score'].mean():.1f}/100")
    print(f"   High risk (≥80): {len(df[df['risk_score'] >= 80])} patients")
    print(f"   Low risk (≤20): {len(df[df['risk_score'] <= 20])} patients")

def analyze_research_abstracts():
    """Analyze medical research abstracts dataset."""
    
    print("\n\n📚 Medical Research Abstracts Analysis")
    print("=" * 45)
    
    datasets_dir = os.path.join(os.path.dirname(__file__), '..')
    abstracts_path = os.path.join(datasets_dir, "medical_abstracts_medium.csv")
    
    if not os.path.exists(abstracts_path):
        print("❌ Abstracts dataset not found. Run generate_datasets.py first.")
        return
    
    # Load sample for analysis (to avoid memory issues)
    df = pd.read_csv(abstracts_path, nrows=1000)
    total_count = sum(1 for line in open(abstracts_path)) - 1
    
    print(f"📊 Dataset Overview:")
    print(f"   Total abstracts: {total_count:,}")
    print(f"   Sample analyzed: {len(df):,}")
    print(f"   Unique journals: {df['journal'].nunique()}")
    
    # Parse publication dates
    df['publication_date'] = pd.to_datetime(df['publication_date'])
    df['year'] = df['publication_date'].dt.year
    
    print(f"\n📅 Publication Timeline (Sample):")
    year_dist = df['year'].value_counts().sort_index().tail(5)
    for year, count in year_dist.items():
        print(f"   {year}: {count} publications")
    
    print(f"\n📖 Top Journals (Sample):")
    journal_dist = df['journal'].value_counts().head(5)
    for journal, count in journal_dist.items():
        percentage = (count / len(df)) * 100
        print(f"   {journal}: {count} ({percentage:.1f}%)")
    
    print(f"\n📊 Citation Impact Analysis (Sample):")
    print(f"   Average citations: {df['citation_count'].mean():.1f}")
    print(f"   Median citations: {df['citation_count'].median():.1f}")
    print(f"   Highly cited (≥100): {len(df[df['citation_count'] >= 100])} papers")
    
    # Abstract length analysis
    df['abstract_length'] = df['abstract'].str.len()
    print(f"\n📝 Abstract Length Analysis:")
    print(f"   Average length: {df['abstract_length'].mean():.0f} characters")
    print(f"   Median length: {df['abstract_length'].median():.0f} characters")
    
    # Common keywords analysis
    all_keywords = []
    for keywords_str in df['keywords'].dropna():
        keywords = [k.strip() for k in keywords_str.split(',')]
        all_keywords.extend(keywords)
    
    from collections import Counter
    keyword_counts = Counter(all_keywords)
    
    print(f"\n🏷️ Top Research Keywords (Sample):")
    for keyword, count in keyword_counts.most_common(10):
        print(f"   {keyword}: {count} mentions")

def analyze_clinical_trials():
    """Analyze clinical trials dataset."""
    
    print("\n\n🧪 Clinical Trials Analysis")
    print("=" * 35)
    
    datasets_dir = os.path.join(os.path.dirname(__file__), '..')
    trials_path = os.path.join(datasets_dir, "clinical_trials_medium.csv")
    
    if not os.path.exists(trials_path):
        print("❌ Clinical trials dataset not found. Run generate_datasets.py first.")
        return
    
    # Load sample for analysis
    df = pd.read_csv(trials_path, nrows=1000)
    total_count = sum(1 for line in open(trials_path)) - 1
    
    print(f"📊 Dataset Overview:")
    print(f"   Total trials: {total_count:,}")
    print(f"   Sample analyzed: {len(df):,}")
    print(f"   Unique conditions: {df['condition'].nunique()}")
    print(f"   Unique sponsors: {df['sponsor'].nunique()}")
    
    print(f"\n🧬 Trial Phase Distribution:")
    phase_dist = df['phase'].value_counts().sort_index()
    for phase, count in phase_dist.items():
        percentage = (count / len(df)) * 100
        print(f"   Phase {phase}: {count} ({percentage:.1f}%)")
    
    print(f"\n📊 Trial Status Distribution:")
    status_dist = df['status'].value_counts()
    for status, count in status_dist.items():
        percentage = (count / len(df)) * 100
        print(f"   {status}: {count} ({percentage:.1f}%)")
    
    print(f"\n🏥 Top Medical Conditions (Sample):")
    condition_dist = df['condition'].value_counts().head(10)
    for condition, count in condition_dist.items():
        percentage = (count / len(df)) * 100
        print(f"   {condition}: {count} ({percentage:.1f}%)")
    
    print(f"\n💼 Top Sponsors (Sample):")
    sponsor_dist = df['sponsor'].value_counts().head(5)
    for sponsor, count in sponsor_dist.items():
        percentage = (count / len(df)) * 100
        print(f"   {sponsor}: {count} ({percentage:.1f}%)")
    
    # Enrollment analysis
    print(f"\n👥 Enrollment Analysis:")
    print(f"   Average target enrollment: {df['enrollment_target'].mean():.0f} participants")
    print(f"   Median target enrollment: {df['enrollment_target'].median():.0f} participants")
    print(f"   Large trials (≥1000): {len(df[df['enrollment_target'] >= 1000])} trials")
    
    # Geographic distribution
    print(f"\n🌍 Geographic Distribution (Sample):")
    location_dist = df['location'].value_counts()
    for location, count in location_dist.items():
        percentage = (count / len(df)) * 100
        print(f"   {location}: {count} ({percentage:.1f}%)")

def cross_dataset_analysis():
    """Perform cross-dataset analysis and insights."""
    
    print("\n\n🔗 Cross-Dataset Insights")
    print("=" * 35)
    
    datasets_dir = os.path.join(os.path.dirname(__file__), '..')
    
    # Load all datasets
    datasets = {}
    
    try:
        datasets['symptoms'] = pd.read_excel(os.path.join(datasets_dir, "medical_symptoms_small.xlsx"))
        datasets['patients'] = pd.read_excel(os.path.join(datasets_dir, "patient_records_small.xlsx"))
        datasets['abstracts'] = pd.read_csv(os.path.join(datasets_dir, "medical_abstracts_medium.csv"), nrows=1000)
        datasets['trials'] = pd.read_csv(os.path.join(datasets_dir, "clinical_trials_medium.csv"), nrows=1000)
        
        print(f"📊 Dataset Size Comparison:")
        for name, df in datasets.items():
            size_mb = sys.getsizeof(df) / 1024 / 1024
            print(f"   {name.title()}: {len(df):,} records ({size_mb:.2f} MB in memory)")
        
        # Medical condition overlap analysis
        patient_conditions = set(datasets['patients']['primary_condition'].unique())
        trial_conditions = set(datasets['trials']['condition'].unique())
        
        common_conditions = patient_conditions.intersection(trial_conditions)
        
        print(f"\n⚕️ Condition Coverage Analysis:")
        print(f"   Patient conditions: {len(patient_conditions)}")
        print(f"   Trial conditions: {len(trial_conditions)}")
        print(f"   Overlapping conditions: {len(common_conditions)}")
        
        if common_conditions:
            print(f"   Common conditions: {', '.join(list(common_conditions)[:5])}")
        
        # Data completeness assessment
        print(f"\n✅ Data Quality Assessment:")
        for name, df in datasets.items():
            missing_percentage = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
            print(f"   {name.title()}: {missing_percentage:.1f}% missing data")
        
        # Research-to-practice pipeline simulation
        print(f"\n🔬 Research-to-Practice Pipeline Simulation:")
        
        # Find abstracts about diabetes
        diabetes_abstracts = datasets['abstracts'][
            datasets['abstracts']['keywords'].str.contains('diabetes', case=False, na=False)
        ]
        
        # Find diabetes trials
        diabetes_trials = datasets['trials'][
            datasets['trials']['condition'].str.contains('Diabetes', case=False, na=False)
        ]
        
        # Find diabetes patients
        diabetes_patients = datasets['patients'][
            datasets['patients']['primary_condition'].str.contains('Diabetes', case=False, na=False)
        ]
        
        print(f"   Diabetes research pipeline:")
        print(f"     📚 Research abstracts: {len(diabetes_abstracts)}")
        print(f"     🧪 Clinical trials: {len(diabetes_trials)}")
        print(f"     👥 Patient records: {len(diabetes_patients)}")
        
        if len(diabetes_patients) > 0:
            good_response = diabetes_patients[
                diabetes_patients['treatment_response'].isin(['Excellent', 'Good'])
            ]
            print(f"     ✅ Positive treatment outcomes: {len(good_response)}/{len(diabetes_patients)} ({(len(good_response)/len(diabetes_patients))*100:.1f}%)")
        
    except Exception as e:
        print(f"❌ Error in cross-dataset analysis: {e}")

def generate_insights_summary():
    """Generate high-level insights and recommendations."""
    
    print("\n\n💡 Key Insights & RAG Applications")
    print("=" * 45)
    
    insights = [
        {
            "category": "Clinical Decision Support",
            "insight": "Symptom urgency classification can be combined with patient history for triage automation",
            "rag_application": "Query: 'Patient with chest pain and diabetes - what is the urgency level and recommended protocols?'"
        },
        {
            "category": "Research Integration",
            "insight": "Cross-referencing research abstracts with ongoing trials reveals research-to-practice gaps",
            "rag_application": "Query: 'What recent research supports the clinical trials currently recruiting for heart disease?'"
        },
        {
            "category": "Personalized Medicine",
            "insight": "Patient demographics and treatment responses can inform personalized recommendations",
            "rag_application": "Query: 'For a 55-year-old female with hypertension and poor treatment response, what alternative approaches are available?'"
        },
        {
            "category": "Drug Development",
            "insight": "Clinical trial data can identify underserved conditions and successful intervention patterns",
            "rag_application": "Query: 'Which medical conditions have the most Phase III trials and what are the success rates?'"
        }
    ]
    
    for i, insight in enumerate(insights, 1):
        print(f"\n{i}. {insight['category']}:")
        print(f"   💡 {insight['insight']}")
        print(f"   🤖 {insight['rag_application']}")
    
    print(f"\n🚀 Next Steps for RAG Enhancement:")
    next_steps = [
        "Implement semantic search across all medical datasets",
        "Add entity extraction for medical terms and conditions",
        "Create cross-dataset relationship mapping",
        "Develop specialized medical prompts for different use cases",
        "Integrate with medical ontologies (SNOMED, ICD-10)",
        "Add temporal analysis for research trends and outcomes"
    ]
    
    for step in next_steps:
        print(f"   ✅ {step}")

def main():
    """Main analysis function."""
    
    print("📊 RAG-Anything Medical Dataset Analysis")
    print("=" * 50)
    print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        analyze_symptoms_data()
        analyze_patient_data()
        analyze_research_abstracts()
        analyze_clinical_trials()
        cross_dataset_analysis()
        generate_insights_summary()
        
        print(f"\n\n✅ Analysis Complete!")
        print(f"💾 Consider saving these insights for RAG system optimization")
        
    except Exception as e:
        print(f"\n❌ Analysis error: {e}")
        print(f"💡 Make sure all datasets are generated first: python service/datasets/generate_datasets.py")

if __name__ == "__main__":
    main()
