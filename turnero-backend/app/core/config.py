from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    APP_NAME: str = "Turnero Backend"
    BACKEND_CORS_ORIGINS: List[str] = ["http://127.0.0.1:5173", "http://localhost:5173"]
    DATABASE_URL: str = "sqlite:///./turnero.db"
    JWT_SECRET: str = "change-me"
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
