from typing import List, Optional, Union, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate
from app.core.tenant import get_tenant_id

class StudentService:
    @staticmethod
    def get_student(db: Session, student_id: int) -> Optional[Student]:
        """
        Get a student by ID.
        """
        tenant_id = get_tenant_id()
        query = db.query(Student).filter(Student.id == student_id)
        
        # If tenant context is set, filter by tenant
        if tenant_id:
            query = query.filter(Student.organization_id == tenant_id)
            
        return query.first()

    @staticmethod
    def get_student_by_user_id(db: Session, user_id: int) -> Optional[Student]:
        """
        Get a student by user ID.
        """
        tenant_id = get_tenant_id()
        query = db.query(Student).filter(Student.user_id == user_id)
        
        # If tenant context is set, filter by tenant
        if tenant_id:
            query = query.filter(Student.organization_id == tenant_id)
            
        return query.first()

    @staticmethod
    def get_student_by_student_id(db: Session, student_id: str) -> Optional[Student]:
        """
        Get a student by student ID.
        """
        tenant_id = get_tenant_id()
        query = db.query(Student).filter(Student.student_id == student_id)
        
        # If tenant context is set, filter by tenant
        if tenant_id:
            query = query.filter(Student.organization_id == tenant_id)
            
        return query.first()

    @staticmethod
    def get_students(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = False
    ) -> List[Student]:
        """
        Get all students.
        """
        tenant_id = get_tenant_id()
        query = db.query(Student)
        
        # If tenant context is set, filter by tenant
        if tenant_id:
            query = query.filter(Student.organization_id == tenant_id)
            
        if active_only:
            query = query.filter(Student.is_active == True)
            
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def create_student(db: Session, student_in: StudentCreate) -> Student:
        """
        Create a new student.
        """
        # Check if student with same student ID already exists
        existing_student = StudentService.get_student_by_student_id(db, student_id=student_in.student_id)
        if existing_student:
            raise HTTPException(
                status_code=400,
                detail="Student with this ID already exists"
            )
        
        # Get tenant ID from context
        tenant_id = get_tenant_id()
        
        # Create student
        student = Student(
            user_id=student_in.user_id,
            student_id=student_in.student_id,
            date_of_birth=student_in.date_of_birth,
            gender=student_in.gender,
            address=student_in.address,
            phone_number=student_in.phone_number,
            enrollment_date=student_in.enrollment_date,
            graduation_date=student_in.graduation_date,
            current_grade=student_in.current_grade,
            gpa=student_in.gpa,
            organization_id=tenant_id or student_in.organization_id
        )
        db.add(student)
        db.commit()
        db.refresh(student)
        return student

    @staticmethod
    def update_student(
        db: Session,
        student_id: int,
        student_in: Union[StudentUpdate, Dict[str, Any]]
    ) -> Student:
        """
        Update a student.
        """
        student = StudentService.get_student(db, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        update_data = student_in.dict(exclude_unset=True) if isinstance(student_in, StudentUpdate) else student_in
        
        # Don't allow changing organization_id if tenant context is set
        tenant_id = get_tenant_id()
        if tenant_id and "organization_id" in update_data:
            del update_data["organization_id"]
        
        for field, value in update_data.items():
            setattr(student, field, value)
        
        db.commit()
        db.refresh(student)
        return student

    @staticmethod
    def delete_student(db: Session, student_id: int) -> None:
        """
        Delete a student.
        """
        student = StudentService.get_student(db, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        db.delete(student)
        db.commit() 