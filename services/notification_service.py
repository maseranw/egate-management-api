from typing import List
from sqlalchemy.orm import Session
from repositories.notification_repository import NotificationRepository
from schemas.notification import NotificationCreate, NotificationResponse
from database import Notification

class NotificationService:
    def __init__(self, session: Session):
        self.notification_repository = NotificationRepository(session)

    def create(self, new_notification: NotificationCreate) -> NotificationResponse:
        return self.notification_repository.create(new_notification)

    def get(self, id: int) -> Notification:
        return self.notification_repository.get(id)

    def get_all(self) -> List[Notification]:
        return self.notification_repository.get_all()

    def delete(self, id: int) -> bool:
        return self.notification_repository.delete(id)
