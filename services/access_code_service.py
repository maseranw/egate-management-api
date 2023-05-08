from typing import List
from sqlalchemy.orm import Session
from schemas.access_code import AccessCode
from repositories.access_code_repository import AccessCodeRepository
from schemas.visitor import Visitor, VisitorCreate
from services.visitor_service import VisitorService

class AccessCodeService:
    def __init__(self, session: Session):
        self.AccessCode_repository = AccessCodeRepository(session)
        self.visitor_service = VisitorService(session)

    def create_access_code(self,visitor: VisitorCreate) -> AccessCode:
        _visitor: Visitor = self.visitor_service.create_visitor(visitor)
        return self.AccessCode_repository.create_access_code(_visitor.id)

    def get_access_code_by_id(self, access_code_id: int) -> AccessCode:
        return self.AccessCode_repository.get_access_code_by_id(access_code_id)

    def get_access_codes_by_visitor_id(self, visitor_id: int) -> List[AccessCode]:
        return self.AccessCode_repository.get_access_codes_by_visitor_id(visitor_id)
    