from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.notification import Notification
from app.schemas.notification import NotificationCreate, NotificationUpdate

class NotificationService:
    def __init__(self, db: Session):
        self.db = db

    def create_notification(self, notification: NotificationCreate) -> Notification:
        db_notification = Notification(
            title=notification.title,
            message=notification.message,
            user_id=notification.user_id,
            notification_type=notification.notification_type,
            priority=notification.priority,
            metadata=notification.metadata,
            is_delivered=False,
            is_read=False
        )
        self.db.add(db_notification)
        self.db.commit()
        self.db.refresh(db_notification)
        return db_notification

    def get_notification(self, notification_id: int) -> Optional[Notification]:
        return self.db.query(Notification).filter(Notification.id == notification_id).first()

    def get_user_notifications(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Notification]:
        return (
            self.db.query(Notification)
            .filter(Notification.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update_notification(
        self, notification_id: int, notification: NotificationUpdate
    ) -> Optional[Notification]:
        db_notification = self.get_notification(notification_id)
        if db_notification:
            update_data = notification.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_notification, key, value)
            db_notification.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(db_notification)
        return db_notification

    def mark_as_delivered(self, notification_id: int) -> Optional[Notification]:
        db_notification = self.get_notification(notification_id)
        if db_notification:
            db_notification.is_delivered = True
            db_notification.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(db_notification)
        return db_notification

    def mark_as_read(self, notification_id: int) -> Optional[Notification]:
        db_notification = self.get_notification(notification_id)
        if db_notification:
            db_notification.is_read = True
            db_notification.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(db_notification)
        return db_notification

    def delete_notification(self, notification_id: int) -> bool:
        db_notification = self.get_notification(notification_id)
        if db_notification:
            self.db.delete(db_notification)
            self.db.commit()
            return True
        return False 