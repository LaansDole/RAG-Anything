from typing import List, Optional, Union
from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str
    mode: str = "hybrid"


class MultimodalQueryRequest(BaseModel):
    query: str
    mode: str = "hybrid"
    multimodal_content: List[dict] = []


class QueryResponse(BaseModel):
    result: str


# Excel Processing Models
class ExcelProcessingRequest(BaseModel):
    max_rows: Optional[int] = None
    sheet_name: Union[str, int, List[str]] = 0
    convert_to_text: bool = True
    include_summary: bool = True
    chunk_size: int = 100
    doc_id: Optional[str] = None


class ExcelProcessingResponse(BaseModel):
    success: bool
    doc_id: str
    total_rows: int
    columns: List[str]
    chunks_created: int
    metadata: Optional[dict] = None


# Generic file processing response
class FileProcessingResponse(BaseModel):
    success: bool
    message: str
    file_path: Optional[str] = None
    metadata: Optional[dict] = None
