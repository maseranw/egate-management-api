from sqlalchemy.orm import Session
from database import UserRole
from schemas.user_role import UserRoleCreate

class UserRoleRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_user_role(self, role_id: int):
        return self.session.query(UserRole).filter(UserRole.id == role_id).first()

    def get_user_role_by_name(self, role_name: str):
        return self.session.query(UserRole).filter(UserRole.name == role_name).first()

    def get_all_user_roles(self):
        return self.session.query(UserRole).all()

    def create_user_role(self, role: UserRoleCreate):
        db_role = UserRole(name=role.name)
        self.session.add(db_role)
        self.session.commit()
        self.session.refresh(db_role)
        return db_role

    def delete_user_role(self, role_id: int):
        db_role = self.get_user_role(role_id)
        if db_role:
            self.session.delete(db_role)
            self.session.commit()
            return True
        return False
