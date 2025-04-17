from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
from datetime import datetime

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    due_date = Column(DateTime, nullable=False)
    total_points = Column(Float, nullable=False, default=100.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    course = relationship("Course", back_populates="assignments")
    submissions = relationship("AssignmentSubmission", back_populates="assignment")
    
class AssignmentSubmission(Base):
    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignment.id"))
    student_id = Column(Integer, ForeignKey("student.id"))
    submission_text = Column(Text)
    submission_file = Column(String)  # File path
    submitted_at = Column(DateTime, default=datetime.utcnow)
    grade = Column(Float)
    feedback = Column(Text)
    
    # Relationships
    assignment = relationship("Assignment", back_populates="submissions")
    student = relationship("Student", back_populates="submissions") 