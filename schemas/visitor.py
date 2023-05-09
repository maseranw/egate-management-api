from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from schemas.access_code import AccessCode

class VisitorBase(BaseModel):
    tenant_id: int = None
    phone: str


class VisitorCreate(VisitorBase):
    pass

class VisitorUpdate(VisitorBase):
    phone: str = None
    check_in_time: datetime = None
    check_out_time: datetime = None
    
class VisitorResponse(VisitorBase):
    phone: str = None
    check_in_time: datetime = None
    check_out_time: datetime = None


class Visitor(BaseModel):
    id: int = None
    phone: Optional[str]
    car_id: Optional[int] = None
    create_date: Optional[datetime]
    update_date: datetime = None
    check_in_time: datetime = None
    check_out_time: datetime = None
    access_codes: List[AccessCode]
    tenant_id: int
    class Config:
        orm_mode = True