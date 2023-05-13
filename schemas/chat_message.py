from pydantic import BaseModel
from datetime import datetime

class ChatMessageCreate(BaseModel):
    message: str
    username: str
    sender: str
    tenant_id: int

class ChatMessage(BaseModel):
    id: int
    message: str
    username: str
    sender: str
    tenant_id: int
    create_date: datetime

    class Config:
        orm_mode = True
