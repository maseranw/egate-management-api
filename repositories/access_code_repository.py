from sqlalchemy import and_, exists, select
from typing import List
import bcrypt
from sqlalchemy.orm import Session, aliased, subqueryload
from database import AccessCode, User, Visitor
from datetime import datetime, date, timedelta
import random


class AccessCodeRepository:
    def __init__(self, session: Session):
        self.session = session
        self.salt = bcrypt.gensalt()

    # ----------- Create AccessCode--------------
    def create_access_code(self, visitor_id: int):
        while True:
            rand_code = random.randint(1000, 9999)
            existing_access_code = self.session.query(
                AccessCode).filter_by(code=rand_code).first()
            if not existing_access_code:
                break

        now = datetime.now()
        midnight = datetime(now.year, now.month, now.day, 23, 59, 59)

        db_access_code = AccessCode(
            visitor_id=visitor_id, code=rand_code, create_date=now, expiry_date=midnight)
        self.session.add(db_access_code)
        self.session.commit()
        self.session.refresh(db_access_code)
        return db_access_code

    def get_access_code_by_id(self, access_code_id: int):
        return self.session.query(AccessCode).filter(AccessCode.id == access_code_id).first()

    def get_access_codes_by_visitor_id(self, visitor_id: str) -> List[AccessCode]:
        return self.session.query(AccessCode).filter(AccessCode.visitor_id == visitor_id).all()

    def get_access_codes_by_tenant_id(self, tenant_id: int):
        today = datetime.now().date()
        latest_access_code_subquery = (
            self.session.query(
                AccessCode.visitor_id,
                AccessCode.create_date
            )
            .filter(
                exists().where(AccessCode.visitor_id == Visitor.id)
            )
            .order_by(AccessCode.create_date.desc())
            .limit(1)
            .subquery()
        )

        visitor_alias = aliased(Visitor)
        access_code_alias = aliased(AccessCode)

        visitors = (
            self.session.query(visitor_alias, access_code_alias.create_date)
            .join(latest_access_code_subquery, and_(latest_access_code_subquery.c.visitor_id == visitor_alias.id))
            .join(access_code_alias, and_(access_code_alias.visitor_id == latest_access_code_subquery.c.visitor_id, access_code_alias.create_date == latest_access_code_subquery.c.create_date))
            .filter(
                visitor_alias.tenant_id == tenant_id,
                access_code_alias.create_date >= today,
                access_code_alias.create_date < today + timedelta(days=1)
            )
            .all()
        )

        access_codes = [
            {
                "phone": visitor[0].phone,
                "time": visitor[0].create_date.strftime('%H:%M'),
                "access_code": visitor[0].access_codes[-1].code
            }
            for visitor in visitors
        ]

        return access_codes
