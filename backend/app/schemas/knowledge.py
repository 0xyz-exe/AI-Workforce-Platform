from pydantic import BaseModel

from app.schemas.common import TimestampedModel


class KnowledgeBaseCreate(BaseModel):
    name: str
    description: str | None = None
    is_default: bool = False


class KnowledgeBaseRead(TimestampedModel):
    company_id: int
    name: str
    description: str | None = None
    is_default: bool
    indexing_status: str


class DocumentRead(TimestampedModel):
    company_id: int
    knowledge_base_id: int
    uploaded_by_id: int | None = None
    filename: str
    mime_type: str
    file_size: int
    s3_key: str
    status: str
    page_count: int | None = None
    chunk_count: int
    metadata_json: dict
