from fastapi import BackgroundTasks
from typing import List, Dict, Optional, Union, Any
from pydantic import BaseModel, EmailStr
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
import json
import aiohttp
import asyncio
from enum import Enum
from sqlalchemy.orm import Session
from app.models.notification import Notification, NotificationStatus
import requests
from fastapi import HTTPException

from app.schemas.notification import (
    NotificationCreate,
    NotificationResponse,
    NotificationType,
    NotificationUpdate
)
from app.core.email import send_email
from app.core.sms import send_sms
from app.core.push import send_push_notification
from app.core.tenant import get_tenant_id

class NotificationType(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    IN_APP = "in_app"

class NotificationPriority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class NotificationChannel(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    IN_APP = "in_app"

class NotificationTemplate(BaseModel):
    subject: str
    body: str
    html_body: Optional[str] = None

class Notification(BaseModel):
    recipient_id: int
    recipient_email: EmailStr
    notification_type: NotificationType
    priority: NotificationPriority
    template: NotificationTemplate
    data: Dict = {}
    channels: List[NotificationChannel]
    scheduled_for: Optional[datetime] = None
    created_at: datetime = datetime.utcnow()

class NotificationService:
    def __init__(self, db: Session):
        self.db = db
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load notification templates from configuration."""
        return {
            "welcome": {
                "subject": "Welcome to Smart Education ERP",
                "body": "Welcome {name}! We're excited to have you on board.",
                "channels": [NotificationChannel.EMAIL]
            },
            "password_reset": {
                "subject": "Password Reset Request",
                "body": "Click here to reset your password: {reset_link}",
                "channels": [NotificationChannel.EMAIL]
            },
            "assignment_due": {
                "subject": "Assignment Due Soon",
                "body": "Your assignment '{assignment_name}' is due on {due_date}",
                "channels": [NotificationChannel.EMAIL, NotificationChannel.IN_APP]
            }
        }

    @staticmethod
    def create_notification(db: Session, notification_in: NotificationCreate) -> Notification:
        """
        Create a new notification.
        """
        # Get tenant ID from context
        tenant_id = get_tenant_id()
        
        # Create notification
        notification = Notification(
            user_id=notification_in.user_id,
            title=notification_in.title,
            message=notification_in.message,
            notification_type=notification_in.notification_type,
            priority=notification_in.priority,
            metadata=notification_in.metadata,
            organization_id=tenant_id or notification_in.organization_id
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification

    @staticmethod
    def get_notification(db: Session, notification_id: int) -> Optional[Notification]:
        """
        Get a notification by ID.
        """
        tenant_id = get_tenant_id()
        query = db.query(Notification).filter(Notification.id == notification_id)
        
        # If tenant context is set, filter by tenant
        if tenant_id:
            query = query.filter(Notification.organization_id == tenant_id)
            
        return query.first()

    @staticmethod
    def get_user_notifications(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 10,
        unread_only: bool = False
    ) -> List[Notification]:
        """
        Get notifications for a specific user.
        """
        tenant_id = get_tenant_id()
        query = db.query(Notification).filter(Notification.user_id == user_id)
        
        # If tenant context is set, filter by tenant
        if tenant_id:
            query = query.filter(Notification.organization_id == tenant_id)
            
        if unread_only:
            query = query.filter(Notification.is_read == False)
            
        return query.order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def update_notification(
        db: Session,
        notification_id: int,
        notification_in: NotificationUpdate
    ) -> Notification:
        """
        Update a notification.
        """
        notification = NotificationService.get_notification(db, notification_id)
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")

        update_data = notification_in.dict(exclude_unset=True)
        
        # Don't allow changing organization_id if tenant context is set
        tenant_id = get_tenant_id()
        if tenant_id and "organization_id" in update_data:
            del update_data["organization_id"]
            
        for field, value in update_data.items():
            setattr(notification, field, value)

        db.commit()
        db.refresh(notification)
        return notification

    @staticmethod
    def mark_as_read(db: Session, notification_id: int) -> Notification:
        """
        Mark a notification as read.
        """
        notification = NotificationService.get_notification(db, notification_id)
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")

        notification.is_read = True
        db.commit()
        db.refresh(notification)
        return notification

    @staticmethod
    def mark_as_delivered(db: Session, notification_id: int) -> Notification:
        """
        Mark a notification as delivered.
        """
        notification = NotificationService.get_notification(db, notification_id)
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")

        notification.is_delivered = True
        db.commit()
        db.refresh(notification)
        return notification

    @staticmethod
    def delete_notification(db: Session, notification_id: int) -> None:
        """
        Delete a notification.
        """
        notification = NotificationService.get_notification(db, notification_id)
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")

        db.delete(notification)
        db.commit()

    async def send_notification(self, notification_id: int) -> NotificationResponse:
        notification = await self.get_notification(self.db, notification_id)
        
        if notification.status != NotificationStatus.PENDING:
            raise HTTPException(
                status_code=400,
                detail="Notification is not in pending status"
            )

        try:
            for channel in notification.channels:
                if channel == "email":
                    await send_email(
                        notification.recipient_email,
                        notification.title,
                        notification.message
                    )
                elif channel == "sms":
                    await send_sms(
                        notification.recipient_email,
                        notification.message
                    )
                elif channel == "push":
                    await send_push_notification(
                        notification.recipient_id,
                        notification.title,
                        notification.message
                    )

            notification.status = NotificationStatus.SENT
            notification.sent_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(notification)
            return notification

        except Exception as e:
            notification.status = NotificationStatus.FAILED
            self.db.commit()
            raise HTTPException(
                status_code=500,
                detail=f"Failed to send notification: {str(e)}"
            )

    def create_notification(
        self,
        recipient_id: int,
        recipient_email: str,
        notification_type: NotificationType,
        template_name: str,
        template_data: Dict[str, Any],
        priority: NotificationPriority = NotificationPriority.MEDIUM,
        channels: List[NotificationChannel] = None,
        scheduled_for: Optional[datetime] = None
    ) -> Notification:
        """Create a new notification."""
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found")

        if channels is None:
            channels = self.templates[template_name]["channels"]

        notification = Notification(
            recipient_id=recipient_id,
            recipient_email=recipient_email,
            notification_type=notification_type,
            template_name=template_name,
            template_data=template_data,
            priority=priority,
            channels=channels,
            data=self.templates[template_name],
            scheduled_for=scheduled_for,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            status=NotificationStatus.SCHEDULED if scheduled_for else NotificationStatus.PENDING
        )

        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification

    def send_notification(self, notification_id: int) -> bool:
        """Send a notification through all specified channels."""
        notification = self.db.query(Notification).filter(Notification.id == notification_id).first()
        if not notification:
            return False

        try:
            for channel in notification.channels:
                if channel == NotificationChannel.EMAIL:
                    self._send_email(notification)
                elif channel == NotificationChannel.SMS:
                    self._send_sms(notification)
                elif channel == NotificationChannel.PUSH:
                    self._send_push(notification)
                elif channel == NotificationChannel.IN_APP:
                    self._send_in_app(notification)

            notification.status = NotificationStatus.SENT
            notification.updated_at = datetime.utcnow()
            self.db.commit()
            return True

        except Exception as e:
            notification.status = NotificationStatus.FAILED
            notification.error_message = str(e)
            notification.updated_at = datetime.utcnow()
            self.db.commit()
            return False

    def _send_email(self, notification: Notification) -> None:
        """Send email notification."""
        msg = MIMEMultipart()
        msg["From"] = settings.SMTP_USER
        msg["To"] = notification.recipient_email
        msg["Subject"] = notification.data["subject"].format(**notification.template_data)

        body = notification.data["body"].format(**notification.template_data)
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)

    def _send_sms(self, notification: Notification) -> None:
        """Send SMS notification using a third-party service."""
        # Implement SMS sending logic here
        pass

    def _send_push(self, notification: Notification) -> None:
        """Send push notification."""
        # Implement push notification logic here
        pass

    def _send_in_app(self, notification: Notification) -> None:
        """Send in-app notification."""
        # Implement in-app notification logic here
        pass

    def get_notification_status(self, notification_id: int) -> Optional[Dict[str, Any]]:
        """Get the status of a notification."""
        notification = self.db.query(Notification).filter(Notification.id == notification_id).first()
        if not notification:
            return None

        return {
            "id": notification.id,
            "status": notification.status,
            "error_message": notification.error_message,
            "created_at": notification.created_at,
            "updated_at": notification.updated_at
        }

    def get_user_notifications(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[NotificationStatus] = None
    ) -> List[Notification]:
        """Get notifications for a specific user."""
        query = self.db.query(Notification).filter(Notification.recipient_id == user_id)
        
        if status:
            query = query.filter(Notification.status == status)
        
        return query.order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()

notification_service = NotificationService() 