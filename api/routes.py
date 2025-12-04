import os
import uuid
import subprocess
from pathlib import Path
from typing import Union, Optional
import json
import re
from fastapi import APIRouter, HTTPException, UploadFile, File

from .core import get_rag
from .models import (
    QueryRequest,
    MultimodalQueryRequest,
    QueryResponse,
    ExcelProcessingResponse,
    FileProcessingResponse,
)

router = APIRouter()


def serialize_for_json(obj):
    """Convert numpy types and other non-serializable types to JSON-serializable types"""
    import numpy as np

    if isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: serialize_for_json(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [serialize_for_json(item) for item in obj]
    else:
        return obj


def check_libreoffice_installation():
    """Check if LibreOffice is installed and available"""
    for cmd in ["libreoffice", "soffice"]:
        try:
            subprocess.run(
                [cmd, "--version"], capture_output=True, check=True, timeout=10
            )
            return True
        except (
            subprocess.CalledProcessError,
            FileNotFoundError,
            subprocess.TimeoutExpired,
        ):
            continue
    return False


def validate_office_document(file_path: str):
    """Validate if file is a supported Office document format"""
    supported_extensions = {".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx"}
    file_path_obj = Path(file_path)

    if not file_path_obj.exists():
        raise HTTPException(status_code=400, detail=f"File does not exist: {file_path}")

    if file_path_obj.suffix.lower() in supported_extensions:
        if not check_libreoffice_installation():
            raise HTTPException(
                status_code=400,
                detail="LibreOffice is required for Office document processing but not found. Please install LibreOffice.",
            )

    return True


@router.get("/health")
async def health():
    return {"status": "ok"}


def parse_structured_response(result: str) -> dict:
    """
    Parse LLM response and return structured data if it contains JSON,
    otherwise return the original result as a simple string response.
    """
    # Check if the result looks like it contains structured JSON
    if not result or len(result.strip()) < 10:
        return {"result": result}

    result_stripped = result.strip()

    # Try to detect and extract JSON from the response
    json_match = None

    # Look for JSON block patterns
    json_patterns = [
        r'\{[\s\S]*"detailed_description"[\s\S]*"entity_info"[\s\S]*\}',  # Full JSON with required fields
        r'\{[\s\S]*"entity_info"[\s\S]*"detailed_description"[\s\S]*\}',  # Reversed order
        r"\{[\s\S]*\}",  # Any JSON-like structure
    ]

    for pattern in json_patterns:
        json_match = re.search(pattern, result_stripped, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            try:
                parsed_json = json.loads(json_str)
                # Validate that it has the expected structure
                if (
                    isinstance(parsed_json, dict)
                    and "detailed_description" in parsed_json
                    and "entity_info" in parsed_json
                ):
                    entity_info = parsed_json.get("entity_info", {})
                    if (
                        isinstance(entity_info, dict)
                        and "entity_name" in entity_info
                        and "entity_type" in entity_info
                        and "summary" in entity_info
                    ):
                        # Return the structured response
                        return parsed_json

            except json.JSONDecodeError:
                continue

    # If no valid JSON structure found, return as simple result
    return {"result": result}


@router.post("/query", response_model=QueryResponse)
async def query(req: QueryRequest):
    rag = await get_rag()
    try:
        result = await rag.aquery(req.query, mode=req.mode)

        # Parse the response to detect structured JSON
        structured_result = parse_structured_response(result)

        # If we found structured data, return it directly
        if "detailed_description" in structured_result:
            return QueryResponse(result=structured_result)
        else:
            # Return the original result for backward compatibility
            return QueryResponse(result=structured_result.get("result", result))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query-multimodal", response_model=QueryResponse)
async def query_multimodal(req: MultimodalQueryRequest):
    rag = await get_rag()
    try:
        # Enhanced logging for debugging
        print(f"🔍 Multimodal query received: {req.query}")
        print(f"📋 Mode: {req.mode}")
        print(f"🎯 Multimodal content count: {len(req.multimodal_content)}")

        # Log multimodal content structure for debugging
        if req.multimodal_content:
            for i, content in enumerate(req.multimodal_content):
                print(f"  Content {i + 1}: {content}")
        else:
            print("  No multimodal content provided - will fallback to text query")

        # For Office documents, we process structured content (tables, text) without images
        result = await rag.aquery_with_multimodal(
            req.query, multimodal_content=req.multimodal_content, mode=req.mode
        )

        print("✅ Multimodal query completed successfully")

        # Parse the response to detect structured JSON
        structured_result = parse_structured_response(result)

        # If we found structured data, return it directly
        if "detailed_description" in structured_result:
            return QueryResponse(result=structured_result)
        else:
            # Return the original result for backward compatibility
            return QueryResponse(result=structured_result.get("result", result))

    except AttributeError as e:
        error_msg = f"Method not available: aquery_with_multimodal() - {str(e)}"
        print(f"❌ AttributeError: {error_msg}")
        raise HTTPException(status_code=501, detail=error_msg)
    except TypeError as e:
        error_msg = f"Invalid parameters for aquery_with_multimodal(): {str(e)}"
        print(f"❌ TypeError: {error_msg}")
        raise HTTPException(status_code=400, detail=error_msg)
    except Exception as e:
        error_msg = f"Multimodal query failed: {str(e)}"
        print(f"❌ Exception: {error_msg}")
        print(f"🔍 Exception type: {type(e).__name__}")
        import traceback

        print(f"📍 Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=error_msg)


@router.post("/process-file", response_model=FileProcessingResponse)
async def process_file(file: UploadFile = File(...)):
    rag = await get_rag()

    # Save uploaded file to a temp path inside working directory
    working_dir = rag.config.working_dir
    os.makedirs(working_dir, exist_ok=True)
    dest_path = os.path.join(working_dir, file.filename)

    try:
        with open(dest_path, "wb") as f:
            f.write(await file.read())

        # Validate file format and check dependencies
        validate_office_document(dest_path)

        # Verify parser installation for document processing context
        try:
            rag.verify_parser_installation_once()
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Parser installation error: {str(e)}"
            )

        await rag.process_document_complete(
            file_path=dest_path,
            output_dir=os.path.join(working_dir, "output"),
            parse_method="auto",
            display_stats=True,
        )
        # Return success response with filename
        return FileProcessingResponse(
            success=True,
            message=f"Successfully processed document: {file.filename}",
            file_path=dest_path,
        )
    except HTTPException:
        # Re-raise HTTP exceptions (validation errors)
        raise
    except Exception as e:
        # Handle other processing errors
        error_msg = f"Document processing failed: {str(e)}"
        if "LibreOffice" in str(e):
            error_msg += (
                " Please ensure LibreOffice is installed for Office document support."
            )
        raise HTTPException(status_code=500, detail=error_msg)


@router.post("/process-excel", response_model=ExcelProcessingResponse)
async def process_excel_file(
    file: UploadFile = File(...),
    max_rows: Optional[int] = None,
    sheet_name: Union[str, int] = 0,
    convert_to_text: bool = True,
    include_summary: bool = True,
    chunk_size: int = 100,
    doc_id: Optional[str] = None,
):
    """Process Excel file and insert into RAG system"""
    rag = await get_rag()

    # Validate file extension
    if not file.filename.lower().endswith((".xlsx", ".xls")):
        raise HTTPException(
            status_code=400, detail="Only Excel files (.xlsx, .xls) are supported"
        )

    # Save uploaded file to a temp path inside working directory
    working_dir = rag.config.working_dir
    os.makedirs(working_dir, exist_ok=True)
    dest_path = os.path.join(working_dir, file.filename)

    try:
        with open(dest_path, "wb") as f:
            f.write(await file.read())

        # Process Excel file using RAGAnything's Excel processor
        result = await rag.process_excel_file(
            file_path=dest_path,
            max_rows=max_rows,
            convert_to_text=convert_to_text,
            include_summary=include_summary,
            chunk_size=chunk_size,
            doc_id=doc_id or f"excel-{uuid.uuid4()}",
        )

        # Ensure ALL data is properly serialized before creating the response
        result = serialize_for_json(result)

        if result["success"]:
            # Convert numpy types to Python types for Pydantic serialization
            total_rows = (
                int(result["total_rows"]) if result.get("total_rows") is not None else 0
            )
            chunks_created = (
                int(result["chunks_created"])
                if result.get("chunks_created") is not None
                else 0
            )
            columns = [str(col) for col in result.get("columns", [])]
            metadata = result.get("metadata") if result.get("metadata") else None

            return ExcelProcessingResponse(
                success=True,
                doc_id=result["doc_id"],
                total_rows=total_rows,
                columns=columns,
                chunks_created=chunks_created,
                metadata=metadata,
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Excel processing failed: {result['error']}"
            )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle other processing errors
        error_msg = f"Excel file processing failed: {str(e)}"
        raise HTTPException(status_code=500, detail=error_msg)
    finally:
        # Clean up uploaded file
        if os.path.exists(dest_path):
            try:
                os.remove(dest_path)
            except Exception:
                pass  # Ignore cleanup errors
