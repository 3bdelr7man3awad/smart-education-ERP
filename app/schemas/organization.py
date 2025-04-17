from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class OrganizationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=50)
    domain: Optional[str] = Field(None, max_length=255)
    logo_url: Optional[str] = Field(None, max_length=255)
    settings: Optional[Dict[str, Any]] = Field(default_factory=dict)

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=50)
    domain: Optional[str] = Field(None, max_length=255)
    logo_url: Optional[str] = Field(None, max_length=255)
    settings: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class OrganizationResponse(OrganizationBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 