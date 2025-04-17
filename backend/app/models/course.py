from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base

# Association table for student-course relationship
student_course = Table(
    'student_course',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('student.id'), primary_key=True),
    Column('course_id', Integer, ForeignKey('course.id'), primary_key=True)
)

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    teacher_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    grade_level = Column(Integer, nullable=False)
    section = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    teacher = relationship("User", back_populates="courses")
    students = relationship("Student", secondary=student_course, back_populates="courses")
    enrollments = relationship("Enrollment", back_populates="course")
    assignments = relationship("Assignment", back_populates="course")
    materials = relationship("CourseMaterial", back_populates="course")
    schedule = relationship("CourseSchedule", back_populates="course")
    grades = relationship("Grade", back_populates="course") 