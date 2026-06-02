from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.entities import Agent, CompanyAgent


class AgentService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def marketplace_agents(self) -> list[Agent]:
        return list(self.session.scalars(select(Agent).where(Agent.is_marketplace.is_(True), Agent.is_active.is_(True))))

    def subscribe_agent(self, company_id: int, agent_id: int) -> CompanyAgent:
        existing = self.session.scalar(
            select(CompanyAgent).where(CompanyAgent.company_id == company_id, CompanyAgent.agent_id == agent_id)
        )
        if existing:
            existing.status = "enabled"
            self.session.commit()
            return existing

        company_agent = CompanyAgent(company_id=company_id, agent_id=agent_id, status="enabled")
        self.session.add(company_agent)
        self.session.commit()
        return company_agent

    def toggle_agent(self, company_id: int, agent_id: int, enabled: bool) -> CompanyAgent:
        company_agent = self.session.scalar(
            select(CompanyAgent).where(CompanyAgent.company_id == company_id, CompanyAgent.agent_id == agent_id)
        )
        if company_agent is None:
            raise ValueError("Agent not subscribed")
        company_agent.status = "enabled" if enabled else "disabled"
        self.session.commit()
        return company_agent