from fastapi import APIRouter
from pydantic import BaseModel
from app.services import ai_service

router = APIRouter()

class ContentRequest(BaseModel):
    prompt: str

class ContentResponse(BaseModel):
    content: str

@router.post("/generate", response_model=ContentResponse)
def generate_blog(data: ContentRequest):
    return ai_service.generate_content(data.prompt)
