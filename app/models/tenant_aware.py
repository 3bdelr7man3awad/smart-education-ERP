from sqlalchemy import Column, Integer, ForeignKey
from app.db.base_class import Base

class TenantAwareModel(Base):
    """Base model for all tenant-aware models."""
    
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    
    @classmethod
    def get_tenant_filter(cls, tenant_id):
        """Get the filter for the current tenant."""
        return cls.organization_id == tenant_id 