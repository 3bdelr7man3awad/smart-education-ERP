from typing import List, Optional, Union, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.assignment import Assignment
from app.schemas.assignment import AssignmentCreate, AssignmentUpdate
from app.core.tenant import get_tenant_id

class AssignmentService:
    @staticmethod
    def get_assignment(db: Session, assignment_id: int) -> Optional[Assignment]:
        """
        Get an assignment by ID.
        """
        tenant_id = get_tenant_id()
        query = db.query(Assignment).filter(Assignment.id == assignment_id)
        
        # If tenant context is set, filter by tenant
        if tenant_id:
            query = query.filter(Assignment.organization_id == tenant_id)
            
        return query.first()

    @staticmethod
    def get_assignments(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        course_id: Optional[int] = None,
        active_only: bool = False
    ) -> List[Assignment]:
        """
        Get all assignments.
        """
        tenant_id = get_tenant_id()
        query = db.query(Assignment)
        
        # If tenant context is set, filter by tenant
        if tenant_id:
            query = query.filter(Assignment.organization_id == tenant_id)
            
        if course_id:
            query = query.filter(Assignment.course_id == course_id)
            
        if active_only:
            query = query.filter(Assignment.is_active == True)
            
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def create_assignment(db: Session, assignment_in: AssignmentCreate) -> Assignment:
        """
        Create a new assignment.
        """
        # Get tenant ID from context
        tenant_id = get_tenant_id()
        
        # Create assignment
        assignment = Assignment(
            title=assignment_in.title,
            description=assignment_in.description,
            course_id=assignment_in.course_id,
            due_date=assignment_in.due_date,
            total_points=assignment_in.total_points,
            organization_id=tenant_id or assignment_in.organization_id
        )
        db.add(assignment)
        db.commit()
        db.refresh(assignment)
        return assignment

    @staticmethod
    def update_assignment(
        db: Session,
        assignment_id: int,
        assignment_in: Union[AssignmentUpdate, Dict[str, Any]]
    ) -> Assignment:
        """
        Update an assignment.
        """
        assignment = AssignmentService.get_assignment(db, assignment_id)
        if not assignment:
            raise HTTPException(status_code=404, detail="Assignment not found")
        
        update_data = assignment_in.dict(exclude_unset=True) if isinstance(assignment_in, AssignmentUpdate) else assignment_in
        
        # Don't allow changing organization_id if tenant context is set
        tenant_id = get_tenant_id()
        if tenant_id and "organization_id" in update_data:
            del update_data["organization_id"]
        
        for field, value in update_data.items():
            setattr(assignment, field, value)
        
        db.commit()
        db.refresh(assignment)
        return assignment

    @staticmethod
    def delete_assignment(db: Session, assignment_id: int) -> None:
        """
        Delete an assignment.
        """
        assignment = AssignmentService.get_assignment(db, assignment_id)
        if not assignment:
            raise HTTPException(status_code=404, detail="Assignment not found")
        
        db.delete(assignment)
        db.commit() 