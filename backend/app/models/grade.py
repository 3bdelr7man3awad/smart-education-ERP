from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base

class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)
    assignment_id = Column(Integer, ForeignKey("assignment.id"), nullable=False)
    submission_id = Column(Integer, ForeignKey("assignment_submission.id"), nullable=False)
    score = Column(Float, nullable=False)
    feedback = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    student = relationship("Student", back_populates="grades")
    course = relationship("Course", back_populates="grades")
    assignment = relationship("Assignment", back_populates="grades")
    submission = relationship("AssignmentSubmission", back_populates="grade") 