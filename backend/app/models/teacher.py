from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    teacher_id = Column(String, unique=True, index=True, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    department = Column(String, nullable=False)
    qualification = Column(String, nullable=False)
    joining_date = Column(Date, nullable=False)

    # Relationships
    user = relationship("User", back_populates="teacher_profile")
    courses = relationship("Course", back_populates="teacher")
    assignments = relationship("Assignment", back_populates="teacher")
    attendance_records = relationship("Attendance", back_populates="teacher")
    grades = relationship("Grade", back_populates="teacher") 