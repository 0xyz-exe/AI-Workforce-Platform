from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.db.session import engine
from app.middleware.tenant import TenantMiddleware
from app.models import entities
from app.services.bootstrap import seed_reference_data
from app.db.base import Base
from app.db.session import SessionLocal

settings = get_settings()

app = FastAPI(title=settings.app_name, version="0.1.0", openapi_url=f"{settings.api_v1_prefix}/openapi.json")

app.add_middleware(TenantMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        seed_reference_data(session)
        session.commit()


@app.get("/")
def root() -> dict:
    return {"service": settings.app_name, "version": "0.1.0"}
