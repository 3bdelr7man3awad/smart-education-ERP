from contextvars import ContextVar
from typing import Optional

# Context variable to store the current tenant ID
tenant_context: ContextVar[Optional[int]] = ContextVar("tenant_context", default=None)

def set_tenant_context(tenant_id: int) -> None:
    """Set the current tenant ID in the context."""
    tenant_context.set(tenant_id)

def get_tenant_context() -> Optional[int]:
    """Get the current tenant ID from the context."""
    return tenant_context.get()

def clear_tenant_context() -> None:
    """Clear the current tenant ID from the context."""
    tenant_context.set(None)

def get_tenant_id() -> Optional[int]:
    """Get the current tenant ID from the context."""
    return get_tenant_context() 