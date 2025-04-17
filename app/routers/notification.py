from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.notification import NotificationService
from app.schemas.notification import (
    NotificationCreate,
    NotificationUpdate,
    NotificationResponse
)

router = APIRouter(
    prefix="/notifications",
    tags=["notifications"]
)

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
    return notification_service.get_notification(notification_id)

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
    notification_update: NotificationUpdate,
    db: Session = Depends(get_db)
):
    notification_service = NotificationService(db)
    return notification_service.update_notification(notification_id, notification_update)

@router.post("/{notification_id}/deliver", response_model=NotificationResponse)
def mark_as_delivered(
    notification_id: int,
    db: Session = Depends(get_db)
):
    notification_service = NotificationService(db)
    return notification_service.mark_as_delivered(notification_id)

@router.post("/{notification_id}/read", response_model=NotificationResponse)
def mark_as_read(
    notification_id: int,
    db: Session = Depends(get_db)
):
    notification_service = NotificationService(db)
    return notification_service.mark_as_read(notification_id)

@router.delete("/{notification_id}")
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db)
):
    notification_service = NotificationService(db)
    notification_service.delete_notification(notification_id)
    return {"message": "Notification deleted successfully"} 