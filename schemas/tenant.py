from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TenantBase(BaseModel):
    firstname: str
    lastname: str
    phone: str
    email: str


class TenantCreate(TenantBase):
     user_id: int
     
     class Config:
        orm_mode = True


class TenantUpdate(TenantBase):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    

class TenantResponse(TenantBase):
    id: int
    code: Optional[str] = None
    create_date: Optional[datetime] = None
    update_date: Optional[datetime] = None
    user_id: Optional[int] = None


class Tenant(TenantBase):
    id: int
    code: str
    create_date: datetime
    update_date: Optional[datetime] = None
    user_id: Optional[int] = None

    class Config:
        orm_mode = True