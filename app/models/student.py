from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    student_id = Column(String(50), nullable=False)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String)
    address = Column(String)
    phone_number = Column(String)
    enrollment_date = Column(Date, nullable=True)
    graduation_date = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True)
    current_grade = Column(String)
    gpa = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="student")
    enrollments = relationship("Enrollment", back_populates="student")
    grades = relationship("Grade", back_populates="student")
    attendance = relationship("Attendance", back_populates="student") 