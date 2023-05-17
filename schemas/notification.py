from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class NotificationBase(BaseModel):
    title: str
    message: str


class NotificationCreate(NotificationBase):
    estate_id: int
    user_id: int


class NotificationResponse(NotificationBase):
    id: int
    create_date: Optional[datetime]
    update_date: Optional[datetime]
    estate_id: Optional[int]
    user_id: Optional[int]

    class Config:
        orm_mode = True


class Notification(NotificationBase):
    id: int
    create_date: Optional[datetime]
    update_date: Optional[datetime]
    estate_id: Optional[int]
    user_id: Optional[int]

    class Config:
        orm_mode = True