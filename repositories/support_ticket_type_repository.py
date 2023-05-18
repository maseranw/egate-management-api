from sqlalchemy.orm import Session
from date_helper import DateHelper
from schemas.support_ticket_type import SupportTicketTypeCreate, SupportTicketTypeUpdate
from database import SupportTicketType

date_helper = DateHelper()

class SupportTicketTypeRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, ticket: SupportTicketTypeCreate):
        db_ticket_type = SupportTicketType(
            **ticket.dict(),create_date=date_helper.get_date()
        )
        self.session.add(db_ticket_type)
        self.session.commit()
        self.session.refresh(db_ticket_type)
        return db_ticket_type

    def update(self, ticket: SupportTicketTypeUpdate):
        db_ticket_type = self.get(ticket.id)
        for field, value in ticket:
            setattr(db_ticket_type, field, value)
        db_ticket_type.update_date = date_helper.get_date()
        self.session.commit()
        self.session.refresh(db_ticket_type)
        return db_ticket_type

    def delete(self, id: int):
        db_ticket_type = self.get(id)
        self.session.delete(db_ticket_type)
        self.session.commit()

    def get(self, id: int):
        return self.session.query(SupportTicketType).filter(SupportTicketType.id == id).first()
    
    def get_all(self):
        return self.session.query(SupportTicketType).all()
