from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.base_class import Base

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(String, nullable=False)
    notification_type = Column(String(50), nullable=False)
    priority = Column(String(20), nullable=False, default="medium")
    metadata = Column(JSON, nullable=True)
    is_read = Column(Boolean, default=False)
    is_delivered = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 