from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    student_id = Column(String, unique=True, index=True, nullable=False)
    date_of_birth = Column(Date)
    grade_level = Column(Integer)
    section = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("parents.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="student")
    parent = relationship("Parent", back_populates="children")
    courses = relationship("Course", secondary="student_course", back_populates="students")
    assignments = relationship("Assignment", back_populates="student")
    grades = relationship("Grade", back_populates="student")
    attendance = relationship("Attendance", back_populates="student")
    enrollments = relationship("Enrollment", back_populates="student")
    assignments_submitted = relationship("AssignmentSubmission", back_populates="student")
    attendance_records = relationship("Attendance", back_populates="student") 