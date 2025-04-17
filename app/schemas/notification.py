from typing import List, Optional, Dict, Any
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from enum import Enum

class NotificationType(str, Enum):
    SYSTEM = "system"
    COURSE = "course"
    ASSIGNMENT = "assignment"
    GRADE = "grade"
    ANNOUNCEMENT = "announcement"
    MESSAGE = "message"

class NotificationPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class NotificationStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"

class NotificationChannel(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    IN_APP = "in_app"

class NotificationBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    message: str = Field(..., min_length=1)
    notification_type: NotificationType
    priority: NotificationPriority = NotificationPriority.MEDIUM
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class NotificationCreate(NotificationBase):
    user_id: int

class NotificationUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    message: Optional[str] = Field(None, min_length=1)
    notification_type: Optional[NotificationType] = None
    priority: Optional[NotificationPriority] = None
    metadata: Optional[Dict[str, Any]] = None
    is_read: Optional[bool] = None
    is_delivered: Optional[bool] = None

class NotificationResponse(NotificationBase):
    id: int
    user_id: int
    is_read: bool
    is_delivered: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 