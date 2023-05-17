from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from database import get_db
from schemas.notification import NotificationCreate, Notification
from services.notification_service import NotificationService

router = APIRouter(prefix="/api", tags=["Notification"])

@router.post("/notifications", response_model=Notification)
def create_notification(notification: NotificationCreate, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    # auth.jwt_required()
    notification_service = NotificationService(db)
    created_notification = notification_service.create(notification)
    return created_notification

@router.get("/notifications/{notification_id}", response_model=Notification)
def get_notification(notification_id: int, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    # auth.jwt_required()
    notification_service = NotificationService(db)
    notification = notification_service.get(notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@router.get("/notifications", response_model=List[Notification])
def get_all_notifications(db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    # auth.jwt_required()
    notification_service = NotificationService(db)
    notifications = notification_service.get_all()
    return notifications

@router.delete("/notifications/{notification_id}")
def delete_notification(notification_id: int, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    # auth.jwt_required()
    notification_service = NotificationService(db)
    deleted = notification_service.delete(notification_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"detail": "Notification deleted successfully"}