from typing import List
from sqlalchemy.orm import Session
from repositories.estate_repository import EstateRepository
from schemas.estate import EstateCreate, EstateUpdate, EstateResponse
from database import Estate

class EstateService:
    def __init__(self, session: Session):
        self.estate_repository = EstateRepository(session)

    def create(self, new_estate: EstateCreate) -> EstateResponse:
        return self.estate_repository.create(new_estate)

    def get(self, id: int) -> Estate:
        return self.estate_repository.get(id)

    def get_all(self) -> List[Estate]:
        return self.estate_repository.get_all()

    def update(self, id: int, updated_estate: EstateUpdate) -> EstateResponse:
        return self.estate_repository.update(id, updated_estate)

    def delete(self, id: int) -> bool:
        return self.estate_repository.delete(id)