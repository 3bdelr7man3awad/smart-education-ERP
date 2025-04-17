from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api import deps
from app.services.notification_service import NotificationService, NotificationType, NotificationPriority, NotificationChannel
from app.schemas.notification import NotificationCreate, NotificationResponse, NotificationStatus
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=NotificationResponse)
def create_notification(
    notification: NotificationCreate,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
):
    """Create a new notification."""
    notification_service = NotificationService(db)
    try:
        created_notification = notification_service.create_notification(
            recipient_id=notification.recipient_id,
            recipient_email=notification.recipient_email,
            notification_type=notification.notification_type,
            template_name=notification.template_name,
            template_data=notification.template_data,
            priority=notification.priority,
            channels=notification.channels,
            scheduled_for=notification.scheduled_for
        )
        return created_notification
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{notification_id}", response_model=NotificationResponse)
def get_notification(
    notification_id: int,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
):
    """Get a specific notification by ID."""
    notification_service = NotificationService(db)
    notification = notification_service.get_notification_status(notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@router.get("/user/{user_id}", response_model=List[NotificationResponse])
def get_user_notifications(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[NotificationStatus] = None,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
):
    """Get notifications for a specific user."""
    notification_service = NotificationService(db)
    notifications = notification_service.get_user_notifications(
        user_id=user_id,
        skip=skip,
        limit=limit,
        status=status
    )
    return notifications

@router.post("/{notification_id}/send", response_model=NotificationResponse)
def send_notification(
    notification_id: int,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
):
    """Send a notification immediately."""
    notification_service = NotificationService(db)
    success = notification_service.send_notification(notification_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to send notification")
    return notification_service.get_notification_status(notification_id) 