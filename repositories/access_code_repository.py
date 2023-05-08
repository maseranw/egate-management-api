from typing import List
import bcrypt
from sqlalchemy.orm import Session
from database import AccessCode, User, Visitor
import datetime
import time
import random


class AccessCodeRepository:
    def __init__(self, session: Session):
        self.session = session
        self.salt = bcrypt.gensalt()

    # ----------- Create AccessCode--------------
    def create_access_code(self, visitor_id: int):
        while True:
            rand_code = random.randint(1000, 9999)
            existing_access_code = self.session.query(AccessCode).filter_by(code=rand_code).first()
            if not existing_access_code:
                break

        now = datetime.datetime.now()
        midnight = datetime.datetime(now.year, now.month, now.day, 23, 59, 59)
         
        db_access_code = AccessCode(visitor_id=visitor_id, code=rand_code, create_date=now, expiry_date=midnight)
        self.session.add(db_access_code)
        self.session.commit()
        self.session.refresh(db_access_code)
        return db_access_code


    def get_access_code_by_id(self, access_code_id: int):
        return self.session.query(AccessCode).filter(AccessCode.id == access_code_id).first()
    
    
    def get_access_codes_by_visitor_id(self, visitor_id: str, skip: int = 0, limit: int = 100) -> List[AccessCode]:
        return self.session.query(AccessCode).filter(AccessCode.visitor_id == visitor_id).offset(skip).limit(limit).all()
