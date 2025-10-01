from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "ContentPilot AI backend is running!"}