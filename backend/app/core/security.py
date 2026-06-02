from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from app.core.config import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
settings = get_settings()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_token(subject: str, expires_delta: timedelta, secret_key: str, token_type: str, claims: dict[str, Any] | None = None) -> str:
    payload: dict[str, Any] = {
        "sub": subject,
        "type": token_type,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + expires_delta,
    }
    if claims:
        payload.update(claims)
    return jwt.encode(payload, secret_key, algorithm="HS256")


def create_access_token(subject: str, claims: dict[str, Any] | None = None) -> str:
    return create_token(
        subject=subject,
        expires_delta=timedelta(minutes=settings.jwt_access_token_expires_minutes),
        secret_key=settings.jwt_secret_key,
        token_type="access",
        claims=claims,
    )


def create_refresh_token(subject: str, claims: dict[str, Any] | None = None) -> str:
    return create_token(
        subject=subject,
        expires_delta=timedelta(days=settings.jwt_refresh_token_expires_days),
        secret_key=settings.jwt_refresh_secret_key,
        token_type="refresh",
        claims=claims,
    )


def decode_token(token: str, secret_key: str) -> dict[str, Any]:
    return jwt.decode(token, secret_key, algorithms=["HS256"])
