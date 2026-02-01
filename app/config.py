import os
from dotenv import load_dotenv

load_dotenv()


GOOGLE_DEVELOPER_TOKEN = os.getenv("GOOGLE_DEVELOPER_TOKEN", "")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REFRESH_TOKEN = os.getenv("GOOGLE_REFRESH_TOKEN", "")
GOOGLE_CUSTOMER_ID = os.getenv("GOOGLE_CUSTOMER_ID", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")

# ✅ map Render env vars to your code
OLLAMA_USERNAME = os.getenv("OLLAMA_BASIC_AUTH_USER")
OLLAMA_PASSWORD = os.getenv("OLLAMA_BASIC_AUTH_PASS")