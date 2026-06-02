from contextvars import ContextVar
from typing import Optional

current_company_id: ContextVar[Optional[int]] = ContextVar("current_company_id", default=None)
current_user_id: ContextVar[Optional[int]] = ContextVar("current_user_id", default=None)


def set_tenant(company_id: int | None, user_id: int | None = None) -> None:
    current_company_id.set(company_id)
    current_user_id.set(user_id)


def get_current_company_id() -> int | None:
    return current_company_id.get()


def get_current_user_id() -> int | None:
    return current_user_id.get()