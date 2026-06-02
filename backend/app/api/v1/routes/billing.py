from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy.orm import Session

from app.api.deps import db_session, get_current_user
from app.core.config import get_settings
from app.models.entities import User
from app.schemas.billing import CheckoutRequest, PlanRead
from app.services.billing import BillingService
from app.models.entities import Plan
from sqlalchemy import select
import stripe

router = APIRouter()


@router.get("/plans", response_model=list[PlanRead])
def plans(session: Session = Depends(db_session)) -> list[PlanRead]:
    return [PlanRead.model_validate(plan) for plan in session.scalars(select(Plan).order_by(Plan.price_monthly_cents.asc()))]


@router.post("/checkout")
def checkout(payload: CheckoutRequest, session: Session = Depends(db_session), current_user: User = Depends(get_current_user)) -> dict:
    service = BillingService(session)
    try:
        url = service.create_checkout_session(current_user.company_id, payload.plan_code, current_user.email)
        return {"url": url}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/webhook")
async def webhook(request: Request, stripe_signature: str | None = Header(default=None, alias="Stripe-Signature"), session: Session = Depends(db_session)) -> dict:
    payload = await request.body()
    try:
        event = stripe.Webhook.construct_event(payload=payload, sig_header=stripe_signature or "", secret=get_settings().stripe_webhook_secret)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Invalid webhook") from exc
    if event["type"] in {"checkout.session.completed", "invoice.paid", "customer.subscription.updated"}:
        BillingService(session).handle_subscription_event(event["data"]["object"])
    return {"received": True}