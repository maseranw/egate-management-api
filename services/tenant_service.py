from typing import List
from sqlalchemy.orm import Session
from schemas.tenant import TenantCreate, TenantUpdate
from database import Tenant
from repositories.tenant_repository import TenantRepository

class TenantService:
    def __init__(self, session: Session):
        self.tenant_repository = TenantRepository(session)

    def create_tenant(self, new_tenant: TenantCreate) -> Tenant:
        return self.tenant_repository.create_tenant(new_tenant)

    def get_tenant(self, tenant_id: int) -> Tenant:
        return self.tenant_repository.get_tenant_by_id(tenant_id)

    def get_tenants(self, skip: int = 0, limit: int = 100) -> List[Tenant]:
        return self.tenant_repository.get_all_tenants(skip, limit)

    def update_tenant(self, tenant_id: int, updated_tenant: TenantUpdate) -> Tenant:
        return self.tenant_repository.update_tenant(tenant_id, updated_tenant)

    def delete_tenant(self, tenant_id: int) -> bool:
        return self.tenant_repository.delete_tenant(tenant_id)
