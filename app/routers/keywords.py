from fastapi import APIRouter
from app.models.keyword_model import KeywordRequest, KeywordResponse
from app.services import keyword_service

router = APIRouter()

@router.post("/process", response_model=KeywordResponse)
def process_keywords(request: KeywordRequest):
    return keyword_service.process_keywords(request)