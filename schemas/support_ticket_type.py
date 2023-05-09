from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class SupportTicketTypeBase(BaseModel):
    name: str

class SupportTicketTypeCreate(SupportTicketTypeBase):
    pass

class SupportTicketTypeUpdate(SupportTicketTypeBase):
    id: int

class SupportTicketTypeResponse(BaseModel):
    id: int
    name: str
    create_date: Optional[datetime]
    update_date: Optional[datetime] = None

    class Config:
        orm_mode = True
