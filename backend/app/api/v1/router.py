from fastapi import APIRouter

from app.api.v1.routes import agents, analytics, auth, billing, chat, health, knowledge

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(knowledge.router, prefix="/knowledge", tags=["knowledge"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(billing.router, prefix="/billing", tags=["billing"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
