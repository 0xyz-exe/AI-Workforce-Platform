from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Index, Integer, JSON, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, CompanyScopedMixin, IDMixin, TimestampMixin


class Company(Base, IDMixin, TimestampMixin):
    __tablename__ = "companies"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    legal_name: Mapped[Optional[str]] = mapped_column(String(255))
    industry: Mapped[Optional[str]] = mapped_column(String(120))
    size: Mapped[Optional[str]] = mapped_column(String(60))
    status: Mapped[str] = mapped_column(String(50), default="active", nullable=False)

    users = relationship("User", back_populates="company", cascade="all, delete-orphan")
    subscriptions = relationship("Subscription", back_populates="company", cascade="all, delete-orphan")
    company_agents = relationship("CompanyAgent", back_populates="company", cascade="all, delete-orphan")
    knowledge_bases = relationship("KnowledgeBase", back_populates="company", cascade="all, delete-orphan")


class Plan(Base, IDMixin, TimestampMixin):
    __tablename__ = "plans"

    code: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    price_monthly_cents: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    max_users: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    max_agents: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    features: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    subscriptions = relationship("Subscription", back_populates="plan")


class Subscription(Base, IDMixin, TimestampMixin):
    __tablename__ = "subscriptions"

    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    plan_id: Mapped[int] = mapped_column(ForeignKey("plans.id"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), default="trialing", nullable=False)
    stripe_customer_id: Mapped[Optional[str]] = mapped_column(String(120), unique=True)
    stripe_subscription_id: Mapped[Optional[str]] = mapped_column(String(120), unique=True)
    current_period_start: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    current_period_end: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    company = relationship("Company", back_populates="subscriptions")
    plan = relationship("Plan", back_populates="subscriptions")
    billing_records = relationship("BillingRecord", back_populates="subscription", cascade="all, delete-orphan")


class Role(Base, IDMixin, TimestampMixin):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    is_system: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    users = relationship("UserRole", back_populates="role", cascade="all, delete-orphan")
    permissions = relationship("RolePermission", back_populates="role", cascade="all, delete-orphan")


class Permission(Base, IDMixin, TimestampMixin):
    __tablename__ = "permissions"

    code: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)

    roles = relationship("RolePermission", back_populates="permission", cascade="all, delete-orphan")


class User(Base, IDMixin, TimestampMixin):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("company_id", "email", name="uq_users_company_email"),)

    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number: Mapped[Optional[str]] = mapped_column(String(30))
    avatar_url: Mapped[Optional[str]] = mapped_column(String(512))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_owner: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    password_reset_token_hash: Mapped[Optional[str]] = mapped_column(String(255))
    password_reset_expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    company = relationship("Company", back_populates="users")
    roles = relationship("UserRole", back_populates="user", cascade="all, delete-orphan")
    chat_sessions = relationship("ChatSession", back_populates="user")
    tasks = relationship("Task", back_populates="assigned_to")


class UserRole(Base, IDMixin, TimestampMixin):
    __tablename__ = "user_roles"
    __table_args__ = (UniqueConstraint("user_id", "role_id", name="uq_user_roles_user_role"),)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="users")


class RolePermission(Base, IDMixin, TimestampMixin):
    __tablename__ = "role_permissions"
    __table_args__ = (UniqueConstraint("role_id", "permission_id", name="uq_role_permissions_role_permission"),)

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    permission_id: Mapped[int] = mapped_column(ForeignKey("permissions.id", ondelete="CASCADE"), nullable=False)

    role = relationship("Role", back_populates="permissions")
    permission = relationship("Permission", back_populates="roles")


