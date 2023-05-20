from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from database import  get_db
from schemas.visitor import Visitor, VisitorCreate, VisitorUpdate
from schemas.visitor_access_code import VisitorAccessCode
from services.visitor_service import VisitorService

router = APIRouter(prefix="/api", tags=["Visitor"])

@router.post("/visitors", response_model=VisitorAccessCode)
async def create_visitor_api(visitor: VisitorCreate, db: Session = Depends(get_db),auth: AuthJWT = Depends()):
    auth.jwt_required()
    service = VisitorService(db)
    _newVisitor = service.create_visitor(visitor)
    await service.ws_visitor_created(_newVisitor.visitor.tenant_id) 
    return _newVisitor


@router.get("/visitors", response_model=List[Visitor])
def get_visitors_api(db: Session = Depends(get_db),auth: AuthJWT = Depends()):
    auth.jwt_required()
    service = VisitorService(db)
    return service.get_visitors()


@router.get("/visitors/{visitor_id}", response_model=Visitor)
def get_visitor_api(visitor_id: int, db: Session = Depends(get_db),auth: AuthJWT = Depends()):
    auth.jwt_required()
    service = VisitorService(db)
    db_visitor = service.get_visitor(visitor_id)
    if db_visitor is None:
        raise HTTPException(status_code=404, detail="visitor not found")
    return db_visitor

@router.get("/users/visitors/{user_id}", response_model=List[Visitor])
def get_visitor_api(user_id: int, db: Session = Depends(get_db),auth: AuthJWT = Depends()):
    auth.jwt_required()
    service = VisitorService(db)
    db_visitor = service.get_visitor_by_userId(user_id)
    if db_visitor is None:
        raise HTTPException(status_code=404, detail="visitor not found")
    return db_visitor


@router.put("/visitors/{visitor_id}", response_model=Visitor)
def update_visitor_api(visitor_id: int, visitor: VisitorUpdate, db: Session = Depends(get_db),auth: AuthJWT = Depends()):
    auth.jwt_required()
    service = VisitorService(db)
    return service.update_visitor(db, visitor_id, visitor)


@router.delete("/visitors/{visitor_id}")
async def delete_visitor_api(visitor_id: int, db: Session = Depends(get_db),auth: AuthJWT = Depends()):
    auth.jwt_required()
    service = VisitorService(db)
    visitor = service.delete_visitor(db, visitor_id)
    await service.ws_visitor_deleted(visitor.tenant_id) 
    return 'visitor deleted successfully'