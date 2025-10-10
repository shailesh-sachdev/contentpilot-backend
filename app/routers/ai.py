from fastapi import APIRouter
from pydantic import BaseModel
from app.services import ai_service
from app.services.ai_service import generate_blog_with_image  # <-- This line is required!


router = APIRouter()

class ContentRequest(BaseModel):
    prompt: str

class ContentResponse(BaseModel):
    content: str

class BlogRequest(BaseModel):
    prompt: str


@router.post("/generate", response_model=ContentResponse)
def generate_blog(data: ContentRequest):
    return ai_service.generate_content(data.prompt)

@router.post("/generate-blog")
def generate_blog(request: BlogRequest):
    return generate_blog_with_image(request.prompt)