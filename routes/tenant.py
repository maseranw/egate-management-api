import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from database import get_db
from schemas.tenant import Tenant, TenantCreate, TenantLogin, TenantLoginResponse, TenantUpdate
from services.tenant_service import TenantService
from fastapi_jwt_auth import AuthJWT

router = APIRouter(prefix="/api", tags=["Tenant"])

@router.post("/tenants", response_model=Tenant)
def create_tenant_api(tenant: TenantCreate, db: Session = Depends(get_db),auth: AuthJWT = Depends()):
     # auth.jwt_required()
    service = TenantService(db)
    return service.create_tenant(tenant)


@router.get("/tenants", response_model=List[Tenant])
def get_tenants_api(db: Session = Depends(get_db),auth: AuthJWT = Depends()):
     # auth.jwt_required()
    service = TenantService(db)
    return service.get_tenants()


@router.get("/tenants/{tenant_id}", response_model=Tenant)
def get_tenant_api(tenant_id: int, db: Session = Depends(get_db),auth: AuthJWT = Depends()):
     # auth.jwt_required()
    service = TenantService(db)
    db_tenant = service.get_tenant(tenant_id)
    if db_tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return db_tenant


@router.put("/tenants/{tenant_id}", response_model=Tenant)
def update_tenant_api(tenant_id: int, tenant: TenantUpdate, db: Session = Depends(get_db),auth: AuthJWT = Depends()):
     # auth.jwt_required()
    service = TenantService(db)
    return service.update_tenant(db, tenant_id, tenant)


@router.delete("/tenants/{tenant_id}")
def delete_tenant_api(tenant_id: int, db: Session = Depends(get_db),auth: AuthJWT = Depends()):
     # auth.jwt_required()
    service = TenantService(db)
    return service.delete_tenant(tenant_id)


@router.post('/tenants/login', response_model=TenantLoginResponse)
def login(tenantLogin: TenantLogin, auth_jwt: AuthJWT = Depends(), db: Session = Depends(get_db)):
    service = TenantService(db)
    # authenticate tenant
    tenant = service.authenticate_tenant(tenantLogin.phone, tenantLogin.code)
    if not tenant:
        raise HTTPException(status_code=401, detail='Invalid tenant details')
    # create access token
    access_token = auth_jwt.create_access_token(subject=tenant.id,expires_time=False)
    return TenantLoginResponse( access_token = access_token,tenant = tenant)


def get_current_user_id(auth_jwt: AuthJWT = Depends(),auth: AuthJWT = Depends()):
     # auth.jwt_required()
    auth_jwt.jwt_required()
    current_user_id = auth_jwt.get_jwt_subject()
    return current_user_id
