import os

class Settings:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")  # FastAPI backend
    DEBUG = os.environ.get("DEBUG", "1") == "1"

settings = Settings()
