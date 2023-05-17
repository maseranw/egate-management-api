from typing import List
from sqlalchemy.orm import Session
from schemas.user_role import UserRoleCreate, UserRoleResponse
from repositories.user_role_repository import UserRoleRepository

class UserRoleService:
    def __init__(self, session: Session):
        self.user_role_repository = UserRoleRepository(session)

    def create_user_role(self, new_role: UserRoleCreate) -> UserRoleResponse:
        role = self.user_role_repository.create_user_role(new_role)
        return UserRoleResponse(id=role.id, name=role.name)

    def get_user_role(self, role_id: int) -> UserRoleResponse:
        role = self.user_role_repository.get_user_role(role_id)
        return UserRoleResponse(id=role.id, name=role.name) if role else None

    def get_all_user_roles(self) -> List[UserRoleResponse]:
        roles = self.user_role_repository.get_all_user_roles()
        return [UserRoleResponse(id=role.id, name=role.name) for role in roles]

    def delete_user_role(self, role_id: int) -> bool:
        return self.user_role_repository.delete_user_role(role_id)
