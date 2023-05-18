from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from schemas.estate import TenantEstateResponse


class TenantBase(BaseModel):
    firstname: str
    lastname: str
    phone: str
    email: str
    unitNr: str


class TenantCreate(TenantBase):
    user_id: int
    estate_id: int


class TenantUpdate(TenantBase):
    code: str
    

class TenantUpdateResponse(TenantBase):
    id: int
    code: Optional[str] = None
    user_id: Optional[int] = None
    estate_id: Optional[int] = None
    
class TenantResponse(TenantBase):
    id: int
    code: Optional[str] = None
    create_date: Optional[datetime] = None
    update_date: Optional[datetime] = None
    user_id: Optional[int] = None
    estate_id: Optional[int] = None
    estate: Optional[TenantEstateResponse]


class Tenant(TenantBase):
    id: int
    code: str
    create_date: datetime
    update_date: Optional[datetime] = None
    user_id: Optional[int] = None
    estate_id: Optional[int] = None
    estate: Optional[TenantEstateResponse]

    class Config:
        orm_mode = True


class TenantLogin(BaseModel):
    phone: str
    code: str


class TenantLoginResponse(BaseModel):
    access_token: str
    tenant: Tenant

    class Config:
        orm_mode = True
