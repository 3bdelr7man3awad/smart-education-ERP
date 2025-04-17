from sqlalchemy import Boolean, Column, Integer, String, Enum, DateTime
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import enum
from datetime import datetime

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"
    PARENT = "parent"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="user", uselist=False)
    courses = relationship("Course", back_populates="teacher")
    notifications = relationship("Notification", back_populates="user")
    attendance_records = relationship("Attendance", back_populates="user")
    grades = relationship("Grade", back_populates="user")
    assignments_submitted = relationship("AssignmentSubmission", back_populates="user") 