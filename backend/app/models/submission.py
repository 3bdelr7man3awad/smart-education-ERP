from sqlalchemy import Column, Text, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from datetime import datetime

class Submission(BaseModel):
    __tablename__ = "submissions"

    assignment_id = Column(ForeignKey("assignments.id"), nullable=False)
    student_id = Column(ForeignKey("users.id"), nullable=False)
    content = Column(Text)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    grade = Column(Integer)
    feedback = Column(Text)
    
    # Relationships
    assignment = relationship("Assignment", back_populates="submissions")
    student = relationship("User", back_populates="submissions") 