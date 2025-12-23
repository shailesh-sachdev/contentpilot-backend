
from fastapi import APIRouter
from pydantic import BaseModel
from app.services import ai_service
from app.services.ai_service import generate_blog_with_image  # <-- This line is required!

router = APIRouter()

class KeywordSuggestionRequest(BaseModel):
    products: list[str]
    posts: list[str]

class KeywordSuggestionResponse(BaseModel):
    keywords: list[dict]

class DetailedBlogRequest(BaseModel):
    keyword: str
    context: dict = None

class DetailedBlogResponse(BaseModel):
    keyword: str
    blog: str

class ContentRequest(BaseModel):
    prompt: str

class ContentResponse(BaseModel):
    content: str

class BlogRequest(BaseModel):
    prompt: str

class PromptRequest(BaseModel):
    prompt: str

@router.post("/suggest-keywords", response_model=KeywordSuggestionResponse)
def suggest_keywords(data: KeywordSuggestionRequest):
    keywords = ai_service.suggest_keywords_from_products_and_posts(data.products, data.posts)
    # If the result is a dict with 'raw', return as a single-item list
    if isinstance(keywords, dict) and 'raw' in keywords:
        return {"keywords": [keywords]}
    return {"keywords": keywords}

@router.post("/generate-detailed-blog", response_model=DetailedBlogResponse)
def generate_detailed_blog(data: DetailedBlogRequest):
    result = ai_service.generate_detailed_blog(data.keyword, data.context)
    return result

@router.post("/generate", response_model=ContentResponse)
def generate_content(data: ContentRequest):
    return ai_service.generate_content(data.prompt)

@router.post("/generate-blog")
def generate_blog(request: BlogRequest):
    return generate_blog_with_image(request.prompt)

@router.post("/keyword-plan")
def keyword_plan(request: PromptRequest):
    # Call your AI keyword research service here
    from app.services.ai_service import generate_keyword_plan
    return generate_keyword_plan(request.prompt)