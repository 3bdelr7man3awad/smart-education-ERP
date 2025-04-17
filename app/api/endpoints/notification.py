from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.notification import (
    NotificationCreate,
    NotificationUpdate,
    NotificationResponse
)
from app.services.notification import NotificationService

router = APIRouter()

@router.post("/", response_model=NotificationResponse)
def create_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Create a new notification.
    """
    notification_service = NotificationService(db)
    return notification_service.create_notification(notification)

@router.get("/{notification_id}", response_model=NotificationResponse)
def get_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get a specific notification by ID.
    """
    notification_service = NotificationService(db)
    return notification_service.get_notification(notification_id)

@router.get("/user/{user_id}", response_model=List[NotificationResponse])
def get_user_notifications(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get all notifications for a specific user.
    """
    notification_service = NotificationService(db)
    return notification_service.get_user_notifications(user_id, skip, limit)

@router.put("/{notification_id}", response_model=NotificationResponse)
def update_notification(
    notification_id: int,
    notification_update: NotificationUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Update a notification.
    """
    notification_service = NotificationService(db)
    return notification_service.update_notification(notification_id, notification_update)

@router.post("/{notification_id}/deliver", response_model=NotificationResponse)
def mark_as_delivered(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Mark a notification as delivered.
    """
    notification_service = NotificationService(db)
    return notification_service.mark_as_delivered(notification_id)

@router.post("/{notification_id}/read", response_model=NotificationResponse)
def mark_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Mark a notification as read.
    """
    notification_service = NotificationService(db)
    return notification_service.mark_as_read(notification_id)

@router.delete("/{notification_id}")
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Delete a notification.
    """
    notification_service = NotificationService(db)
    notification_service.delete_notification(notification_id)
    return {"message": "Notification deleted successfully"} 