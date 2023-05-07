from pydantic import BaseModel

from schemas.token import Token
from schemas.visitor import Visitor

class VisitorToken(BaseModel):
    visitor: Visitor
    token: Token
    class Config:
        orm_mode = True