from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from database import ChatMessage
from repositories.chat_message_repository import ChatMessageRepository
from schemas.chat_message import ChatMessageCreate


class ChatMessageService:
    def __init__(self, session: Session):
        self.repository = ChatMessageRepository(session)

    def create(self, chat_message: ChatMessageCreate):
        return self.repository.create(chat_message)

    def read(self, id: int)  -> ChatMessage:
        return self.repository.get_by_id(id)
    
    def read_all(self):
        return self.repository.get_all()

    def delete(self, id: int)  -> bool:
        return self.repository.delete(id)
