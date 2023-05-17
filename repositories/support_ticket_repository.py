from sqlalchemy.orm import Session
from datetime import datetime
from schemas.support_ticket import SupportTicketCreate, SupportTicketUpdate
from database import SupportTicket

class SupportTicketRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, ticket: SupportTicketCreate):
        db_ticket = SupportTicket(
            **ticket.dict(),
            status = "New",
        )
        self.session.add(db_ticket)
        self.session.commit()
        self.session.refresh(db_ticket)
        return db_ticket

    def update(self, ticket: SupportTicketUpdate):
        db_ticket = self.get(ticket.id)
        for field, value in ticket:
            setattr(db_ticket, field, value)
        db_ticket.update_date = datetime.utcnow
        self.session.commit()
        self.session.refresh(db_ticket)
        return db_ticket

    def delete(self, id: int):
        db_ticket = self.get(id)
        self.session.delete(db_ticket)
        self.session.commit()

    def get(self, id: int):
        return self.session.query(SupportTicket).filter(SupportTicket.id == id).first()

    def get_by_tenant_id(self, id: int):
        return self.session.query(SupportTicket).filter(SupportTicket.tenant_id == id).all()
    
    def get_all(self):
        return self.session.query(SupportTicket).all()
