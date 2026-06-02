from pydantic import BaseModel, Field

from app.schemas.common import TimestampedModel


class AgentRead(TimestampedModel):
    code: str
    name: str
    category: str
    description: str
    prompt_template: str
    system_prompt: str
    default_model: str
    is_marketplace: bool
    is_active: bool
    metadata_json: dict


class AgentSubscribeRequest(BaseModel):
    agent_id: int


class CompanyAgentRead(TimestampedModel):
    company_id: int
    agent_id: int
    status: str
    usage_count: int
    config_json: dict


class AgentToggleRequest(BaseModel):
    enabled: bool = Field(default=True)
