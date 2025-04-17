from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.organization import Organization
from app.core.tenant import set_tenant_context, clear_tenant_context

class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip tenant resolution for certain paths
        if self._should_skip_tenant_resolution(request.url.path):
            return await call_next(request)
        
        # Get tenant from request
        tenant_id = self._get_tenant_id(request)
        if not tenant_id:
            return await call_next(request)
        
        # Validate tenant exists
        db = SessionLocal()
        try:
            tenant = db.query(Organization).filter(Organization.id == tenant_id).first()
            if not tenant or not tenant.is_active:
                raise HTTPException(status_code=404, detail="Organization not found or inactive")
            
            # Set tenant context
            set_tenant_context(tenant_id)
            
            # Process request
            response = await call_next(request)
            
            return response
        finally:
            # Clear tenant context
            clear_tenant_context()
            db.close()
    
    def _should_skip_tenant_resolution(self, path: str) -> bool:
        """Check if tenant resolution should be skipped for this path."""
        skip_paths = [
            "/docs",
            "/redoc",
            "/openapi.json",
            "/health",
            "/auth/login",
            "/auth/register",
            "/organizations"
        ]
        return any(path.startswith(skip_path) for skip_path in skip_paths)
    
    def _get_tenant_id(self, request: Request) -> int:
        """Extract tenant ID from request."""
        # Try to get from header
        tenant_id = request.headers.get("X-Tenant-ID")
        if tenant_id:
            return int(tenant_id)
        
        # Try to get from subdomain
        host = request.headers.get("host", "")
        if "." in host:
            subdomain = host.split(".")[0]
            # In a real implementation, you would look up the tenant by subdomain
            # For now, we'll just return None
            return None
        
        # Try to get from query parameter (for development/testing)
        tenant_id = request.query_params.get("tenant_id")
        if tenant_id:
            return int(tenant_id)
        
        return None 