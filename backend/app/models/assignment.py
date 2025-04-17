from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)
    due_date = Column(DateTime, nullable=False)
    max_score = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    course = relationship("Course", back_populates="assignments")
    submissions = relationship("AssignmentSubmission", back_populates="assignment")
    grades = relationship("Grade", back_populates="assignment")

class AssignmentSubmission(Base):
    __tablename__ = "assignment_submissions"

    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignment.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("student.id"), nullable=False)
    submission_date = Column(DateTime, nullable=False)
    content = Column(Text)
    file_path = Column(String)
    marks_obtained = Column(Float)
    feedback = Column(Text)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    assignment = relationship("Assignment", back_populates="submissions")
    student = relationship("Student", back_populates="submissions")
    grade = relationship("Grade", back_populates="submission", uselist=False)
    attachments = relationship("SubmissionAttachment", back_populates="submission") 