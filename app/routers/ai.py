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

class PromptRequest(BaseModel):
    prompt: str


@router.post("/generate", response_model=ContentResponse)
def generate_blog(data: ContentRequest):
    return ai_service.generate_content(data.prompt)

@router.post("/generate-blog")
def generate_blog(request: BlogRequest):
    return generate_blog_with_image(request.prompt)

@router.post("/keyword-plan")
def keyword_plan(request: PromptRequest):
    # Call your AI keyword research service here
    from app.services.ai_service import generate_keyword_plan
    return generate_keyword_plan(request.prompt)