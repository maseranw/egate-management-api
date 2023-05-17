from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

from schemas.user_role import UserRole


class UserBase(BaseModel):
    username: str
    firstname: str
    lastname: str
    phone: str
    email: str
    role_id: int  
    
class UserResponse(UserBase):
    pass

class UserCreate(UserBase):
    password: str
        
class UserUpdate(UserBase):
    username: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

        
class UserPasswordUpdate(BaseModel):
    password: str
    
class User(UserBase):
    id: int
    create_date: datetime
    update_date: datetime = None
    role_id: int  
    user_role: Optional[UserRole]
    class Config:
        orm_mode = True