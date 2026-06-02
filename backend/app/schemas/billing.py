from pydantic import BaseModel

from app.schemas.common import TimestampedModel


class PlanRead(TimestampedModel):
    code: str
    name: str
    description: str | None = None
    price_monthly_cents: int
    max_users: int
    max_agents: int
    features: dict
    is_active: bool


class SubscriptionRead(TimestampedModel):
    company_id: int
    plan_id: int
    status: str
    stripe_customer_id: str | None = None
    stripe_subscription_id: str | None = None
    current_period_start: str | None = None
    current_period_end: str | None = None


class CheckoutRequest(BaseModel):
    plan_code: str
