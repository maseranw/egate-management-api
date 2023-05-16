from fastapi import HTTPException
from psycopg2 import IntegrityError
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from database import AccessCode, SupportTicket, Tenant, Visitor
from schemas.tenant import TenantUpdate, TenantCreate
import secrets
import string


class TenantRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_tenant(self, tenant: TenantCreate) -> Tenant:
        
        try:
            code = self.generate_random_code()
            db_tenant = Tenant(**tenant.dict(),code=code,create_date=datetime.utcnow())
            self.session.add(db_tenant)
            self.session.commit()
            self.session.refresh(db_tenant)
            return db_tenant
        except IntegrityError:
            self.session.rollback()

    def get_tenant_by_id(self, tenant_id: int) -> Tenant:
        return self.session.query(Tenant).filter(Tenant.id == tenant_id).first()
    
    def get_user_by_phone_and_code(self, phone: str,code: str) -> Tenant:
        return self.session.query(Tenant).filter(Tenant.code == code,Tenant.phone == phone).first()
    

    def get_tenant_by_code(self, code: str) -> Tenant:
        return self.session.query(Tenant).filter(Tenant.code == code).first()

    def get_all_tenants(self) -> List[Tenant]:
        return self.session.query(Tenant).all()

    def update_tenant(self, tenant_id: int, tenant: TenantUpdate) -> Tenant:
        db_tenant = self.get_tenant_by_id(tenant_id)
        db_tenant.firstname = tenant.firstname
        db_tenant.lastname = tenant.lastname
        db_tenant.email = tenant.email
        db_tenant.phone = tenant.phone

        # Ensure that the tenant's code is unique
        if tenant.code:
            other_tenant = self.get_tenant_by_code(tenant.code)
            if other_tenant and other_tenant.id != tenant_id:
                raise ValueError("Code already in use")
            db_tenant.code = tenant.code

        db_tenant.update_date = datetime.utcnow()
        self.session.commit()
        self.session.refresh(db_tenant)
        return db_tenant

    # def delete_tenant(self, tenant_id: int):
    #     tenant = self.session.query(Tenant).get(tenant_id)
    #     if tenant:
    #         # Delete associated data from other tables
    #         self.session.query(SupportTicket).filter(SupportTicket.tenant_id == tenant_id).delete()
    #         self.session.query(Visitor).filter(Visitor.tenant_id == tenant_id).delete()
    #         self.session.query(AccessCode).join(Visitor).filter(Visitor.tenant_id == tenant_id).delete()
            
    #         # Delete the tenant
    #         self.session.delete(tenant)
    #         self.session.commit()
            
    #         return True
    #     return False

    def delete_tenant(self, tenant_id: int) -> bool:
        tenant = self.session.query(Tenant).filter(
            Tenant.id == tenant_id).first()

        if not tenant:
            return False

        self.session.delete(tenant)
        self.session.commit()

        return True

    def generate_random_code(self, length=8):
        alphabet = string.ascii_uppercase + string.digits
        code = ''.join(secrets.choice(alphabet) for _ in range(length))
        return code
