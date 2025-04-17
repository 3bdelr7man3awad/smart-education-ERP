from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.notification import (
    NotificationCreate,
    NotificationUpdate,
    NotificationResponse
)
from app.services.notification import NotificationService

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.post("/", response_model=NotificationResponse)
def create_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db)
):
    notification_service = NotificationService(db)
    return notification_service.create_notification(notification)

@router.get("/{notification_id}", response_model=NotificationResponse)
def get_notification(
    notification_id: int,
    db: Session = Depends(get_db)
):
    notification_service = NotificationService(db)
    notification = notification_service.get_notification(notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@router.get("/user/{user_id}", response_model=List[NotificationResponse])
def get_user_notifications(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    notification_service = NotificationService(db)
    return notification_service.get_user_notifications(user_id, skip, limit)

@router.put("/{notification_id}", response_model=NotificationResponse)
def update_notification(
    notification_id: int,
    notification: NotificationUpdate,
    db: Session = Depends(get_db)
):
    notification_service = NotificationService(db)
    updated_notification = notification_service.update_notification(notification_id, notification)
    if not updated_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return updated_notification

@router.post("/{notification_id}/deliver", response_model=NotificationResponse)
def mark_as_delivered(
    notification_id: int,
    db: Session = Depends(get_db)
):
    notification_service = NotificationService(db)
    notification = notification_service.mark_as_delivered(notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@router.post("/{notification_id}/read", response_model=NotificationResponse)
def mark_as_read(
    notification_id: int,
    db: Session = Depends(get_db)
):
    notification_service = NotificationService(db)
    notification = notification_service.mark_as_read(notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@router.delete("/{notification_id}")
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db)
):
    notification_service = NotificationService(db)
    if not notification_service.delete_notification(notification_id):
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"message": "Notification deleted successfully"} 