from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from database import get_db
from schemas.estate import EstateCreate, EstateUpdate, Estate
from services.esate_service import EstateService

router = APIRouter(prefix="/api", tags=["Estate"])

@router.post("/estates", response_model=Estate)
def create_estate(estate: EstateCreate, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    auth.jwt_required()
    estate_service = EstateService(db)
    created_estate = estate_service.create(estate)
    return created_estate

@router.get("/estates/{estate_id}", response_model=Estate)
def get_estate(estate_id: int, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    auth.jwt_required()
    estate_service = EstateService(db)
    estate = estate_service.get(estate_id)
    if not estate:
        raise HTTPException(status_code=404, detail="Estate not found")
    return estate

@router.get("/estates", response_model=List[Estate])
def get_all_estates(db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    auth.jwt_required()
    estate_service = EstateService(db)
    estates = estate_service.get_all()
    return estates

@router.put("/estates/{estate_id}", response_model=Estate)
def update_estate(estate_id: int, estate: EstateUpdate, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    auth.jwt_required()
    estate_service = EstateService(db)
    updated_estate = estate_service.update(estate_id, estate)
    if not updated_estate:
        raise HTTPException(status_code=404, detail="Estate not found")
    return updated_estate

@router.delete("/estates/{estate_id}")
def delete_estate(estate_id: int, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    auth.jwt_required()
    estate_service = EstateService(db)
    deleted = estate_service.delete(estate_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Estate not found")
    return {"detail": "Estate deleted successfully"}

