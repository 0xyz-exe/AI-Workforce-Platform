from __future__ import annotations

from typing import Generic, TypeVar

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.core.tenant import get_current_company_id
from app.db.base import CompanyScopedMixin

ModelT = TypeVar("ModelT")


class BaseRepository(Generic[ModelT]):
    def __init__(self, session: Session, model: type[ModelT]) -> None:
        self.session = session
        self.model = model

    def _base_query(self) -> Select[tuple[ModelT]]:
        query = select(self.model)
        if issubclass(self.model, CompanyScopedMixin):
            company_id = get_current_company_id()
            if company_id is not None:
                query = query.where(getattr(self.model, "company_id") == company_id)
        return query

    def get(self, object_id: int) -> ModelT | None:
        return self.session.get(self.model, object_id)

    def list(self, limit: int = 100, offset: int = 0) -> list[ModelT]:
        query = self._base_query().offset(offset).limit(limit)
        return list(self.session.scalars(query))

    def add(self, entity: ModelT) -> ModelT:
        self.session.add(entity)
        self.session.flush()
        return entity

    def delete(self, entity: ModelT) -> None:
        self.session.delete(entity)