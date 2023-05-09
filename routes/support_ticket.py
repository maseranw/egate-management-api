from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas.support_ticket import SupportTicketCreate, SupportTicketUpdate, SupportTicket
from services.support_ticket_service import SupportTicketService


router = APIRouter(prefix="/api", tags=["SupportTicket"])


@router.post("/support-tickets", response_model=SupportTicket)
def create_support_ticket(support_ticket: SupportTicketCreate, db: Session = Depends(get_db)):
    ticket_service = SupportTicketService(db)
    created_ticket = ticket_service.create(support_ticket)
    return created_ticket


@router.get("/support-tickets/{ticket_id}", response_model=SupportTicket)
def get_support_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket_service = SupportTicketService(db)
    ticket = ticket_service.get(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.get("/support-tickets", response_model=List[SupportTicket])
def get_all_support_tickets(db: Session = Depends(get_db)):
    ticket_service = SupportTicketService(db)
    tickets = ticket_service.get_all()
    return tickets


@router.put("/support-tickets/{ticket_id}", response_model=SupportTicket)
def update_support_ticket(ticket_id: int, support_ticket: SupportTicketUpdate, db: Session = Depends(get_db)):
    ticket_service = SupportTicketService(db)
    updated_ticket = ticket_service.update(ticket_id, support_ticket)
    if not updated_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return updated_ticket


@router.delete("/support-tickets/{ticket_id}")
def delete_support_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket_service = SupportTicketService(db)
    deleted = ticket_service.delete(ticket_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {"detail": "Ticket deleted successfully"}

@router.get("/support-tickets/by-tenant/{tenant_id}", response_model=List[SupportTicket])
def get_support_tickets_by_tenant_id(tenant_id: int, db: Session = Depends(get_db)):
    ticket_service = SupportTicketService(db)
    tickets = ticket_service.get_by_tenant_id(tenant_id)
    return tickets

