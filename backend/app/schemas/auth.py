from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class CompanyCreate(BaseModel):
    name: str
    slug: str
    legal_name: str | None = None
    industry: str | None = None
    size: str | None = None


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str = Field(min_length=8)


class RegisterCompanyRequest(BaseModel):
    company: CompanyCreate
    owner: UserCreate
    plan_code: str = "starter"


class RegisterUserRequest(UserCreate):
    role: str = "staff"


class LoginRequest(BaseModel):
    company_slug: str
    email: EmailStr
    password: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_at: datetime


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class ForgotPasswordRequest(BaseModel):
    company_slug: str
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    company_slug: str
    email: EmailStr
    new_password: str = Field(min_length=8)


class LogoutResponse(BaseModel):
    success: bool = True
