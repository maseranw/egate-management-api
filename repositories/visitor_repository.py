import datetime
from typing import List
import bcrypt
from fastapi import HTTPException
from sqlalchemy.orm import Session
from database import Visitor
from schemas.visitor import VisitorCreate, VisitorUpdate

class VisitorRepository:
    def __init__(self, session: Session):
        self.session = session
        self.salt = bcrypt.gensalt()

    def get_visitor(self, visitor_id: int):
        return self.session.query(Visitor).filter(Visitor.id == visitor_id).first()

    def get_visitor_by_userId(self, user_id: int):
        return self.session.query(Visitor).filter(Visitor.user_id == user_id).all()
    
    
    def get_visitor_by_phone_and_tenant(self, phone: str, tenant_id: int):
        return self.session.query(Visitor).filter(Visitor.phone == phone, Visitor.tenant_id == tenant_id).first()
    
    def get_visitors(self):
        return self.session.query(Visitor).all()

    def create_visitor(self, visitor: VisitorCreate):
        db_visitor = Visitor(**visitor.dict())
        self.session.add(db_visitor)
        self.session.commit()
        self.session.refresh(db_visitor)
        return db_visitor


    def update_visitor(self,visitor_id: int, visitor: VisitorUpdate):
        db_visitor = self.get_visitor(visitor_id)
        if db_visitor is None:
            raise HTTPException(status_code=404, detail="visitor not found")
        update_data = visitor.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_visitor, key, value)
        db_visitor.update_date = datetime.datetime.now()
        self.session.commit()
        self.session.refresh(db_visitor)
        return db_visitor


    def delete_visitor(self,visitor_id: int):
        db_visitor = self.get_visitor(visitor_id)
        if db_visitor is None:
            raise HTTPException(status_code=404, detail="visitor not found")
        self.session.delete(db_visitor)
        self.session.commit()
        return {"message": "visitor deleted successfully"}