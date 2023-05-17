from typing import List
from fastapi import APIRouter, Depends, HTTPException,status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserUpdate
from database import get_db
from schemas.user import User
from services.user_service import UserService

router = APIRouter(prefix="/api", tags=["User"])

@router.post('/users', response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db),auth: AuthJWT = Depends()):
    auth.jwt_required()
    user_service = UserService(db)
    db_user = user_service.get_user_by_username(user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return user_service.create_user(user)

@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: int,user: UserUpdate, db: Session = Depends(get_db),auth: AuthJWT = Depends()):
    auth.jwt_required()
    user_service = UserService(db)
    db_user = user_service.get_user(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_service.update_user(user_id, user)

@router.get('/users', response_model=List[User])
def read_users(db: Session = Depends(get_db),auth: AuthJWT = Depends()):
    auth.jwt_required()
    user_service = UserService(db)
    users = user_service.get_users()
    return users

@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db),auth: AuthJWT = Depends()):
    auth.jwt_required()
    user_service = UserService(db)
    db_user = user_service.get_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/protected")
def protected_route(auth: AuthJWT = Depends()):
    auth.jwt_required()
    allowed_roles = ["admin", "support","manager"]
    current_user = auth.get_raw_jwt()
    if current_user.get('role') in allowed_roles:
        return {"message": "You have access to the protected route as an admin."}
    else:
        return {"message": "You don't have access to access this resource"}
