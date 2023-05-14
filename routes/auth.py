import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from services.user_service import UserService
from database import get_db
from schemas.user import User, UserCreate
from repositories.user_repository import UserRepository

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post('/login')
def login(username: str = Query(...), password: str = Query(...), auth_jwt: AuthJWT = Depends(), db: Session = Depends(get_db)):
    userService = UserService(db)
    # authenticate user
    user_id = userService.authenticate_user(username, password)
    if not user_id:
        raise HTTPException(status_code=401, detail='Invalid username or password')
    # create access token
    expires = datetime.timedelta(days=1)
    access_token = auth_jwt.create_access_token(subject=user_id,expires_time=expires)
    return {'access_token': access_token}


@router.post('/register', response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    userService = UserService(db)
    db_user = userService.get_user_by_username(user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return userService.create_user(user)