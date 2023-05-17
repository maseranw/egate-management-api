from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi_jwt_auth import AuthJWT
from database import get_db
from schemas.support_ticket_type import SupportTicketTypeCreate, SupportTicketTypeUpdate, SupportTicketTypeResponse
from services.support_ticket_type_service import SupportTicketTypeService

router = APIRouter(prefix="/api", tags=["SupportTicketType"])


@router.post("/support-ticket-type", response_model=SupportTicketTypeResponse)
def create_support_ticket_type(support_ticket_type: SupportTicketTypeCreate, db: Session = Depends(get_db),auth: AuthJWT = Depends()):
    auth.jwt_required()
    db_support_ticket_type = SupportTicketTypeService(db).create(support_ticket_type)
    return db_support_ticket_type


@router.get("/support-ticket-type/{id}", response_model=SupportTicketTypeResponse)
def get_support_ticket_type(id: int, db: Session = Depends(get_db),auth: AuthJWT = Depends()):
    auth.jwt_required()
    db_support_ticket_type = SupportTicketTypeService(db).get(id)
    if db_support_ticket_type is None:
        raise HTTPException(status_code=404, detail="Support ticket type not found")
    return db_support_ticket_type


@router.get("/support-ticket-type", response_model=List[SupportTicketTypeResponse])
def get_all_support_ticket_types(db: Session = Depends(get_db),auth: AuthJWT = Depends()):
    auth.jwt_required()
    return SupportTicketTypeService(db).get_all()


@router.put("/support-ticket-type/{id}", response_model=SupportTicketTypeResponse)
def update_support_ticket_type(id: int, support_ticket_type: SupportTicketTypeUpdate, db: Session = Depends(get_db),auth: AuthJWT = Depends()):
    auth.jwt_required()
    db_support_ticket_type = SupportTicketTypeService(db).get(id)
    if db_support_ticket_type is None:
        raise HTTPException(status_code=404, detail="Support ticket type not found")
    return SupportTicketTypeService(db).update(id, support_ticket_type)


@router.delete("/support-ticket-type/{id}")
def delete_support_ticket_type(id: int, db: Session = Depends(get_db),auth: AuthJWT = Depends()):
    auth.jwt_required()
    db_support_ticket_type = SupportTicketTypeService(db).get(id)
    if db_support_ticket_type is None:
        raise HTTPException(status_code=404, detail="Support ticket type not found")
    SupportTicketTypeService(db).delete(id)
    return {"message": "Support ticket type deleted successfully"}
