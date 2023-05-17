from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from fastapi_jwt_auth import AuthJWT
from schemas.access_code import AccessCode
from schemas.visitor import VisitorCreate
from services.tenant_service import TenantService
from services.access_code_service import AccessCodeService
from services.user_service import UserService
from services.visitor_service import VisitorService

router = APIRouter(prefix="/api", tags=["AccessCode"])

@router.get('/access-codes/{access_code_id}', response_model=List[AccessCode])
def read_access_code(access_code_id: int, db: Session = Depends(get_db),auth: AuthJWT = Depends()):
    auth.jwt_required()
    service = AccessCodeService(db)
    results = service.get_access_code_by_id(access_code_id)
    return results

@router.delete('/access-codes/{access_code_id}')
def delete_access_code(access_code_id: int, db: Session = Depends(get_db),auth: AuthJWT = Depends()):
    auth.jwt_required()
    service = AccessCodeService(db)
    results = service.delete_access_code(access_code_id)
    return results


@router.get("/access-codes/visitor/{visitor_id}", response_model=List[AccessCode])
def read_user(visitor_id: int, db: Session = Depends(get_db),auth: AuthJWT = Depends()):
    auth.jwt_required()
    service = AccessCodeService(db)
    access_codes = service.get_access_codes_by_visitor_id(visitor_id)
    return access_codes

@router.get("/access-codes/tenant/{tenant_id}")
def read_user(tenant_id: int, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    try:
        auth.jwt_required()
        service = AccessCodeService(db)
        tenant_service = TenantService(db)
        db_tenant = tenant_service.get_tenant(tenant_id)
        access_codes = service.get_access_codes_by_tenant_id(db_tenant.id)
        return access_codes
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
