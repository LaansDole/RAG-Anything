# Medical Datasets for RAG-Anything Service

This directory contains curated medical datasets for testing and demonstrating RAG-Anything's multimodal capabilities with healthcare data.

## 📋 Dataset Overview

### Small Excel Files (< 1MB)
Perfect for quick testing and prototype development:

1. **`medical_symptoms_small.xlsx`** - Medical symptom triage data
   - Size: ~500 rows
   - Format: Excel (.xlsx)
   - Source: Synthetic medical symptom classification
   - Use case: Symptom → diagnosis mapping, triage workflows

2. **`patient_records_small.xlsx`** - Anonymized patient summary data
   - Size: ~200 records
   - Format: Excel (.xlsx)
   - Source: Synthetic patient demographics and conditions
   - Use case: Patient information retrieval, clinical decision support

### Medium CSV Files (1-10MB)
Suitable for comprehensive testing and realistic demonstrations:

3. **`medical_abstracts_medium.csv`** - Medical research abstracts
   - Size: ~5,000 abstracts
   - Format: CSV
   - Source: PubMed-derived medical literature
   - Use case: Literature search, research assistance, knowledge discovery

4. **`clinical_trials_medium.csv`** - Clinical trials metadata
   - Size: ~10,000 trial records
   - Format: CSV
   - Source: Clinical trials registry data
   - Use case: Trial matching, research pipeline analysis

## 🚀 Quick Start

### Prerequisites
Ensure you have the required dependencies installed:

```bash
# Install pandas and openpyxl for Excel/CSV handling
uv add pandas openpyxl

# Optional: Install additional data processing libraries
uv add numpy matplotlib seaborn
```

### Loading Datasets

#### Excel Files
```python
import pandas as pd

# Load medical symptoms dataset
symptoms_df = pd.read_excel('service/datasets/medical_symptoms_small.xlsx')
print(f"Symptoms dataset: {len(symptoms_df)} rows")

# Load patient records dataset
patients_df = pd.read_excel('service/datasets/patient_records_small.xlsx')
print(f"Patient records: {len(patients_df)} rows")
```

#### CSV Files
```python
import pandas as pd

# Load medical abstracts dataset
abstracts_df = pd.read_csv('service/datasets/medical_abstracts_medium.csv')
print(f"Medical abstracts: {len(abstracts_df)} rows")

# Load clinical trials dataset
trials_df = pd.read_csv('service/datasets/clinical_trials_medium.csv')
print(f"Clinical trials: {len(trials_df)} rows")
```

### Integration with RAG-Anything

#### Processing CSV Data for RAG
```python
import asyncio
from raganything import RAGAnything, RAGAnythingConfig

async def process_medical_csv():
    # Initialize RAG-Anything
    config = RAGAnythingConfig(
        working_dir="./rag_storage_medical",
        enable_table_processing=True,
    )

    rag = RAGAnything(config=config, ...)

    # Load CSV as content list
    df = pd.read_csv('service/datasets/medical_abstracts_medium.csv')

    content_list = []
    for idx, row in df.iterrows():
        content_list.append({
            "type": "text",
            "text": f"Title: {row['title']}\nAbstract: {row['abstract']}",
            "page_idx": idx
        })

    # Insert into RAG system
    await rag.insert_content_list(
        content_list=content_list,
        file_path="medical_abstracts_medium.csv"
    )

    # Query the medical knowledge
    result = await rag.aquery(
        "What are the latest treatments for cardiovascular disease?",
        mode="hybrid"
    )
    return result
```

#### Processing Excel Data for RAG
```python
async def process_medical_excel():
    # Initialize RAG-Anything
    rag = RAGAnything(config=config, ...)

    # Load Excel as structured table
    df = pd.read_excel('service/datasets/medical_symptoms_small.xlsx')

    # Convert DataFrame to markdown table for better RAG processing
    table_markdown = df.to_markdown(index=False)

    content_list = [{
        "type": "table",
        "table_body": table_markdown,
        "table_caption": ["Medical Symptoms Classification Table"],
        "table_footnote": ["Source: Synthetic medical triage data"],
        "page_idx": 0
    }]

    # Insert structured table into RAG
    await rag.insert_content_list(
        content_list=content_list,
        file_path="medical_symptoms_small.xlsx"
    )

    # Query with table awareness
    result = await rag.aquery(
        "What symptoms are associated with respiratory conditions?",
        mode="hybrid"
    )
    return result
```

