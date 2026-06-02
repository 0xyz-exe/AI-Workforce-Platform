from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.entities import Agent, Permission, Plan, Role, RolePermission


DEFAULT_PLANS = [
    {
        "code": "starter",
        "name": "Starter",
        "description": "For early teams that need one agent and a few users.",
        "price_monthly_cents": 4900,
        "max_users": 5,
        "max_agents": 1,
        "features": {"agents": ["Sales Agent"], "analytics": True, "rag": True},
    },
    {
        "code": "business",
        "name": "Business",
        "description": "For growing teams running multiple agent workflows.",
        "price_monthly_cents": 14900,
        "max_users": 20,
        "max_agents": 3,
        "features": {"agents": ["Sales Agent", "HR Agent", "Customer Support Agent"], "analytics": True, "rag": True},
    },
    {
        "code": "enterprise",
        "name": "Enterprise",
        "description": "Unlimited scaling with custom governance and SLAs.",
        "price_monthly_cents": 49900,
        "max_users": 0,
        "max_agents": 0,
        "features": {"agents": "unlimited", "analytics": True, "rag": True, "sso": True},
    },
]

DEFAULT_PERMISSIONS = [
    ("manage_users", "Manage users"),
    ("manage_agents", "Manage agents"),
    ("manage_billing", "Manage billing"),
    ("manage_documents", "Manage documents"),
    ("view_analytics", "View analytics"),
]

ROLE_PERMISSION_MATRIX = {
    "Owner": {"manage_users", "manage_agents", "manage_billing", "manage_documents", "view_analytics"},
    "Admin": {"manage_users", "manage_agents", "manage_documents", "view_analytics"},
    "Manager": {"manage_agents", "manage_documents", "view_analytics"},
    "Staff": {"view_analytics"},
}

DEFAULT_AGENTS = [
    {
        "code": "sales-agent",
        "name": "Sales Agent",
        "category": "sales",
        "description": "Qualifies leads and generates sales collateral.",
        "prompt_template": "Act as a sales assistant and answer using the company's ICP and lead data.",
        "system_prompt": "You are a sales agent that helps qualify leads and write outbound messaging.",
    },
    {
        "code": "hr-agent",
        "name": "HR Agent",
        "category": "hr",
        "description": "Screens resumes and generates interview questions.",
        "prompt_template": "Review the candidate profile and return fit, missing skills, and interview questions.",
        "system_prompt": "You are an HR assistant that helps with hiring workflows.",
    },
    {
        "code": "finance-agent",
        "name": "Finance Agent",
        "category": "finance",
        "description": "Categorizes expenses and summarizes financials.",
        "prompt_template": "Analyze the finance data and produce a concise actionable summary.",
        "system_prompt": "You are a finance assistant focused on invoices, expenses, and reporting.",
    },
    {
        "code": "marketing-agent",
        "name": "Marketing Agent",
        "category": "marketing",
        "description": "Creates content and campaign planning.",
        "prompt_template": "Generate platform-specific marketing content with a strong brand tone.",
        "system_prompt": "You are a marketing strategist and content creator.",
    },
    {
        "code": "support-agent",
        "name": "Customer Support Agent",
        "category": "support",
        "description": "Answers support questions using company knowledge.",
        "prompt_template": "Use the retrieved knowledge base context to answer clearly and cite sources.",
        "system_prompt": "You are a customer support assistant with RAG access to company knowledge.",
    },
]


def seed_reference_data(session: Session) -> None:
    for plan_data in DEFAULT_PLANS:
        exists = session.scalar(select(Plan).where(Plan.code == plan_data["code"]))
        if exists is None:
            session.add(Plan(**plan_data))

    for code, name in DEFAULT_PERMISSIONS:
        exists = session.scalar(select(Permission).where(Permission.code == code))
        if exists is None:
            session.add(Permission(code=code, name=name))

    role_lookup: dict[str, Role] = {}
    for role_name in ROLE_PERMISSION_MATRIX:
        role = session.scalar(select(Role).where(Role.name == role_name))
        if role is None:
            role = Role(name=role_name, description=f"Built-in {role_name.lower()} role", is_system=True)
            session.add(role)
            session.flush()
        role_lookup[role_name] = role

    permission_lookup = {permission.code: permission for permission in session.scalars(select(Permission)).all()}
    for role_name, permission_codes in ROLE_PERMISSION_MATRIX.items():
        role = role_lookup[role_name]
        existing_codes = {link.permission.code for link in role.permissions}
        for permission_code in permission_codes:
            if permission_code in existing_codes:
                continue
            session.add(RolePermission(role_id=role.id, permission_id=permission_lookup[permission_code].id))

    for agent_data in DEFAULT_AGENTS:
        exists = session.scalar(select(Agent).where(Agent.code == agent_data["code"]))
        if exists is None:
            session.add(
                Agent(
                    metadata_json={"version": 1, "owner": "platform"},
                    default_model="gpt-4o-mini",
                    is_marketplace=True,
                    is_active=True,
                    **agent_data,
                )
            )