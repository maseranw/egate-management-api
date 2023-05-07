from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from fastapi_jwt_auth import AuthJWT
from schemas.token import Token
from services.token_service import TokenService
from services.user_service import UserService

router = APIRouter(prefix="/api/tokens", tags=["token"])

@router.post('/generate/{user_id}', response_model=Token)
def generate(user_id: int, db: Session = Depends(get_db),auth: AuthJWT = Depends()):
    auth.jwt_required()
    user_service = UserService(db)
    db_user = user_service.get_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    service = TokenService(db)
    return service.create_token(user_id)

@router.get('/{token_id}', response_model=List[Token])
def read_token(token_id: int, db: Session = Depends(get_db),auth: AuthJWT = Depends()):
    auth.jwt_required()
    service = TokenService(db)
    users = service.get_token_by_id(token_id)
    return users

@router.get("/visitor/{visitor_id}", response_model=List[Token])
def read_user(visitor_id: int, db: Session = Depends(get_db),auth: AuthJWT = Depends()):
    auth.jwt_required()
    service = TokenService(db)
    tokens = service.get_tokens_by_visitor_id(visitor_id)
    return tokens

@router.get("/user/{user_id}", response_model=List[Token])
def read_user(user_id: int, db: Session = Depends(get_db),auth: AuthJWT = Depends()):
    auth.jwt_required()
    service = TokenService(db)
    user_service = UserService(db)
    db_user = user_service.get_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    tokens = service.get_tokens_by_user_id(user_id)
    return tokens
