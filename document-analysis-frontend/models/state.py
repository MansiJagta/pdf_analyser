from typing import TypedDict, List, Optional
from pydantic import BaseModel

class GraphState(TypedDict):
    file_path: str
    persona: str
    raw_text: str
    layout_type: str  # 'digital' or 'scanned'
    summary: str
    vector_status: str
    error: Optional[str]