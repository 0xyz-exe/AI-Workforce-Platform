from sqlalchemy.orm import Session

from app.models.entities import Company


class TenantService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_company_by_slug(self, slug: str) -> Company | None:
        return self.session.query(Company).filter(Company.slug == slug).one_or_none()

    def validate_company_access(self, company_id: int, user_company_id: int) -> bool:
        return company_id == user_company_id