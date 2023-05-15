from typing import List
from sqlalchemy.orm import Session
from database import ChatMessage
import datetime
from schemas.chat_message import ChatMessageCreate


class ChatMessageRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[ChatMessage]:
        return self.session.query(ChatMessage).all()

    def get_by_id(self, id: int) -> ChatMessage:
        return self.session.query(ChatMessage).get(id)

    def create(self, message: ChatMessageCreate) -> ChatMessage:
        db_message = ChatMessage(
            **message.dict(),
            create_date=datetime.datetime.now()
        )
        self.session.add(db_message)
        self.session.commit()
        self.session.refresh(db_message)
        return db_message

    def delete(self, message: ChatMessage) -> None:
        self.session.delete(message)
        self.session.commit()
