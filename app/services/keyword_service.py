from app.models.keyword_model import KeywordRequest, KeywordResponse

def process_keywords(request: KeywordRequest) -> KeywordResponse:
     # Fake traffic data — later replace with Google API results
    dummy_traffic = {kw: len(kw) * 100 for kw in request.keywords}
    
    return KeywordResponse(
        niche=request.niche,
        keywords=request.keywords,
        traffic_data=dummy_traffic
    )