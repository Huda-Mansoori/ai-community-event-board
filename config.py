import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    MONGO_URI = os.environ.get("MONGO_URI", "")
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    DEBUG = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