## 📊 Dataset Schemas

### Medical Symptoms (Excel)
```
Columns:
- symptom_id: Unique identifier
- symptom_name: Primary symptom description
- severity: Scale 1-10
- category: Body system (respiratory, cardiac, etc.)
- typical_age_range: Common age demographics
- urgency_level: Triage priority (low, medium, high, critical)
```

### Patient Records (Excel)
```
Columns:
- patient_id: Anonymized identifier
- age_group: Age bracket (20-30, 31-40, etc.)
- gender: M/F/Other
- primary_condition: Main diagnosis category
- comorbidities: Additional conditions
- treatment_response: Outcome category
```

### Medical Abstracts (CSV)
```
Columns:
- abstract_id: PubMed or unique ID
- title: Research paper title
- abstract: Full abstract text
- keywords: Medical subject headings
- publication_date: YYYY-MM-DD format
- journal: Publication venue
- doi: Digital object identifier
```

### Clinical Trials (CSV)
```
Columns:
- trial_id: Clinical trial registry number
- title: Official trial title
- condition: Target medical condition
- intervention: Treatment being tested
- phase: Trial phase (I, II, III, IV)
- status: Current status (recruiting, completed, etc.)
- start_date: Trial start date
- estimated_completion: Expected completion
- sponsor: Funding organization
```

## 🔍 Example Queries for RAG-Anything

### Medical Knowledge Retrieval
```python
# Symptom-based queries
await rag.aquery("What are the emergency symptoms that require immediate attention?")

# Treatment research queries
await rag.aquery("Find clinical trials for diabetes treatment in adults")

# Condition-specific queries
await rag.aquery("What are the latest research findings on cardiovascular disease prevention?")

# Cross-reference queries
await rag.aquery("Compare treatment outcomes for patients with multiple comorbidities")
```

### Multimodal Medical Queries
```python
# Table-enhanced queries
await rag.aquery_with_multimodal(
    "Analyze this symptom data in context of the medical literature",
    multimodal_content=[{
        "type": "table",
        "table_data": symptoms_df.head(10).to_csv(),
        "table_caption": "Patient symptom analysis"
    }]
)
```

## 📁 File Structure
```
service/datasets/
├── README.md                          # This documentation
├── medical_symptoms_small.xlsx        # Small Excel: Symptom triage data
├── patient_records_small.xlsx         # Small Excel: Patient summaries
├── medical_abstracts_medium.csv       # Medium CSV: Research abstracts
├── clinical_trials_medium.csv         # Medium CSV: Trial metadata
└── examples/                          # Usage examples
    ├── load_datasets.py              # Basic data loading
    ├── rag_integration.py             # RAG processing examples
    └── analysis_demo.py               # Data analysis demos
```

## ⚙️ Data Processing Best Practices

### Memory Management
- Load large CSV files in chunks: `pd.read_csv('file.csv', chunksize=1000)`
- Use efficient data types: `pd.read_csv('file.csv', dtype={'id': 'category'})`

### RAG Optimization
- **Text chunking**: Split long abstracts into paragraphs for better retrieval
- **Metadata preservation**: Keep publication dates, DOIs, trial phases as searchable metadata
- **Entity extraction**: Pre-process medical terms and conditions for enhanced searchability

### Privacy & Compliance
- All datasets use synthetic or publicly available data
- No personally identifiable information (PII) included
- Suitable for development, testing, and demonstration purposes
- For production use, ensure compliance with HIPAA, GDPR, and local regulations

## 🤝 Contributing

To add new medical datasets:

1. Ensure data is de-identified and publicly available
2. Follow the naming convention: `{domain}_{description}_{size}.{format}`
3. Update this README with dataset documentation
4. Add example usage code
5. Test integration with RAG-Anything workflows

## 📄 License & Attribution

- **Datasets**: Various open licenses (see individual dataset sources)
- **Synthetic data**: Generated for demonstration purposes
- **Real data**: Properly attributed with source citations
- **Usage**: Intended for research, development, and educational purposes

For production medical applications, consult with healthcare data experts and ensure regulatory compliance.
