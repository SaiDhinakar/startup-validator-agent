"""LLM client factory. Returns configured ChatGoogleGenerativeAI instances."""

from langchain_core.language_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import settings


def get_llm(model: str | None = None, temperature: float | None = None) -> BaseChatModel:
    return ChatGoogleGenerativeAI(
        model=model or settings.GEMINI_MODEL,
        temperature=temperature if temperature is not None else settings.TEMPERATURE,
        google_api_key=settings.GEMINI_API_KEY,
    )
