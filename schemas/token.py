from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TokenBase(BaseModel):
    visitor_id: int
    code: int
    create_date: datetime
    update_date: Optional[datetime]
    expiry_date: datetime

    def is_code_expired(self) -> bool:
        return self.expiry_date < datetime.now()


class TokenCreate(BaseModel):
    visitor_id: int
    

class TokenUpdate(BaseModel):
    visitor_id: int = None
    expiry_date: datetime = None
    

class Token(TokenBase):
    id: int
    class Config:
        orm_mode = True
