from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from schemas.token import Token


class VisitorBase(BaseModel):
    car_id: int = None
    tenant_id: int = None


class VisitorCreate(VisitorBase):
    phone: str
    class Config:
        orm_mode = True


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
    create_date: Optional[datetime]
    update_date: datetime = None
    check_in_time: datetime = None
    check_out_time: datetime = None
    tokens: List[Token]
    tenant_id: int
    class Config:
        orm_mode = True