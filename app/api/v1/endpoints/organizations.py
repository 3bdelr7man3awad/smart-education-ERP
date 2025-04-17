from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.organization import (
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationResponse
)
from app.services.organization_service import OrganizationService

router = APIRouter()

@router.post("/", response_model=OrganizationResponse)
def create_organization(
    *,
    db: Session = Depends(deps.get_db),
    organization_in: OrganizationCreate,
    current_user = Depends(deps.get_current_active_superuser)
):
    """
    Create a new organization.
    """
    organization = OrganizationService.create_organization(
        db=db,
        organization_in=organization_in
    )
    return organization

@router.get("/", response_model=List[OrganizationResponse])
def get_organizations(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    active_only: bool = Query(False),
    current_user = Depends(deps.get_current_active_superuser)
):
    """
    Get all organizations.
    """
    organizations = OrganizationService.get_organizations(
        db=db,
        skip=skip,
        limit=limit,
        active_only=active_only
    )
    return organizations

@router.get("/{organization_id}", response_model=OrganizationResponse)
def get_organization(
    *,
    db: Session = Depends(deps.get_db),
    organization_id: int,
    current_user = Depends(deps.get_current_active_superuser)
):
    """
    Get a specific organization by ID.
    """
    organization = OrganizationService.get_organization(
        db=db,
        organization_id=organization_id
    )
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization

@router.put("/{organization_id}", response_model=OrganizationResponse)
def update_organization(
    *,
    db: Session = Depends(deps.get_db),
    organization_id: int,
    organization_in: OrganizationUpdate,
    current_user = Depends(deps.get_current_active_superuser)
):
    """
    Update an organization.
    """
    organization = OrganizationService.update_organization(
        db=db,
        organization_id=organization_id,
        organization_in=organization_in
    )
    return organization

@router.delete("/{organization_id}")
def delete_organization(
    *,
    db: Session = Depends(deps.get_db),
    organization_id: int,
    current_user = Depends(deps.get_current_active_superuser)
):
    """
    Delete an organization.
    """
    OrganizationService.delete_organization(
        db=db,
        organization_id=organization_id
    )
    return {"message": "Organization deleted successfully"} 