from pydantic import BaseModel

from app.schemas.common import ORMModel, TimestampedModel


class CompanyRead(TimestampedModel):
    name: str
    slug: str
    legal_name: str | None = None
    industry: str | None = None
    size: str | None = None
    status: str


class TenantContext(BaseModel):
    company_id: int
    company_slug: str | None = None
    user_id: int | None = None
