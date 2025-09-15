from typing import List, Optional
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


class ContentItem(BaseModel):
    type: str
    text: Optional[str] = None
    page_idx: Optional[int] = 0
    # Additional optional fields for multimodal content
    img_path: Optional[str] = None
    table_body: Optional[str] = None
    table_data: Optional[str] = None
    table_caption: Optional[str] = None
    latex: Optional[str] = None
    equation_caption: Optional[str] = None


class InsertContentListRequest(BaseModel):
    content_list: List[ContentItem]
    file_path: str = "api_content_list.txt"
    doc_id: Optional[str] = None
    display_stats: bool = True


class InsertResponse(BaseModel):
    success: bool
    doc_id: str
