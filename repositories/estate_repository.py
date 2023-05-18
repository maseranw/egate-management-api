from fastapi import HTTPException
import pytz
from sqlalchemy.orm import Session
from database import Estate
from date_helper import DateHelper
from schemas.estate import EstateCreate, EstateUpdate

date_helper = DateHelper()

class EstateRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(self, estate_id: int):
        return self.session.query(Estate).filter(Estate.id == estate_id).first()

    def get_all(self):
        return self.session.query(Estate).all()

    def create(self, estate: EstateCreate):
        db_estate = Estate(**estate.dict(),create_date=date_helper.get_date())
        self.session.add(db_estate)
        self.session.commit()
        self.session.refresh(db_estate)
        return db_estate

    def update(self, estate_id: int, estate: EstateUpdate):
        db_estate = self.get(estate_id)
        
        if db_estate is None:
            raise HTTPException(status_code=404, detail="Estate not found")
        update_data = estate.dict(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(db_estate, key, value)
            
        db_estate.update_date = date_helper.get_date()
        self.session.commit()
        self.session.refresh(db_estate)
        return db_estate

    def delete(self, estate_id: int):
        db_estate = self.get(estate_id)
        if db_estate is None:
            raise HTTPException(status_code=404, detail="Estate not found")
        self.session.delete(db_estate)
        self.session.commit()
        return {"message": "Estate deleted successfully"}
