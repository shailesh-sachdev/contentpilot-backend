from fastapi import FastAPI
from app.routers import keywords
from app.routers import ai


app = FastAPI()

app.include_router(keywords.router, prefix="/keywords", tags=["keywords"])
app.include_router(ai.router, prefix="/ai", tags=["AI"])

@app.get("/")
def root():
    return {"message": "ContentPilot AI backend is running!"}