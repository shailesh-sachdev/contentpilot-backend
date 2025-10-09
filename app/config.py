import os
from dotenv import load_dotenv

load_dotenv()


GOOGLE_DEVELOPER_TOKEN = os.getenv("GOOGLE_DEVELOPER_TOKEN", "")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REFRESH_TOKEN = os.getenv("GOOGLE_REFRESH_TOKEN", "")
GOOGLE_CUSTOMER_ID = os.getenv("GOOGLE_CUSTOMER_ID", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")