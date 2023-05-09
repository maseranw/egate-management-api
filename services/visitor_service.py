from typing import List
from sqlalchemy.sql.expression import Tuple
from sqlalchemy.orm import Session
from database import AccessCode
from schemas.visitor import Visitor, VisitorCreate, VisitorUpdate
from schemas.visitor_access_code import VisitorAccessCode
from repositories.access_code_repository import AccessCodeRepository
from repositories.visitor_repository import VisitorRepository

class VisitorService:
    def __init__(self, session: Session):
        self.visitor_repository = VisitorRepository(session)
        self.access_code_repository = AccessCodeRepository(session)
        
    def get_visitor(self, visitor_id: int) -> Visitor:
        return self.visitor_repository.get_visitor(visitor_id)
    
    def get_visitor_by_userId(self, user_id: int) -> Visitor:
        return self.visitor_repository.get_visitor_by_userId(user_id)
    
    def get_visitors(self) -> List[Visitor]:
        return self.visitor_repository.get_visitors()
    
    
    def create_visitor(self, visitor_create: VisitorCreate) -> VisitorAccessCode:
        visitor = self.visitor_repository.get_visitor_by_phone(visitor_create.phone)
        if visitor is None:
            visitor =  self.visitor_repository.create_visitor(visitor_create)
        access_code = self.access_code_repository.create_access_code(visitor.id)
        return VisitorAccessCode(visitor=visitor,access_code=access_code)
    
    def update_visitor(self,visitor_id: int, visitor: VisitorUpdate) -> Visitor:
        return self.visitor_repository.update_visitor(visitor_id,visitor)
    
    def delete_visitor(self,visitor_id: int):
        return self.visitor_repository.delete_visitor(visitor_id)
