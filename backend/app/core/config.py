from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "AI Workforce Platform"
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"
    frontend_url: str = "http://localhost:3000"
    backend_url: str = "http://localhost:8000"

    database_url: str
    jwt_secret_key: str
    jwt_refresh_secret_key: str
    jwt_access_token_expires_minutes: int = 15
    jwt_refresh_token_expires_days: int = 30

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"

    qdrant_url: str = "http://qdrant:6333"
    qdrant_api_key: str = ""
    qdrant_collection: str = "ai_workforce_chunks"

    aws_access_key_id: str = "minio"
    aws_secret_access_key: str = "minio123456"
    aws_region: str = "us-east-1"
    aws_bucket: str = "ai-workforce"
    aws_endpoint_url: str = "http://minio:9000"

    redis_url: str = "redis://redis:6379/0"
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()