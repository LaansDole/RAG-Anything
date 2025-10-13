#!/usr/bin/env python3
"""
RAG integration examples for medical datasets.
Shows how to process medical data with RAG-Anything and query medical knowledge.
"""

import asyncio
import pandas as pd
import os
import sys

# Add the parent directory to Python path to import raganything
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


async def process_medical_excel_demo():
    """Demo: Process Excel medical data with RAG-Anything."""

    print("📊 Excel Dataset RAG Processing Demo")
    print("=" * 50)

    # This is a demo - in real usage, you'd have your API keys and models configured
    print("🔧 Setup Requirements:")
    print("   1. Configure your LLM API keys (OpenAI, LM Studio, etc.)")
    print("   2. Set up RAG-Anything with vision and embedding functions")
    print("   3. Initialize working directory for RAG storage")

    # Simulated RAG processing workflow
    datasets_dir = os.path.join(os.path.dirname(__file__), "..")

    # Load symptoms data
    symptoms_path = os.path.join(datasets_dir, "medical_symptoms_small.xlsx")
    symptoms_df = pd.read_excel(symptoms_path)

    print("\n📋 Processing medical_symptoms_small.xlsx...")
    print(f"   📊 Records: {len(symptoms_df)}")

    # Convert to content list format for RAG
    content_list = []
    for idx, row in symptoms_df.iterrows():
        # Create structured text from symptom data
        symptom_text = f"""
Symptom: {row["symptom_name"]}
Category: {row["category"]}
Severity Scale: {row["severity"]}/10
Age Range: {row["typical_age_range"]}
Urgency: {row["urgency_level"]}
Description: {row["description"]}
Common Causes: {row["common_causes"]}
        """.strip()

        content_list.append({"type": "text", "text": symptom_text, "page_idx": idx})

    print(f"   ✅ Converted to {len(content_list)} content items")

    # Demo table processing
    table_markdown = symptoms_df[
        ["symptom_name", "category", "severity", "urgency_level"]
    ].to_markdown(index=False)

    content_list.append(
        {
            "type": "table",
            "table_body": table_markdown,
            "table_caption": ["Medical Symptoms Classification Summary"],
            "table_footnote": ["Synthetic data for demonstration purposes"],
            "page_idx": len(content_list),
        }
    )

    print("   ✅ Added structured table representation")

    # Example RAG integration code (commented out - requires API setup)
    print("\n💡 RAG Integration Example:")
    print("""
    # Real integration code would look like:

    from raganything import RAGAnything, RAGAnythingConfig

    config = RAGAnythingConfig(
        working_dir="./rag_storage_medical",
        enable_table_processing=True,
    )

    rag = RAGAnything(
        config=config,
        llm_model_func=your_llm_function,
        vision_model_func=your_vision_function,
        embedding_func=your_embedding_function,
    )

    # Insert the processed content
    await rag.insert_content_list(
        content_list=content_list,
        file_path="medical_symptoms_small.xlsx"
    )

    # Query medical knowledge
    result = await rag.aquery(
        "What are the most critical symptoms that require immediate attention?",
        mode="hybrid"
    )
    """)


async def process_medical_csv_demo():
    """Demo: Process CSV medical data with RAG-Anything."""

    print("\n\n📚 CSV Dataset RAG Processing Demo")
    print("=" * 50)

    datasets_dir = os.path.join(os.path.dirname(__file__), "..")

    # Load abstracts data (sample for demo)
    abstracts_path = os.path.join(datasets_dir, "medical_abstracts_medium.csv")
    abstracts_df = pd.read_csv(abstracts_path, nrows=100)  # Sample for demo

    print("📚 Processing medical_abstracts_medium.csv (sample)...")
    print(f"   📊 Sample records: {len(abstracts_df)}")

    # Convert to content list format
    content_list = []
    for idx, row in abstracts_df.iterrows():
        # Create rich text from abstract data
        abstract_text = f"""
Title: {row["title"]}
Journal: {row["journal"]}
Publication Date: {row["publication_date"]}
DOI: {row["doi"]}
Authors: {row["authors"]}
Keywords: {row["keywords"]}

Abstract:
{row["abstract"]}

Citation Count: {row["citation_count"]}
        """.strip()

        content_list.append({"type": "text", "text": abstract_text, "page_idx": idx})

    print(f"   ✅ Converted to {len(content_list)} research articles")

    # Example queries for medical abstracts
    example_queries = [
        "What are the latest treatments for cardiovascular disease?",
        "Find research on diabetes management and patient outcomes",
        "What clinical trials show promising results for cancer treatment?",
        "Summarize recent findings on mental health interventions",
        "What are the emerging trends in medical research?",
    ]

    print("\n🔍 Example Queries for Medical Literature:")
    for i, query in enumerate(example_queries, 1):
        print(f"   {i}. {query}")

    print("\n💡 RAG Integration Example:")
    print("""
    # Process medical literature with RAG:

    await rag.insert_content_list(
        content_list=content_list,
        file_path="medical_abstracts_medium.csv"
    )

    # Advanced multimodal query with research context
    result = await rag.aquery_with_multimodal(
        "Compare these research findings with the latest literature",
        multimodal_content=[{
            "type": "table",
            "table_data": research_results_df.to_csv(),
            "table_caption": "Clinical trial results comparison"
        }],
        mode="hybrid"
    )
    """)


