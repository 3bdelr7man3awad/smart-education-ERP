from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.services.notification_service import (
    notification_service,
    Notification,
    NotificationType,
    NotificationPriority,
    NotificationChannel
)
from app.core.auth import get_current_user
from pydantic import BaseModel, EmailStr
from app.api import deps
from app.schemas.notification import (
    NotificationCreate,
    NotificationUpdate,
    NotificationResponse,
    NotificationStatus
)
from app.services.notification_service import NotificationService

router = APIRouter()

class NotificationRequest(BaseModel):
    recipient_id: int
    recipient_email: EmailStr
    template_name: str
    notification_type: NotificationType
    priority: NotificationPriority
    channels: List[NotificationChannel]
    data: dict
    scheduled_for: Optional[datetime] = None

class NotificationResponse(BaseModel):
    id: int
    recipient_id: int
    recipient_email: EmailStr
    notification_type: NotificationType
    priority: NotificationPriority
    template: dict
    data: dict
    channels: List[NotificationChannel]
    scheduled_for: Optional[datetime]
    created_at: datetime
    status: str

@router.post("/", response_model=NotificationResponse)
def create_notification(
    *,
    db: Session = Depends(deps.get_db),
    notification_in: NotificationCreate,
    current_user_id: int = Depends(deps.get_current_user_id)
):
    """
    Create a new notification.
    """
    notification = NotificationService.create_notification(
        db=db,
        notification_in=notification_in
    )
    return notification

@router.get("/", response_model=List[NotificationResponse])
def get_notifications(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    unread_only: bool = Query(False),
    current_user_id: int = Depends(deps.get_current_user_id)
):
    """
    Get notifications for the current user.
    """
    notifications = NotificationService.get_user_notifications(
        db=db,
        user_id=current_user_id,
        skip=skip,
        limit=limit,
        unread_only=unread_only
    )
    return notifications

@router.get("/{notification_id}", response_model=NotificationResponse)
def get_notification(
    *,
    db: Session = Depends(deps.get_db),
    notification_id: int,
    current_user_id: int = Depends(deps.get_current_user_id)
):
    """
    Get a specific notification by ID.
    """
    notification = NotificationService.get_notification(
        db=db,
        notification_id=notification_id
    )
    if not notification or notification.user_id != current_user_id:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@router.put("/{notification_id}", response_model=NotificationResponse)
def update_notification(
    *,
    db: Session = Depends(deps.get_db),
    notification_id: int,
    notification_in: NotificationUpdate,
    current_user_id: int = Depends(deps.get_current_user_id)
):
    """
    Update a notification.
    """
    notification = NotificationService.get_notification(
        db=db,
        notification_id=notification_id
    )
    if not notification or notification.user_id != current_user_id:
        raise HTTPException(status_code=404, detail="Notification not found")
    notification = NotificationService.update_notification(
        db=db,
        notification_id=notification_id,
        notification_in=notification_in
    )
    return notification

@router.post("/{notification_id}/mark-read", response_model=NotificationResponse)
def mark_notification_as_read(
    *,
    db: Session = Depends(deps.get_db),
    notification_id: int,
    current_user_id: int = Depends(deps.get_current_user_id)
):
    """
    Mark a notification as read.
    """
    notification = NotificationService.get_notification(
        db=db,
        notification_id=notification_id
    )
    if not notification or notification.user_id != current_user_id:
        raise HTTPException(status_code=404, detail="Notification not found")
    notification = NotificationService.mark_as_read(
        db=db,
        notification_id=notification_id
    )
    return notification

@router.delete("/{notification_id}")
def delete_notification(
    *,
    db: Session = Depends(deps.get_db),
    notification_id: int,
    current_user_id: int = Depends(deps.get_current_user_id)
):
    """
    Delete a notification.
    """
    notification = NotificationService.get_notification(
        db=db,
        notification_id=notification_id
    )
    if not notification or notification.user_id != current_user_id:
        raise HTTPException(status_code=404, detail="Notification not found")
    NotificationService.delete_notification(
        db=db,
        notification_id=notification_id
    )
    return {"message": "Notification deleted successfully"}

@router.get("/templates", response_model=List[str])
async def get_notification_templates(current_user: dict = Depends(get_current_user)):
    """Get list of available notification templates."""
    return list(notification_service.email_templates.keys())

@router.get("/status/{notification_id}", response_model=NotificationResponse)
async def get_notification_status(
    notification_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Get the status of a specific notification."""
    # TODO: Implement database integration
    raise HTTPException(status_code=501, detail="Not implemented yet") 