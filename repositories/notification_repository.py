import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from database import Notification
from schemas.notification import NotificationCreate


class NotificationRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(self, notification_id: int):
        return self.session.query(Notification).filter(Notification.id == notification_id).first()

    def get_all(self):
        return self.session.query(Notification).all()

    def create(self, notification: NotificationCreate):
        db_notification = Notification(**notification.dict())
        self.session.add(db_notification)
        self.session.commit()
        self.session.refresh(db_notification)
        return db_notification
    

    def delete(self, notification_id: int):
        db_notification = self.get(notification_id)
        if db_notification is None:
            raise HTTPException(status_code=404, detail="Notification not found")
        self.session.delete(db_notification)
        self.session.commit()
        return {"message": "Notification deleted successfully"}
