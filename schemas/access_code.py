from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AccessCodeBase(BaseModel):
    visitor_id: int = None
    code: int = None
    create_date: datetime = None
    update_date: Optional[datetime] = None
    expiry_date: datetime = None

    def is_code_expired(self) -> bool:
        return self.expiry_date < datetime.now()


class AccessCodeCreate(BaseModel):
    visitor_id: int
    

class AccessCodeUpdate(BaseModel):
    visitor_id: int = None
    expiry_date: datetime = None
    

class AccessCode(AccessCodeBase):
    id: int = None
    class Config:
        orm_mode = True
