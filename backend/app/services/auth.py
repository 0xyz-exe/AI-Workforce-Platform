from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import create_access_token, create_refresh_token, decode_token, hash_password, verify_password
from app.models.entities import Company, Permission, Plan, Role, Subscription, User, UserRole
from app.services.bootstrap import seed_reference_data

settings = get_settings()


class AuthError(ValueError):
    pass


class AuthService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def register_company(self, company_data: dict, owner_data: dict, plan_code: str) -> dict:
        seed_reference_data(self.session)
        plan = self.session.scalar(select(Plan).where(Plan.code == plan_code))
        if plan is None:
            raise AuthError("Plan not found")

        if self.session.scalar(select(Company).where(Company.slug == company_data["slug"])):
            raise AuthError("Company slug already exists")

        company = Company(**company_data)
        self.session.add(company)
        self.session.flush()

        owner = User(
            company_id=company.id,
            full_name=owner_data["full_name"],
            email=owner_data["email"].lower(),
            password_hash=hash_password(owner_data["password"]),
            is_active=True,
            is_owner=True,
        )
        self.session.add(owner)
        self.session.flush()

        owner_role = self.session.scalar(select(Role).where(Role.name == "Owner"))
        assert owner_role is not None
        self.session.add(UserRole(user_id=owner.id, role_id=owner_role.id))

        subscription = Subscription(company_id=company.id, plan_id=plan.id, status="active")
        self.session.add(subscription)
        self.session.commit()

        return {
            "company": company,
            "user": owner,
            "subscription": subscription,
            "tokens": self.issue_tokens(owner),
        }

    def register_user(self, company_id: int, user_data: dict, role_name: str) -> User:
        user = User(
            company_id=company_id,
            full_name=user_data["full_name"],
            email=user_data["email"].lower(),
            password_hash=hash_password(user_data["password"]),
            is_active=True,
            is_owner=False,
        )
        self.session.add(user)
        self.session.flush()

        role = self.session.scalar(select(Role).where(Role.name == role_name))
        if role is None:
            raise AuthError("Role not found")
        self.session.add(UserRole(user_id=user.id, role_id=role.id))
        self.session.commit()
        return user

    def authenticate(self, company_slug: str, email: str, password: str) -> User:
        company = self.session.scalar(select(Company).where(Company.slug == company_slug))
        if company is None:
            raise AuthError("Invalid credentials")

        user = self.session.scalar(
            select(User).where(User.company_id == company.id, User.email == email.lower())
        )
        if user is None or not verify_password(password, user.password_hash):
            raise AuthError("Invalid credentials")

        user.last_login_at = datetime.now(timezone.utc)
        self.session.commit()
        return user

    def issue_tokens(self, user: User) -> dict:
        permissions = self._resolve_permissions(user)
        claims = {"company_id": user.company_id, "permissions": permissions, "email": user.email}
        access_token = create_access_token(str(user.id), claims=claims)
        refresh_token = create_refresh_token(str(user.id), claims=claims)
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_access_token_expires_minutes)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_at": expires_at,
        }

    def refresh_tokens(self, refresh_token: str) -> dict:
        payload = decode_token(refresh_token, settings.jwt_refresh_secret_key)
        if payload.get("type") != "refresh":
            raise AuthError("Invalid refresh token")
        user = self.session.get(User, int(payload["sub"]))
        if user is None:
            raise AuthError("User not found")
        return self.issue_tokens(user)

    def create_password_reset_token(self, company_slug: str, email: str) -> str:
        company = self.session.scalar(select(Company).where(Company.slug == company_slug))
        if company is None:
            raise AuthError("Company not found")
        user = self.session.scalar(select(User).where(User.company_id == company.id, User.email == email.lower()))
        if user is None:
            raise AuthError("User not found")
        token = create_refresh_token(str(user.id), claims={"company_id": company.id, "purpose": "password_reset"})
        user.password_reset_token_hash = hash_password(token)
        user.password_reset_expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
        self.session.commit()
        return token

    def reset_password(self, token: str, company_slug: str, email: str, new_password: str) -> None:
        payload = decode_token(token, settings.jwt_refresh_secret_key)
        if payload.get("purpose") != "password_reset":
            raise AuthError("Invalid reset token")

        company = self.session.scalar(select(Company).where(Company.slug == company_slug))
        if company is None:
            raise AuthError("Company not found")
        user = self.session.scalar(select(User).where(User.company_id == company.id, User.email == email.lower()))
        if user is None:
            raise AuthError("User not found")
        if user.password_reset_expires_at is None or user.password_reset_expires_at < datetime.now(timezone.utc):
            raise AuthError("Reset token expired")
        if user.password_reset_token_hash is None or not verify_password(token, user.password_reset_token_hash):
            raise AuthError("Invalid reset token")

        user.password_hash = hash_password(new_password)
        user.password_reset_token_hash = None
        user.password_reset_expires_at = None
        self.session.commit()

    def _resolve_permissions(self, user: User) -> list[str]:
        permissions: set[str] = set()
        for role_link in user.roles:
            for role_permission in role_link.role.permissions:
                permissions.add(role_permission.permission.code)
        return sorted(permissions)