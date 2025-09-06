import os
import uuid
from fastapi import APIRouter, HTTPException, UploadFile, File

from .core import get_rag
from .models import (
    QueryRequest,
    QueryResponse,
    InsertContentListRequest,
    InsertResponse,
)

router = APIRouter()


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


@router.post("/process-file", response_model=InsertResponse)
async def process_file(file: UploadFile = File(...)):
    rag = await get_rag()
    # Verify parser for document processing context
    try:
        rag.verify_parser_installation_once()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Save uploaded file to a temp path inside working directory
    working_dir = rag.config.working_dir
    os.makedirs(working_dir, exist_ok=True)
    dest_path = os.path.join(working_dir, file.filename)

    try:
        with open(dest_path, "wb") as f:
            f.write(await file.read())

        await rag.process_document_complete(
            file_path=dest_path,
            output_dir=os.path.join(working_dir, "output"),
            parse_method="auto",
            display_stats=True,
        )
        # Return a doc_id hint; LightRAG uses content-derived IDs, but we can use filename UUID wrapper
        doc_id = f"doc-{uuid.uuid4()}"
        return InsertResponse(success=True, doc_id=doc_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/insert-content-list", response_model=InsertResponse)
async def insert_content_list(req: InsertContentListRequest):
    rag = await get_rag()

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
        raise HTTPException(status_code=500, detail=str(e))
