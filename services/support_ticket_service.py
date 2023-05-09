from typing import List
from sqlalchemy.orm import Session
from repositories.support_ticket_repository import SupportTicketRepository
from schemas.support_ticket import SupportTicketCreate, SupportTicketUpdate
from database import SupportTicket

class SupportTicketService:
    def __init__(self, session: Session):
        self.support_ticket_repository = SupportTicketRepository(session)

    def create(self, new_support_ticket: SupportTicketCreate) -> SupportTicket:
        return self.support_ticket_repository.create(new_support_ticket)

    def get(self, id: int) -> SupportTicket:
        return self.support_ticket_repository.get(id)
    
    def get_by_tenant_id(self, id: int) -> SupportTicket:
        return self.support_ticket_repository.get_by_tenant_id(id)

    def get_all(self) -> List[SupportTicket]:
        return self.support_ticket_repository.get_all()

    def update(self, id: int, updated_support_ticket: SupportTicketUpdate) -> SupportTicket:
        return self.support_ticket_repository.update(id, updated_support_ticket)

    def delete(self, id: int) -> bool:
        return self.support_ticket_repository.delete(id)
