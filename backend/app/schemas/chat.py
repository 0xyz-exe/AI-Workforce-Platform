from pydantic import BaseModel

from app.schemas.common import TimestampedModel


class ChatSessionCreate(BaseModel):
    agent_id: int
    knowledge_base_id: int | None = None
    title: str = "New chat"


class ChatSessionRead(TimestampedModel):
    company_id: int
    agent_id: int
    user_id: int | None = None
    knowledge_base_id: int | None = None
    title: str
    memory_json: dict
    is_archived: bool


class MessageCreate(BaseModel):
    content: str


class MessageRead(TimestampedModel):
    company_id: int
    chat_session_id: int
    sender_role: str
    content: str
    tokens_used: int
    metadata_json: dict
