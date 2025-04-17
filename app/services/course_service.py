from typing import List, Optional, Union, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate
from app.core.tenant import get_tenant_id

class CourseService:
    @staticmethod
    def get_course(db: Session, course_id: int) -> Optional[Course]:
        """
        Get a course by ID.
        """
        tenant_id = get_tenant_id()
        query = db.query(Course).filter(Course.id == course_id)
        
        # If tenant context is set, filter by tenant
        if tenant_id:
            query = query.filter(Course.organization_id == tenant_id)
            
        return query.first()

    @staticmethod
    def get_course_by_code(db: Session, code: str) -> Optional[Course]:
        """
        Get a course by code.
        """
        tenant_id = get_tenant_id()
        query = db.query(Course).filter(Course.code == code)
        
        # If tenant context is set, filter by tenant
        if tenant_id:
            query = query.filter(Course.organization_id == tenant_id)
            
        return query.first()

    @staticmethod
    def get_courses(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        teacher_id: Optional[int] = None,
        active_only: bool = False
    ) -> List[Course]:
        """
        Get all courses.
        """
        tenant_id = get_tenant_id()
        query = db.query(Course)
        
        # If tenant context is set, filter by tenant
        if tenant_id:
            query = query.filter(Course.organization_id == tenant_id)
            
        if teacher_id:
            query = query.filter(Course.teacher_id == teacher_id)
            
        if active_only:
            query = query.filter(Course.is_active == True)
            
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def create_course(db: Session, course_in: CourseCreate) -> Course:
        """
        Create a new course.
        """
        # Check if course with same code already exists
        existing_course = CourseService.get_course_by_code(db, code=course_in.code)
        if existing_course:
            raise HTTPException(
                status_code=400,
                detail="Course with this code already exists"
            )
        
        # Get tenant ID from context
        tenant_id = get_tenant_id()
        
        # Create course
        course = Course(
            title=course_in.title,
            description=course_in.description,
            code=course_in.code,
            teacher_id=course_in.teacher_id,
            organization_id=tenant_id or course_in.organization_id
        )
        db.add(course)
        db.commit()
        db.refresh(course)
        return course

    @staticmethod
    def update_course(
        db: Session,
        course_id: int,
        course_in: Union[CourseUpdate, Dict[str, Any]]
    ) -> Course:
        """
        Update a course.
        """
        course = CourseService.get_course(db, course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        
        update_data = course_in.dict(exclude_unset=True) if isinstance(course_in, CourseUpdate) else course_in
        
        # Don't allow changing organization_id if tenant context is set
        tenant_id = get_tenant_id()
        if tenant_id and "organization_id" in update_data:
            del update_data["organization_id"]
        
        for field, value in update_data.items():
            setattr(course, field, value)
        
        db.commit()
        db.refresh(course)
        return course

    @staticmethod
    def delete_course(db: Session, course_id: int) -> None:
        """
        Delete a course.
        """
        course = CourseService.get_course(db, course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        
        db.delete(course)
        db.commit() 