from typing import List
from sqlalchemy.orm import Session
from repositories.support_ticket_type_repository import SupportTicketTypeRepository
from schemas.support_ticket_type import SupportTicketTypeCreate, SupportTicketTypeUpdate, SupportTicketTypeResponse
from database import SupportTicketType

class SupportTicketTypeService:
    def __init__(self, session: Session):
        self.support_ticket_type_repository = SupportTicketTypeRepository(session)

    def create(self, new_support_ticket_type: SupportTicketTypeCreate) -> SupportTicketTypeResponse:
        return self.support_ticket_type_repository.create(new_support_ticket_type)

    def get(self, id: int) -> SupportTicketType:
        return self.support_ticket_type_repository.get(id)

    def get_all(self) -> List[SupportTicketType]:
        return self.support_ticket_type_repository.get_all()

    def update(self, id: int, updated_support_ticket_type: SupportTicketTypeUpdate) -> SupportTicketTypeResponse:
        return self.support_ticket_type_repository.update(id, updated_support_ticket_type)

    def delete(self, id: int) -> bool:
        return self.support_ticket_type_repository.delete(id)
