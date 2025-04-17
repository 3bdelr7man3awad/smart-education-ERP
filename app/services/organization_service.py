from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.organization import Organization
from app.schemas.organization import OrganizationCreate, OrganizationUpdate

class OrganizationService:
    @staticmethod
    def create_organization(db: Session, organization_in: OrganizationCreate) -> Organization:
        """
        Create a new organization.
        """
        # Check if organization with same code already exists
        existing_org = db.query(Organization).filter(
            Organization.code == organization_in.code
        ).first()
        if existing_org:
            raise HTTPException(
                status_code=400,
                detail="Organization with this code already exists"
            )
        
        # Check if organization with same domain already exists
        if organization_in.domain:
            existing_domain = db.query(Organization).filter(
                Organization.domain == organization_in.domain
            ).first()
            if existing_domain:
                raise HTTPException(
                    status_code=400,
                    detail="Organization with this domain already exists"
                )
        
        organization = Organization(
            name=organization_in.name,
            code=organization_in.code,
            domain=organization_in.domain,
            logo_url=organization_in.logo_url,
            settings=organization_in.settings
        )
        db.add(organization)
        db.commit()
        db.refresh(organization)
        return organization

    @staticmethod
    def get_organization(db: Session, organization_id: int) -> Optional[Organization]:
        """
        Get an organization by ID.
        """
        return db.query(Organization).filter(Organization.id == organization_id).first()

    @staticmethod
    def get_organization_by_code(db: Session, code: str) -> Optional[Organization]:
        """
        Get an organization by code.
        """
        return db.query(Organization).filter(Organization.code == code).first()

    @staticmethod
    def get_organization_by_domain(db: Session, domain: str) -> Optional[Organization]:
        """
        Get an organization by domain.
        """
        return db.query(Organization).filter(Organization.domain == domain).first()

    @staticmethod
    def get_organizations(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = False
    ) -> List[Organization]:
        """
        Get all organizations.
        """
        query = db.query(Organization)
        if active_only:
            query = query.filter(Organization.is_active == True)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update_organization(
        db: Session,
        organization_id: int,
        organization_in: OrganizationUpdate
    ) -> Organization:
        """
        Update an organization.
        """
        organization = OrganizationService.get_organization(db, organization_id)
        if not organization:
            raise HTTPException(status_code=404, detail="Organization not found")

        update_data = organization_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(organization, field, value)

        db.commit()
        db.refresh(organization)
        return organization

    @staticmethod
    def delete_organization(db: Session, organization_id: int) -> None:
        """
        Delete an organization.
        """
        organization = OrganizationService.get_organization(db, organization_id)
        if not organization:
            raise HTTPException(status_code=404, detail="Organization not found")

        db.delete(organization)
        db.commit() 