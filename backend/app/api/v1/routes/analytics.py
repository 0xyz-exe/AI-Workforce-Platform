from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import db_session, get_current_user
from app.models.entities import User
from app.schemas.analytics import DashboardMetrics
from app.services.analytics import AnalyticsService

router = APIRouter()


@router.get("/dashboard", response_model=DashboardMetrics)
def dashboard(session: Session = Depends(db_session), current_user: User = Depends(get_current_user)) -> DashboardMetrics:
    service = AnalyticsService(session)
    return DashboardMetrics(**service.dashboard_metrics(current_user.company_id))