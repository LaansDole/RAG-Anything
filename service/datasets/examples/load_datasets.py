#!/usr/bin/env python3
"""
Basic dataset loading examples for RAG-Anything medical datasets.
Demonstrates how to load and inspect the synthetic medical data.
"""

import pandas as pd
import os
import sys

def load_excel_datasets():
    """Load and display basic info about Excel datasets."""
    
    datasets_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    print("📊 Loading Excel Datasets")
    print("=" * 50)
    
    # Load medical symptoms dataset
    symptoms_path = os.path.join(datasets_dir, "medical_symptoms_small.xlsx")
    if os.path.exists(symptoms_path):
        symptoms_df = pd.read_excel(symptoms_path)
        print(f"\n🔬 Medical Symptoms Dataset:")
        print(f"   📁 File: medical_symptoms_small.xlsx")
        print(f"   📋 Rows: {len(symptoms_df)}")
        print(f"   📊 Columns: {len(symptoms_df.columns)}")
        print(f"   🏷️  Fields: {', '.join(symptoms_df.columns.tolist())}")
        
        print(f"\n📈 Sample Data:")
        print(symptoms_df.head(3).to_string())
        
        print(f"\n📊 Urgency Level Distribution:")
        print(symptoms_df['urgency_level'].value_counts().to_string())
    
    # Load patient records dataset
    patients_path = os.path.join(datasets_dir, "patient_records_small.xlsx")
    if os.path.exists(patients_path):
        patients_df = pd.read_excel(patients_path)
        print(f"\n\n👥 Patient Records Dataset:")
        print(f"   📁 File: patient_records_small.xlsx")
        print(f"   📋 Rows: {len(patients_df)}")
        print(f"   📊 Columns: {len(patients_df.columns)}")
        print(f"   🏷️  Fields: {', '.join(patients_df.columns.tolist())}")
        
        print(f"\n📈 Sample Data:")
        print(patients_df.head(3).to_string())
        
        print(f"\n📊 Primary Condition Distribution (Top 10):")
        print(patients_df['primary_condition'].value_counts().head(10).to_string())

def load_csv_datasets():
    """Load and display basic info about CSV datasets."""
    
    datasets_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    print("\n\n📚 Loading CSV Datasets")
    print("=" * 50)
    
    # Load medical abstracts dataset
    abstracts_path = os.path.join(datasets_dir, "medical_abstracts_medium.csv")
    if os.path.exists(abstracts_path):
        # Load just a sample to avoid memory issues
        abstracts_df = pd.read_csv(abstracts_path, nrows=1000)
        full_count = sum(1 for line in open(abstracts_path)) - 1  # Subtract header
        
        print(f"\n📚 Medical Abstracts Dataset:")
        print(f"   📁 File: medical_abstracts_medium.csv")
        print(f"   📋 Total Rows: {full_count}")
        print(f"   📊 Columns: {len(abstracts_df.columns)}")
        print(f"   🏷️  Fields: {', '.join(abstracts_df.columns.tolist())}")
        
        print(f"\n📈 Sample Data (showing first 2 records):")
        for idx, row in abstracts_df.head(2).iterrows():
            print(f"\n   Abstract {idx + 1}:")
            print(f"   Title: {row['title']}")
            print(f"   Journal: {row['journal']}")
            print(f"   Date: {row['publication_date']}")
            print(f"   Abstract: {row['abstract'][:200]}...")
    
    # Load clinical trials dataset
    trials_path = os.path.join(datasets_dir, "clinical_trials_medium.csv")
    if os.path.exists(trials_path):
        # Load just a sample to avoid memory issues
        trials_df = pd.read_csv(trials_path, nrows=1000)
        full_count = sum(1 for line in open(trials_path)) - 1  # Subtract header
        
        print(f"\n\n🧪 Clinical Trials Dataset:")
        print(f"   📁 File: clinical_trials_medium.csv")
        print(f"   📋 Total Rows: {full_count}")
        print(f"   📊 Columns: {len(trials_df.columns)}")
        print(f"   🏷️  Fields: {', '.join(trials_df.columns.tolist())}")
        
        print(f"\n📈 Sample Data (showing first 2 records):")
        for idx, row in trials_df.head(2).iterrows():
            print(f"\n   Trial {idx + 1}:")
            print(f"   ID: {row['trial_id']}")
            print(f"   Title: {row['title']}")
            print(f"   Condition: {row['condition']}")
            print(f"   Phase: {row['phase']}")
            print(f"   Status: {row['status']}")
        
        print(f"\n📊 Trial Phase Distribution:")
        print(trials_df['phase'].value_counts().to_string())
        
        print(f"\n📊 Trial Status Distribution:")
        print(trials_df['status'].value_counts().to_string())

def generate_summary():
    """Generate overall summary of all datasets."""
    
    datasets_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    print("\n\n📋 Dataset Summary")
    print("=" * 50)
    
    files = [
        ("medical_symptoms_small.xlsx", "Excel", "Small"),
        ("patient_records_small.xlsx", "Excel", "Small"),
        ("medical_abstracts_medium.csv", "CSV", "Medium"),
        ("clinical_trials_medium.csv", "CSV", "Medium")
    ]
    
    total_size = 0
    for filename, file_type, size_cat in files:
        filepath = os.path.join(datasets_dir, filename)
        if os.path.exists(filepath):
            file_size = os.path.getsize(filepath)
            total_size += file_size
            print(f"   📄 {filename}")
            print(f"      Type: {file_type} | Size: {size_cat} | {file_size / 1024 / 1024:.2f} MB")
    
    print(f"\n📊 Total Dataset Size: {total_size / 1024 / 1024:.2f} MB")
    print(f"🎯 Ready for RAG-Anything integration!")

def main():
    """Main function to run all examples."""
    
    print("🏥 RAG-Anything Medical Datasets - Loading Examples")
    print("=" * 60)
    
    try:
        load_excel_datasets()
        load_csv_datasets()
        generate_summary()
        
        print("\n\n✅ All datasets loaded successfully!")
        print("💡 Next steps:")
        print("   1. Run rag_integration.py to see RAG processing examples")
        print("   2. Run analysis_demo.py for data analysis examples")
        print("   3. Integrate with your RAG-Anything workflows")
        
    except Exception as e:
        print(f"\n❌ Error loading datasets: {e}")
        print("💡 Make sure you've generated the datasets first:")
        print("   python service/datasets/generate_datasets.py")

if __name__ == "__main__":
    main()
