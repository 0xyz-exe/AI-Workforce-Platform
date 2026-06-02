from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.entities import Company


class CompanyService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_companies(self) -> list[Company]:
        return list(self.session.scalars(select(Company).order_by(Company.created_at.desc())))