from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

from schemas.tenant import Tenant

class UserBase(BaseModel):
    username: str
    firstname: str
    lastname: str
    phone: str
    email: str
    
class UserResponse(UserBase):
    pass

class UserCreate(UserBase):
    password: str
    class Config:
        orm_mode = True
        
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
    class Config:
        orm_mode = True