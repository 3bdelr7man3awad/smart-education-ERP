from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.base_class import Base

class AttendanceStatus(str, enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    EXCUSED = "excused"

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    status = Column(Enum(AttendanceStatus), nullable=False)
    remarks = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    student = relationship("Student", back_populates="attendance_records")
    user = relationship("User", back_populates="attendance_records")
    teacher = relationship("Teacher", back_populates="attendance_records")
    course = relationship("Course", back_populates="attendance_records") 