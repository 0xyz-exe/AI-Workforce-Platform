from functools import lru_cache

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from app.core.config import get_settings

settings = get_settings()


@lru_cache
def get_chat_model() -> ChatOpenAI:
    return ChatOpenAI(api_key=settings.openai_api_key, model=settings.openai_model, temperature=0.2)


@lru_cache
def get_embeddings() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(api_key=settings.openai_api_key, model=settings.embedding_model)