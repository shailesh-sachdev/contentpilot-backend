from pydantic import BaseModel
from typing import List

class KeywordRequest(BaseModel):
    niche: str
    keywords: List[str]

class KeywordResponse(BaseModel):
    niche: str
    keywords: List[str]
    traffic_data: dict | None = None