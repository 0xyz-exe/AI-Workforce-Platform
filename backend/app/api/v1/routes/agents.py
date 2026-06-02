from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import db_session, get_current_user
from app.models.entities import User
from app.schemas.agent import AgentRead, AgentSubscribeRequest, AgentToggleRequest, CompanyAgentRead
from app.services.agents import AgentService

router = APIRouter()


@router.get("/marketplace", response_model=list[AgentRead])
def marketplace(session: Session = Depends(db_session), current_user: User = Depends(get_current_user)) -> list[AgentRead]:
    service = AgentService(session)
    return [AgentRead.model_validate(agent) for agent in service.marketplace_agents()]


@router.post("/subscribe", response_model=CompanyAgentRead)
def subscribe(payload: AgentSubscribeRequest, session: Session = Depends(db_session), current_user: User = Depends(get_current_user)) -> CompanyAgentRead:
    service = AgentService(session)
    company_agent = service.subscribe_agent(current_user.company_id, payload.agent_id)
    return CompanyAgentRead.model_validate(company_agent)


@router.post("/{agent_id}/toggle", response_model=CompanyAgentRead)
def toggle(agent_id: int, payload: AgentToggleRequest, session: Session = Depends(db_session), current_user: User = Depends(get_current_user)) -> CompanyAgentRead:
    service = AgentService(session)
    try:
        company_agent = service.toggle_agent(current_user.company_id, agent_id, payload.enabled)
        return CompanyAgentRead.model_validate(company_agent)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc