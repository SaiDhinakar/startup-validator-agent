"""Application configuration loaded from environment variables via pydantic-settings."""

from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    NAME: str = "Startup CTO Agent API"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # LLM - Gemini (fallback)
    GEMINI_API_KEY: str = os.environ.get("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = "gemini-2.0-flash"

    # LLM - Ollama (primary)
    OLLAMA_API_KEY: str = os.environ.get("OLLAMA_API_KEY", "")
    OLLAMA_BASE_URL: str = os.environ.get("OLLAMA_BASE_URL", "https://ollama.com/v1")
    OLLAMA_MODEL: str = os.environ.get("OLLAMA_MODEL", "gpt-oss:20b")

    TEMPERATURE: float = 0.4

    # MongoDB
    MONGODB_URL: str = os.environ.get("MONGODB_URL", "mongodb://localhost:27017")
    MONGODB_DB_NAME: str = os.environ.get("MONGODB_DB_NAME", "startup_cto_agent")

    model_config = {"env_file": ".env"}


settings = Settings()
