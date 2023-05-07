from typing import List
from sqlalchemy.sql.expression import Tuple
from sqlalchemy.orm import Session
from database import Token
from schemas.visitor import Visitor, VisitorCreate, VisitorUpdate
from schemas.visitor_token import VisitorToken
from repositories.token_repository import TokenRepository
from repositories.visitor_repository import VisitorRepository

class VisitorService:
    def __init__(self, session: Session):
        self.visitor_repository = VisitorRepository(session)
        self.token_repository = TokenRepository(session)
        
    def get_visitor(self, visitor_id: int) -> Visitor:
        return self.visitor_repository.get_visitor(visitor_id)
    
    def get_visitor_by_userId(self, user_id: int) -> Visitor:
        return self.visitor_repository.get_visitor_by_userId(user_id)
    
    def get_visitors(self) -> List[Visitor]:
        return self.visitor_repository.get_visitors()
    
    def create_visitor(self, visitor: VisitorCreate) -> VisitorToken:
        visitor =  self.visitor_repository.create_visitor(visitor)
        token = self.token_repository.create_token(visitor.id)
        return VisitorToken(visitor=visitor,token=token)
    
    def update_visitor(self,visitor_id: int, visitor: VisitorUpdate) -> Visitor:
        return self.visitor_repository.update_visitor(visitor_id,visitor)
    
    def delete_visitor(self,visitor_id: int):
        return self.visitor_repository.delete_visitor(visitor_id)
