from datetime import datetime
from pydantic import BaseModel


class CarBase(BaseModel):
    make: str
    model: str
    year: int
    visitor_id: int
    create_date: datetime
    update_date: datetime

class Car(CarBase):
    id: int
    class Config:
        orm_mode = True #