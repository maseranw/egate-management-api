from psycopg2 import IntegrityError
import pytz
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from database import Tenant
from schemas.tenant import TenantUpdate, TenantCreate
import secrets
import string


class TenantRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_tenant(self, tenant: TenantCreate) -> Tenant:
        while True:
            try:
                code = self.generate_random_code()
                
                sa_timezone = pytz.timezone('Africa/Johannesburg')
                today = datetime.now().astimezone(sa_timezone)
                
                existing_tenant = self.get_tenant_by_code(code)
                if not existing_tenant:
                    db_tenant = Tenant(**tenant.dict(), code=code, create_date=today)
                    self.session.add(db_tenant)
                    self.session.commit()
                    self.session.refresh(db_tenant)
                    return db_tenant
            except IntegrityError:
                # If an IntegrityError occurs, indicating a code collision, continue the loop to generate a new code
                self.session.rollback()
            # Handle the case when a unique code cannot be generated after multiple attempts
            raise ValueError("Unable to generate a unique code")

    def get_tenant_by_id(self, tenant_id: int) -> Tenant:
        tenant = self.session.query(Tenant).filter(Tenant.id == tenant_id).first()
        if not tenant:
            raise self.CustomException(f"Tenant not found with ID: {tenant_id}")
        return tenant
    
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
    
    
    class CustomException(Exception):
        pass