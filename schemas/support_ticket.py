from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class SupportTicketBase(BaseModel):
    type_id: int
    tenant_id: int
    description: str

class SupportTicketCreate(SupportTicketBase):
    pass

class SupportTicketUpdate(SupportTicketBase):
    id: int

class SupportTicket(BaseModel):
    id: int
    type_id: int
    tenant_id: int
    description: str
    status: Optional[str] = None
    created_at: Optional[datetime]
    update_date: Optional[datetime] = None

    class Config:
        orm_mode = True
