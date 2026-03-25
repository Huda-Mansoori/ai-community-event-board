import os


class Config:
    MONGO_URI = "mongodb+srv://60304645:12class34@web2.0wcr6lw.mongodb.net/?appName=web2"
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    DEBUG = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
