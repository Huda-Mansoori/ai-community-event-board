import os


class Config:
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/event_db")
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    DEBUG = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
