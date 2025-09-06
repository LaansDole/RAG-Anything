from typing import List, Optional
from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str
    mode: str = "hybrid"


class QueryResponse(BaseModel):
    result: str


class ContentItem(BaseModel):
    type: str
    text: Optional[str] = None
    page_idx: Optional[int] = 0
    # Additional optional fields for multimodal stubs
    img_path: Optional[str] = None
    table_body: Optional[str] = None
    latex: Optional[str] = None


class InsertContentListRequest(BaseModel):
    content_list: List[ContentItem]
    file_path: str = "api_content_list.txt"
    doc_id: Optional[str] = None
    display_stats: bool = True


class InsertResponse(BaseModel):
    success: bool
    doc_id: str
