import os
import uuid
import subprocess
from pathlib import Path
from fastapi import APIRouter, HTTPException, UploadFile, File

from .core import get_rag
from .models import (
    QueryRequest,
    MultimodalQueryRequest,
    QueryResponse,
    InsertContentListRequest,
    InsertResponse,
)

router = APIRouter()


def check_libreoffice_installation():
    """Check if LibreOffice is installed and available"""
    for cmd in ["libreoffice", "soffice"]:
        try:
            result = subprocess.run(
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
                detail="LibreOffice is required for Office document processing but not found. Please install LibreOffice."
            )
    
    return True


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.post("/query", response_model=QueryResponse)
async def query(req: QueryRequest):
    rag = await get_rag()
    try:
        result = await rag.aquery(req.query, mode=req.mode)
        return QueryResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query-multimodal", response_model=QueryResponse)
async def query_multimodal(req: MultimodalQueryRequest):
    rag = await get_rag()
    try:
        # Enhanced logging for debugging
        print(f"🔍 Multimodal query received: {req.query}")
        print(f"📋 Mode: {req.mode}")
        print(f"🖼️  Multimodal content count: {len(req.multimodal_content)}")
        
        # Log multimodal content structure for debugging
        if req.multimodal_content:
            for i, content in enumerate(req.multimodal_content):
                print(f"  Content {i+1}: {content}")
        else:
            print("  No multimodal content provided - will fallback to text query")
        
        result = await rag.aquery_with_multimodal(
            req.query, 
            multimodal_content=req.multimodal_content,
            mode=req.mode
        )
        
        print(f"✅ Multimodal query completed successfully")
        return QueryResponse(result=result)
        
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


@router.post("/process-file", response_model=InsertResponse)
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
            raise HTTPException(status_code=400, detail=f"Parser installation error: {str(e)}")

        await rag.process_document_complete(
            file_path=dest_path,
            output_dir=os.path.join(working_dir, "output"),
            parse_method="auto",
            display_stats=True,
        )
        # Return a doc_id hint; LightRAG uses content-derived IDs, but we can use filename UUID wrapper
        doc_id = f"doc-{uuid.uuid4()}"
        return InsertResponse(success=True, doc_id=doc_id)
    except HTTPException:
        # Re-raise HTTP exceptions (validation errors)
        raise
    except Exception as e:
        # Handle other processing errors
        error_msg = f"Document processing failed: {str(e)}"
        if "LibreOffice" in str(e):
            error_msg += " Please ensure LibreOffice is installed for Office document support."
        raise HTTPException(status_code=500, detail=error_msg)


@router.post("/insert-content-list", response_model=InsertResponse)
async def insert_content_list(req: InsertContentListRequest):
    rag = await get_rag()

    # Validate content_list structure
    if not req.content_list:
        raise HTTPException(status_code=400, detail="content_list cannot be empty")
    
    # Validate each content item
    for i, item in enumerate(req.content_list):
        if not item.type:
            raise HTTPException(status_code=400, detail=f"content_list[{i}]: type field is required")
        
        # Validate content based on type
        if item.type == "text" and not item.text:
            raise HTTPException(status_code=400, detail=f"content_list[{i}]: text field is required for type 'text'")
        elif item.type == "table" and not item.table_body:
            raise HTTPException(status_code=400, detail=f"content_list[{i}]: table_body field is required for type 'table'")
        elif item.type == "equation" and not item.latex:
            raise HTTPException(status_code=400, detail=f"content_list[{i}]: latex field is required for type 'equation'")
        elif item.type == "image" and not item.img_path:
            raise HTTPException(status_code=400, detail=f"content_list[{i}]: img_path field is required for type 'image'")

    # Convert Pydantic models to plain dicts
    content_list = [item.model_dump() for item in req.content_list]
    doc_id = req.doc_id or f"api-doc-{uuid.uuid4()}"

    try:
        await rag.insert_content_list(
            content_list=content_list,
            file_path=req.file_path,
            doc_id=doc_id,
            display_stats=req.display_stats,
        )
        return InsertResponse(success=True, doc_id=doc_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Content insertion failed: {str(e)}")
