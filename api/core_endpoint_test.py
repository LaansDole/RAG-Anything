#!/usr/bin/env python
"""
RAG-Anything Core Endpoint Test Script

Tests the complete upload → process → Q&A pipeline for Excel and Office documents.
Assumes the service is running at http://localhost:8000
"""

import argparse
import requests
import json
import time
import sys
from pathlib import Path
import asyncio

# Service configuration
SERVICE_URL = "http://localhost:8000"
TIMEOUT = 300  # seconds


def test_health():
    """Test if the service is running"""
    try:
        response = requests.get(f"{SERVICE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Service is running")
            print("Make sure that you have updated the context length to at least 8192 tokens")
            return True
        else:
            print(f"❌ Service health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to service: {e}")
        print(f"💡 Make sure the service is running: uv run uvicorn api.app:app --reload")
        return False


def upload_and_process_file(file_path: str) -> dict:
    """Upload and process a file (Excel or Office document)"""
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    print(f"📁 Processing file: {file_path.name}")
    
    # Determine endpoint based on file extension
    if file_path.suffix.lower() in ['.xlsx', '.xls']:
        endpoint = f"{SERVICE_URL}/process-excel"
        extra_params = {
            'max_rows': '500',  # Limit rows for demo
            'convert_to_text': 'true',
            'include_summary': 'true'
        }
    else:
        endpoint = f"{SERVICE_URL}/process-file"
        extra_params = {}
    
    # Upload file
    with open(file_path, 'rb') as f:
        files = {'file': (file_path.name, f, 'application/octet-stream')}
        
        response = requests.post(
            endpoint,
            files=files,
            data=extra_params,
            timeout=TIMEOUT
        )
    
    if response.status_code != 200:
        raise Exception(f"Upload failed: {response.status_code} - {response.text}")
    
    result = response.json()
    
    if file_path.suffix.lower() in ['.xlsx', '.xls']:
        print(f"✅ Excel processed successfully:")
        print(f"   📊 Total rows: {result.get('total_rows', 'N/A')}")
        print(f"   📋 Columns: {len(result.get('columns', []))}")
        print(f"   🧩 Chunks created: {result.get('chunks_created', 'N/A')}")
        if result.get('doc_id'):
            print(f"   🔑 Document ID: {result['doc_id']}")
    else:
        print(f"✅ File processed successfully: {result.get('message', 'OK')}")
    
    return result


def query_document(query: str, mode: str = "hybrid") -> str:
    """Query the processed document"""
    print(f"🔍 Querying: {query}")
    
    payload = {
        "query": query,
        "mode": mode
    }
    
    response = requests.post(
        f"{SERVICE_URL}/query",
        json=payload,
        timeout=TIMEOUT
    )
    
    if response.status_code != 200:
        raise Exception(f"Query failed: {response.status_code} - {response.text}")
    
    result = response.json()
    answer = result.get("result", "No answer received")
    
    print(f"💬 Answer: {answer}")
    return answer


def run_pipeline_test(file_path: str):
    """Run the complete pipeline test"""
    print("🚀 Starting RAG-Anything Service Pipeline Test")
    print("=" * 60)
    
    # Step 1: Health check
    print("\n📋 Step 1: Service Health Check")
    if not test_health():
        return False
    
    # Step 2: Process document
    print("\n📋 Step 2: Document Processing")
    try:
        result = upload_and_process_file(file_path)
    except Exception as e:
        print(f"❌ Processing failed: {e}")
        return False
    
    # Wait a moment for processing to complete
    print("\n⏳ Waiting for processing to complete...")
    time.sleep(2)
    
    # Step 3: Query the document
    print("\n📋 Step 3: Document Querying")
    
    # Determine appropriate queries based on file type
    file_path_obj = Path(file_path)
    if file_path_obj.suffix.lower() in ['.xlsx', '.xls']:
        queries = [
            "What is this dataset about?",
            "Summarize the main findings or data patterns",
            "What are the key columns or variables?"
        ]
    else:
        queries = [
            "What is the main topic of this document?",
            "Can you summarize the key points?",
            "What are the main conclusions?"
        ]
    
    try:
        for i, query in enumerate(queries, 1):
            print(f"\n  Query {i}/{len(queries)}:")
            query_document(query)
            if i < len(queries):
                time.sleep(1)  # Brief pause between queries
    except Exception as e:
        print(f"❌ Querying failed: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 Pipeline test completed successfully!")
    print("\n💡 Next steps:")
    print("   • Try more complex queries")
    print("   • Test with different document types")
    print("   • Explore the web UI at http://localhost:8000/docs")
    
    return True


async def main():
    """Main test function"""
    global SERVICE_URL
    
    parser = argparse.ArgumentParser(description="Test RAG-Anything service pipeline")
    parser.add_argument("file_path", help="Path to file to process (Excel, Office docs, PDF, etc.)")
    parser.add_argument("--service-url", default=SERVICE_URL, help=f"Service URL (default: {SERVICE_URL})")
    
    args = parser.parse_args()
    
    # Update global service URL if provided
    SERVICE_URL = args.service_url
    
    # Check if file exists
    if not Path(args.file_path).exists():
        print(f"❌ File not found: {args.file_path}")
        sys.exit(1)
    
    # Run the pipeline test
    success = run_pipeline_test(args.file_path)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())