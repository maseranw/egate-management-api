from typing import List
import bcrypt
from sqlalchemy.orm import Session
from database import Token, User, Visitor
import datetime
import time
import random


class TokenRepository:
    def __init__(self, session: Session):
        self.session = session
        self.salt = bcrypt.gensalt()

    # ----------- Create token--------------
    def create_token(self, visitor_id: int):
        while True:
            rand_code = random.randint(1000, 9999)
            existing_token = self.session.query(Token).filter_by(code=rand_code).first()
            if not existing_token:
                break

        now = datetime.datetime.now()
        midnight = datetime.datetime(now.year, now.month, now.day, 23, 59, 59)
         
        db_token = Token(visitor_id=visitor_id, code=rand_code, create_date=now, expiry_date=midnight)
        self.session.add(db_token)
        self.session.commit()
        self.session.refresh(db_token)
        return db_token


    def get_token_by_id(self, token_id: int):
        return self.session.query(Token).filter(Token.id == token_id).first()
    
    def get_tokens_by_user_id(self, user_id: int) -> List[Token]:
        tokens = self.session.query(Token).join(Visitor).filter(Visitor.user_id == user_id).all()
        return tokens
    
    def get_tokens_by_visitor_id(self, visitor_id: str, skip: int = 0, limit: int = 100) -> List[Token]:
        return self.session.query(Token).filter(Token.visitor_id == visitor_id).offset(skip).limit(limit).all()
