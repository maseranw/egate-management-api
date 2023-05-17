from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class EstateBase(BaseModel):
    name: str
    address: str


class EstateCreate(EstateBase):
    pass


class EstateUpdate(EstateBase):
    pass


class TenantEstateResponse(EstateBase):
    id: int
    class Config:
        orm_mode = True
    
class EstateResponse(EstateBase):
    id: int
    create_date: Optional[datetime]
    update_date: Optional[datetime]
    # tenants: Optional[List[Tenant]]


class Estate(EstateBase):
    id: int
    create_date: Optional[datetime]
    update_date: Optional[datetime]
    # tenants: Optional[List[Tenant]]

    class Config:
        orm_mode = True
