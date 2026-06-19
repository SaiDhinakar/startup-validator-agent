"""LLM client factory. Returns configured ChatOpenAI (Ollama) or ChatGoogleGenerativeAI instances."""

from langchain_core.language_models import BaseChatModel

from app.config import settings


def get_llm(model: str | None = None, temperature: float | None = None) -> BaseChatModel:
    temp = temperature if temperature is not None else settings.TEMPERATURE

    if settings.OLLAMA_API_KEY:
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            base_url=settings.OLLAMA_BASE_URL,
            api_key=settings.OLLAMA_API_KEY,
            model=model or settings.OLLAMA_MODEL,
            temperature=temp,
        )

    from langchain_google_genai import ChatGoogleGenerativeAI

    return ChatGoogleGenerativeAI(
        model=model or settings.GEMINI_MODEL,
        temperature=temp,
        google_api_key=settings.GEMINI_API_KEY,
    )
