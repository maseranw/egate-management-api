import json
from typing import List
from sqlalchemy.orm import Session
from schemas.access_code import AccessCode
from repositories.access_code_repository import AccessCodeRepository
from schemas.visitor import Visitor, VisitorCreate
from services.visitor_service import VisitorService
from routes.websocket_manager import manager

class AccessCodeService:
    def __init__(self, session: Session):
        self.accessCode_repository = AccessCodeRepository(session)
        self.visitor_service = VisitorService(session)

    def create_access_code(self,visitor: VisitorCreate) -> AccessCode:
        _visitor: Visitor = self.visitor_service.create_visitor(visitor)
        return self.accessCode_repository.create_access_code(_visitor.id)

    def get_access_code_by_id(self, access_code_id: int) -> AccessCode:
        return self.accessCode_repository.get_access_code_by_id(access_code_id)
    
    def delete_access_code(self, access_code_id: int,visitor_id: int) -> AccessCode:
        self.visitor_service.delete_visitor(visitor_id)
        return self.accessCode_repository.delete_access_code(access_code_id)

    def get_access_codes_by_visitor_id(self, visitor_id: int) -> List[AccessCode]:
        return self.accessCode_repository.get_access_codes_by_visitor_id(visitor_id)
    
    def get_access_codes_by_tenant_id(self, tenant_id: int) -> List[AccessCode]:
        return self.accessCode_repository.get_access_codes_by_tenant_id(tenant_id)
    
    async def ws_visitor_access_deleted(self, tenant_id):
            message = {'event': 'visitor_access_deleted', 'tenant_id': tenant_id}
            _json = json.dumps(message)
            await manager.broadcastJson(_json)
    
    
    
    
    