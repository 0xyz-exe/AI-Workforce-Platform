from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.entities import Agent, BillingRecord, CompanyAgent, Document, Message, Subscription, User


class AnalyticsService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def dashboard_metrics(self, company_id: int) -> dict:
        active_users = self.session.scalar(select(func.count(User.id)).where(User.company_id == company_id, User.is_active.is_(True))) or 0
        active_agents = self.session.scalar(
            select(func.count(CompanyAgent.id)).where(CompanyAgent.company_id == company_id, CompanyAgent.status == "enabled")
        ) or 0
        ai_requests = self.session.scalar(select(func.count(Message.id)).where(Message.company_id == company_id)) or 0
        document_usage = self.session.scalar(select(func.count(Document.id)).where(Document.company_id == company_id)) or 0
        subscription_revenue = self.session.scalar(
            select(func.coalesce(func.sum(BillingRecord.amount_cents), 0)).where(BillingRecord.company_id == company_id)
        ) or 0
        return {
            "active_users": int(active_users),
            "active_agents": int(active_agents),
            "ai_requests": int(ai_requests),
            "cost_savings": float(ai_requests * 0.35),
            "time_saved": float(ai_requests * 6.0),
            "document_usage": int(document_usage),
            "subscription_revenue": int(subscription_revenue),
        }