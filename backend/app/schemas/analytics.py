from pydantic import BaseModel


class DashboardMetrics(BaseModel):
    active_users: int
    active_agents: int
    ai_requests: int
    cost_savings: float
    time_saved: float
    document_usage: int
    subscription_revenue: int
