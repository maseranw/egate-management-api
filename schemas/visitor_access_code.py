from pydantic import BaseModel

from schemas.access_code import AccessCode
from schemas.visitor import Visitor

class VisitorAccessCode(BaseModel):
    visitor: Visitor
    access_code: AccessCode
    class Config:
        orm_mode = True