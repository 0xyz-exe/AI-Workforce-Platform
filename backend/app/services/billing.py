from __future__ import annotations

from datetime import datetime, timezone

import stripe
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.entities import BillingRecord, Company, Plan, Subscription

settings = get_settings()
stripe.api_key = settings.stripe_secret_key


class BillingService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_checkout_session(self, company_id: int, plan_code: str, customer_email: str) -> str:
        plan = self.session.scalar(select(Plan).where(Plan.code == plan_code))
        if plan is None:
            raise ValueError("Plan not found")
        company = self.session.get(Company, company_id)
        if company is None:
            raise ValueError("Company not found")

        checkout_session = stripe.checkout.Session.create(
            mode="subscription",
            customer_email=customer_email,
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": plan.name},
                        "unit_amount": plan.price_monthly_cents,
                        "recurring": {"interval": "month"},
                    },
                    "quantity": 1,
                }
            ],
            success_url=f"{settings.frontend_url}/billing?success=1",
            cancel_url=f"{settings.frontend_url}/billing?canceled=1",
            metadata={"company_id": str(company_id), "plan_code": plan_code},
        )
        return checkout_session.url or ""

    def handle_subscription_event(self, payload: dict) -> None:
        company_id = int(payload.get("metadata", {}).get("company_id", 0))
        plan_code = payload.get("metadata", {}).get("plan_code")
        if not company_id or not plan_code:
            return
        plan = self.session.scalar(select(Plan).where(Plan.code == plan_code))
        subscription = self.session.scalar(select(Subscription).where(Subscription.company_id == company_id))
        if plan and subscription:
            subscription.plan_id = plan.id
            subscription.status = payload.get("status", subscription.status)
            billing_record = BillingRecord(
                company_id=company_id,
                subscription_id=subscription.id,
                amount_cents=plan.price_monthly_cents,
                currency="usd",
                record_type="subscription",
                status="paid",
                paid_at=datetime.now(timezone.utc),
                metadata_json=payload,
            )
            self.session.add(billing_record)
            self.session.commit()