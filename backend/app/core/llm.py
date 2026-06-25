"""LLM client factory — returns configured ChatOpenAI or Gemini instance."""

import logging

from langchain_core.language_models import BaseChatModel

from app.config import settings

logger = logging.getLogger(__name__)


def get_llm(model: str | None = None, temperature: float | None = None) -> BaseChatModel:
    temp = temperature if temperature is not None else settings.TEMPERATURE

    if settings.OLLAMA_API_KEY:
        from langchain_openai import ChatOpenAI

        resolved_model = model or settings.OLLAMA_MODEL
        logger.info("Using Ollama LLM: model=%s temp=%.2f", resolved_model, temp)
        return ChatOpenAI(
            base_url=settings.OLLAMA_BASE_URL,
            api_key=settings.OLLAMA_API_KEY,
            model=resolved_model,
            temperature=temp,
        )

    from langchain_google_genai import ChatGoogleGenerativeAI

    resolved_model = model or settings.GEMINI_MODEL
    logger.info("Using Gemini LLM: model=%s temp=%.2f", resolved_model, temp)
    return ChatGoogleGenerativeAI(
        model=resolved_model,
        temperature=temp,
        google_api_key=settings.GEMINI_API_KEY,
    )
