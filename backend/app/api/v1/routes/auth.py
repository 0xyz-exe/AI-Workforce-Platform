from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import db_session, get_current_user
from app.models.entities import User
from app.schemas.auth import (
    ForgotPasswordRequest,
    LoginRequest,
    LogoutResponse,
    RefreshTokenRequest,
    RegisterCompanyRequest,
    RegisterUserRequest,
    ResetPasswordRequest,
    TokenPair,
)
from app.schemas.common import ORMModel
from app.services.auth import AuthError, AuthService

router = APIRouter()


class UserRead(ORMModel):
    id: int
    company_id: int
    full_name: str
    email: str
    is_active: bool
    is_owner: bool


@router.post("/register-company", response_model=TokenPair)
def register_company(payload: RegisterCompanyRequest, session: Session = Depends(db_session)) -> TokenPair:
    service = AuthService(session)
    try:
        result = service.register_company(payload.company.model_dump(), payload.owner.model_dump(), payload.plan_code)
        return TokenPair(**result["tokens"])
    except AuthError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/register-user", response_model=UserRead)
def register_user(payload: RegisterUserRequest, session: Session = Depends(db_session), current_user: User = Depends(get_current_user)) -> UserRead:
    service = AuthService(session)
    try:
        user = service.register_user(current_user.company_id, payload.model_dump(exclude={"role"}), payload.role)
        return UserRead.model_validate(user)
    except AuthError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/login", response_model=TokenPair)
def login(payload: LoginRequest, session: Session = Depends(db_session)) -> TokenPair:
    service = AuthService(session)
    try:
        user = service.authenticate(payload.company_slug, payload.email, payload.password)
        return TokenPair(**service.issue_tokens(user))
    except AuthError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


@router.post("/refresh", response_model=TokenPair)
def refresh_token(payload: dict, session: Session = Depends(db_session)) -> TokenPair:
    service = AuthService(session)
    try:
        return TokenPair(**service.refresh_tokens(payload["refresh_token"]))
    except (AuthError, KeyError) as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to refresh token") from exc


@router.post("/forgot-password")
def forgot_password(payload: ForgotPasswordRequest, session: Session = Depends(db_session)) -> dict:
    service = AuthService(session)
    try:
        token = service.create_password_reset_token(payload.company_slug, payload.email)
        return {"reset_token": token}
    except AuthError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/reset-password")
def reset_password(payload: ResetPasswordRequest, session: Session = Depends(db_session)) -> dict:
    service = AuthService(session)
    try:
        service.reset_password(payload.token, payload.company_slug, payload.email, payload.new_password)
        return {"success": True}
    except AuthError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/logout", response_model=LogoutResponse)
def logout() -> LogoutResponse:
    return LogoutResponse()