class Agent(Base, IDMixin, TimestampMixin):
    __tablename__ = "agents"

    code: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    category: Mapped[str] = mapped_column(String(80), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    prompt_template: Mapped[str] = mapped_column(Text, nullable=False)
    system_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    default_model: Mapped[str] = mapped_column(String(80), nullable=False, default="gpt-4o-mini")
    is_marketplace: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    metadata_json: Mapped[dict] = mapped_column("metadata", JSON, default=dict, nullable=False)

    company_agents = relationship("CompanyAgent", back_populates="agent", cascade="all, delete-orphan")
    chat_sessions = relationship("ChatSession", back_populates="agent")
    tasks = relationship("Task", back_populates="agent")


class CompanyAgent(Base, IDMixin, CompanyScopedMixin, TimestampMixin):
    __tablename__ = "company_agents"
    __table_args__ = (UniqueConstraint("company_id", "agent_id", name="uq_company_agents_company_agent"),)

    agent_id: Mapped[int] = mapped_column(ForeignKey("agents.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="enabled", nullable=False)
    enabled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now())
    disabled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    usage_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    config_json: Mapped[dict] = mapped_column("config", JSON, default=dict, nullable=False)

    company = relationship("Company", back_populates="company_agents")
    agent = relationship("Agent", back_populates="company_agents")


class KnowledgeBase(Base, IDMixin, CompanyScopedMixin, TimestampMixin):
    __tablename__ = "knowledge_bases"

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    indexing_status: Mapped[str] = mapped_column(String(50), default="ready", nullable=False)

    company = relationship("Company", back_populates="knowledge_bases")
    documents = relationship("Document", back_populates="knowledge_base", cascade="all, delete-orphan")
    chat_sessions = relationship("ChatSession", back_populates="knowledge_base")


class Document(Base, IDMixin, CompanyScopedMixin, TimestampMixin):
    __tablename__ = "documents"

    knowledge_base_id: Mapped[int] = mapped_column(ForeignKey("knowledge_bases.id", ondelete="CASCADE"), nullable=False)
    uploaded_by_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(120), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    s3_key: Mapped[str] = mapped_column(String(512), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="uploaded", nullable=False)
    page_count: Mapped[Optional[int]] = mapped_column(Integer)
    chunk_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    metadata_json: Mapped[dict] = mapped_column("metadata", JSON, default=dict, nullable=False)

    knowledge_base = relationship("KnowledgeBase", back_populates="documents")
    uploaded_by = relationship("User")


class ChatSession(Base, IDMixin, CompanyScopedMixin, TimestampMixin):
    __tablename__ = "chat_sessions"

    agent_id: Mapped[int] = mapped_column(ForeignKey("agents.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    knowledge_base_id: Mapped[Optional[int]] = mapped_column(ForeignKey("knowledge_bases.id", ondelete="SET NULL"))
    title: Mapped[str] = mapped_column(String(255), nullable=False, default="New chat")
    memory_json: Mapped[dict] = mapped_column("memory", JSON, default=dict, nullable=False)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    agent = relationship("Agent", back_populates="chat_sessions")
    user = relationship("User", back_populates="chat_sessions")
    knowledge_base = relationship("KnowledgeBase", back_populates="chat_sessions")
    messages = relationship("Message", back_populates="chat_session", cascade="all, delete-orphan")


class Message(Base, IDMixin, CompanyScopedMixin, TimestampMixin):
    __tablename__ = "messages"

    chat_session_id: Mapped[int] = mapped_column(ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False)
    sender_role: Mapped[str] = mapped_column(String(30), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    tokens_used: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    metadata_json: Mapped[dict] = mapped_column("metadata", JSON, default=dict, nullable=False)

    chat_session = relationship("ChatSession", back_populates="messages")


class Task(Base, IDMixin, CompanyScopedMixin, TimestampMixin):
    __tablename__ = "tasks"

    agent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agents.id", ondelete="SET NULL"))
    assigned_to_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)
    due_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    metadata_json: Mapped[dict] = mapped_column("metadata", JSON, default=dict, nullable=False)

    agent = relationship("Agent", back_populates="tasks")
    assigned_to = relationship("User", back_populates="tasks")


class ActivityLog(Base, IDMixin, CompanyScopedMixin, TimestampMixin):
    __tablename__ = "activity_logs"

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    action: Mapped[str] = mapped_column(String(120), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(120), nullable=False)
    entity_id: Mapped[Optional[int]] = mapped_column(Integer)
    metadata_json: Mapped[dict] = mapped_column("metadata", JSON, default=dict, nullable=False)


class BillingRecord(Base, IDMixin, CompanyScopedMixin, TimestampMixin):
    __tablename__ = "billing_records"

    subscription_id: Mapped[Optional[int]] = mapped_column(ForeignKey("subscriptions.id", ondelete="SET NULL"))
    amount_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[str] = mapped_column(String(12), default="usd", nullable=False)
    record_type: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)
    invoice_url: Mapped[Optional[str]] = mapped_column(String(512))
    paid_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    metadata_json: Mapped[dict] = mapped_column("metadata", JSON, default=dict, nullable=False)

    subscription = relationship("Subscription", back_populates="billing_records")
