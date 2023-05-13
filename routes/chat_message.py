from typing import List
from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from database import get_db
from schemas.chat_message import ChatMessage, ChatMessageCreate
from services.chat_message_service import ChatMessageService
from fastapi_jwt_auth import AuthJWT


router = APIRouter(prefix="/api", tags=["ChatMessage"])

@router.post("/chat_messages",  response_model=ChatMessage)
def create_chat_message(chat_message: ChatMessageCreate, db: Session = Depends(get_db),auth: AuthJWT = Depends()):
    service = ChatMessageService(db)
    return service.create(chat_message)

@router.get("/chat_messages/{id}", response_model=ChatMessage)
def get_chat_message(id: int, db: Session = Depends(get_db),auth: AuthJWT = Depends()):
    service = ChatMessageService(db)
    return service.read(id)


@router.get("/chat_messages", response_model=List[ChatMessage])
def get_tenants_api(db: Session = Depends(get_db),auth: AuthJWT = Depends()):
     # auth.jwt_required()
    service = ChatMessageService(db)
    return service.read_all()

@router.delete("/chat_messages/{id}")
def delete_chat_message(id: int, db: Session = Depends(get_db),auth: AuthJWT = Depends()):
    service = ChatMessageService(db)
    return service.delete(id)
