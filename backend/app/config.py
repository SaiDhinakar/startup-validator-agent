"""Application configuration loaded from environment variables via pydantic-settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Startup CTO Agent API"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # LLM
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.0-flash"
    TEMPERATURE: float = 0.7

    # MongoDB
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "cto_agent"

    model_config = {"env_prefix": "APP_"}


settings = Settings()
