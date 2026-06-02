from collections.abc import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.tenant import set_tenant


class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        company_id = request.headers.get("x-company-id")
        user_id = request.headers.get("x-user-id")
        set_tenant(int(company_id) if company_id else None, int(user_id) if user_id else None)
        response = await call_next(request)
        set_tenant(None, None)
        return response