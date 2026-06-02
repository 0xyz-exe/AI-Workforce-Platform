"""initial schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-06-02 00:00:00.000000
"""

from __future__ import annotations

from alembic import op
from sqlalchemy import text

from app.db.base import Base
from app.models import entities  # noqa: F401

# revision identifiers, used by Alembic.
revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None

TENANT_TABLES = [
    "users",
    "subscriptions",
    "company_agents",
    "knowledge_bases",
    "documents",
    "chat_sessions",
    "messages",
    "tasks",
    "activity_logs",
    "billing_records",
]


def upgrade() -> None:
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)
    for table_name in TENANT_TABLES:
        op.execute(text(f'ALTER TABLE "{table_name}" ENABLE ROW LEVEL SECURITY'))
        op.execute(
            text(
                f'CREATE POLICY "tenant_isolation_{table_name}" ON "{table_name}" '
                'USING (company_id = current_setting(\'app.current_company_id\', true)::int)'
            )
        )


def downgrade() -> None:
    bind = op.get_bind()
    for table_name in TENANT_TABLES:
        op.execute(text(f'DROP POLICY IF EXISTS "tenant_isolation_{table_name}" ON "{table_name}"'))
    Base.metadata.drop_all(bind=bind)
