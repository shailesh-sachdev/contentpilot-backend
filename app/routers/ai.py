
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging
from app.services import ai_service
from app.services.ai_service import generate_blog_with_image  # <-- This line is required!

router = APIRouter()
logger = logging.getLogger(__name__)

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
    try:
        keywords = ai_service.suggest_keywords_from_products_and_posts(data.products, data.posts)
        # If the result is a dict with 'raw', return as a single-item list
        if isinstance(keywords, dict) and 'raw' in keywords:
            return {"keywords": [keywords]}
        return {"keywords": keywords}
    except Exception as e:
        logger.error(f"Failed to suggest keywords: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate keyword suggestions: {str(e)}"
        )

@router.post("/generate-detailed-blog", response_model=DetailedBlogResponse)
def generate_detailed_blog(data: DetailedBlogRequest):
    try:
        result = ai_service.generate_detailed_blog(data.keyword, data.context)
        return result
    except Exception as e:
        logger.error(f"Failed to generate detailed blog for keyword '{data.keyword}': {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate blog post: {str(e)}"
        )

@router.post("/generate", response_model=ContentResponse)
def generate_content(data: ContentRequest):
    try:
        return ai_service.generate_content(data.prompt)
    except Exception as e:
        logger.error(f"Failed to generate content: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate content: {str(e)}"
        )

@router.post("/generate-blog")
def generate_blog(request: BlogRequest):
    try:
        return generate_blog_with_image(request.prompt)
    except Exception as e:
        logger.error(f"Failed to generate blog with image: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate blog: {str(e)}"
        )

@router.post("/keyword-plan")
def keyword_plan(request: PromptRequest):
    try:
        from app.services.ai_service import generate_keyword_plan
        return generate_keyword_plan(request.prompt)
    except Exception as e:
        logger.error(f"Failed to generate keyword plan: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate keyword plan: {str(e)}"
        )