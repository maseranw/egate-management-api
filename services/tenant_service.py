from typing import List
from sqlalchemy.orm import Session
from repositories.estate_repository import EstateRepository
from schemas.estate import EstateResponse, TenantEstateResponse
from schemas.tenant import TenantCreate, TenantResponse, TenantUpdate, TenantUpdateResponse
from database import Estate, Tenant
from repositories.tenant_repository import TenantRepository

class TenantService:
    def __init__(self, session: Session):
        self.tenant_repository = TenantRepository(session)
        self.estate_repository = EstateRepository(session)

    def create_tenant(self, new_tenant: TenantCreate) -> Tenant:
        tenant = self.tenant_repository.create_tenant(new_tenant)
        return self._map_tenant_with_estate(tenant)

    def get_tenant(self, tenant_id: int) -> Tenant:
        tenant = self.tenant_repository.get_tenant_by_id(tenant_id)
        return self._map_tenant_with_estate(tenant)

    def get_tenants(self) -> List[TenantResponse]:
        tenants = self.tenant_repository.get_all_tenants()
        return [self._map_tenant_with_estate(tenant) for tenant in tenants]

    def update_tenant(self, tenant_id: int, updated_tenant: TenantUpdate) -> TenantResponse:
        tenant =  self.tenant_repository.update_tenant(tenant_id, updated_tenant)
        return self._map_tenant_with_estate(tenant)

    def delete_tenant(self, tenant_id: int) -> bool:
        return self.tenant_repository.delete_tenant(tenant_id)
    
    def authenticate_tenant(self, phone: str, code: str) -> TenantResponse:
        tenant = self.tenant_repository.get_user_by_phone_and_code(phone,code)
        return self._map_tenant_with_estate(tenant)
    
    
    def _map_tenant_update_with_estate(self, tenant: Tenant) -> TenantUpdateResponse:
        tenant_response = TenantUpdateResponse(
            id=tenant.id,
            firstname=tenant.firstname,
            lastname=tenant.lastname,
            phone=tenant.phone,
            email=tenant.email,
            unitNr=tenant.unitNr,
            code=tenant.code,
            user_id=tenant.user_id,
        )
        return tenant_response
        
    def _map_tenant_with_estate(self, tenant: Tenant) -> TenantResponse:
        estate = self.estate_repository.get(tenant.estate_id)
        
        estate_response = TenantEstateResponse(
            id=estate.id,
            name=estate.name,
            address=estate.address,
        )
         
        tenant_response = TenantResponse(
            id=tenant.id,
            firstname=tenant.firstname,
            lastname=tenant.lastname,
            phone=tenant.phone,
            email=tenant.email,
            unitNr=tenant.unitNr,
            estate=estate_response,
            code=tenant.code,
            create_date=tenant.create_date,
            update_date=tenant.update_date,
            user_id=tenant.user_id,
        )
        return tenant_response
          