async def clinical_trials_demo():
    """Demo: Process clinical trials data for trial matching."""

    print("\n\n🧪 Clinical Trials RAG Processing Demo")
    print("=" * 50)

    datasets_dir = os.path.join(os.path.dirname(__file__), "..")

    # Load trials data (sample for demo)
    trials_path = os.path.join(datasets_dir, "clinical_trials_medium.csv")
    trials_df = pd.read_csv(trials_path, nrows=50)  # Sample for demo

    print("🧪 Processing clinical_trials_medium.csv (sample)...")
    print(f"   📊 Sample trials: {len(trials_df)}")

    # Process by medical condition for better organization
    conditions = trials_df["condition"].unique()[:5]  # Top 5 conditions in sample

    for condition in conditions:
        condition_trials = trials_df[trials_df["condition"] == condition]
        print(f"\n   📋 {condition}: {len(condition_trials)} trials")

        # Create content for this condition
        condition_content = []
        for idx, row in condition_trials.iterrows():
            trial_text = f"""
Trial ID: {row["trial_id"]}
Title: {row["title"]}
Condition: {row["condition"]}
Intervention: {row["intervention"]}
Phase: {row["phase"]}
Status: {row["status"]}
Start Date: {row["start_date"]}
Estimated Completion: {row["estimated_completion"]}
Sponsor: {row["sponsor"]}
Target Enrollment: {row["enrollment_target"]}
Primary Endpoint: {row["primary_endpoint"]}
Location: {row["location"]}
Inclusion Criteria: {row["inclusion_criteria"]}
Exclusion Criteria: {row["exclusion_criteria"]}
            """.strip()

            condition_content.append(
                {"type": "text", "text": trial_text, "page_idx": idx}
            )

    # Example use cases for clinical trials data
    use_cases = [
        "Patient trial matching based on medical condition",
        "Research pipeline analysis by pharmaceutical companies",
        "Drug development timeline tracking",
        "Regulatory approval pattern analysis",
        "Geographic distribution of clinical research",
    ]

    print("\n🎯 Clinical Trials Use Cases:")
    for i, use_case in enumerate(use_cases, 1):
        print(f"   {i}. {use_case}")

    print("\n💡 Trial Matching Example:")
    print("""
    # Advanced trial matching with patient criteria:

    patient_query = '''
    Find clinical trials for a 45-year-old patient with Type 2 diabetes
    who has not responded well to standard treatments and is interested
    in participating in a Phase II or III trial in the United States.
    '''

    result = await rag.aquery(patient_query, mode="hybrid")

    # The RAG system can match:
    # - Medical condition (Type 2 diabetes)
    # - Age criteria (45 years old)
    # - Trial phase preferences (II or III)
    # - Geographic constraints (United States)
    # - Treatment history (failed standard treatments)
    """)


async def integrated_medical_knowledge_demo():
    """Demo: Integrated querying across all medical datasets."""

    print("\n\n🔗 Integrated Medical Knowledge Demo")
    print("=" * 50)

    print("🧠 Cross-Dataset Query Examples:")

    cross_queries = [
        {
            "query": "Patient presents with chest pain and shortness of breath. What are the urgency considerations and relevant clinical trials?",
            "datasets": ["symptoms", "trials"],
            "reasoning": "Combines symptom urgency classification with available treatment trials",
        },
        {
            "query": "Find research abstracts and clinical trials related to diabetes management in elderly patients",
            "datasets": ["abstracts", "trials", "patients"],
            "reasoning": "Cross-references literature, ongoing trials, and patient demographics",
        },
        {
            "query": "What are the latest treatment approaches for depression based on research and current clinical trials?",
            "datasets": ["abstracts", "trials"],
            "reasoning": "Integrates published research with ongoing clinical development",
        },
    ]

    for i, example in enumerate(cross_queries, 1):
        print(f"\n   {i}. Query: {example['query']}")
        print(f"      Datasets: {', '.join(example['datasets'])}")
        print(f"      Reasoning: {example['reasoning']}")

    print("\n🚀 Advanced Integration Benefits:")
    benefits = [
        "Real-time clinical decision support",
        "Personalized treatment recommendations",
        "Research-to-practice translation",
        "Evidence-based medicine automation",
        "Clinical trial patient matching",
        "Medical literature synthesis",
    ]

    for benefit in benefits:
        print(f"   ✅ {benefit}")


async def main():
    """Main demo function."""

    print("🏥 RAG-Anything Medical Dataset Integration Examples")
    print("=" * 60)

    try:
        await process_medical_excel_demo()
        await process_medical_csv_demo()
        await clinical_trials_demo()
        await integrated_medical_knowledge_demo()

        print("\n\n✅ RAG Integration Demo Complete!")
        print("🔗 Next Steps:")
        print("   1. Set up your LLM and embedding model APIs")
        print("   2. Configure RAGAnything with your credentials")
        print("   3. Run the actual RAG processing pipeline")
        print("   4. Build medical AI applications on top of the knowledge base")

    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print("💡 This is a demonstration script showing RAG integration patterns.")


if __name__ == "__main__":
    asyncio.run(main())
