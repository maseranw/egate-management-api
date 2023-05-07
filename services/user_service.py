from typing import List
import bcrypt
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserUpdate
from database import User
from repositories.user_repository import UserRepository

class UserService:
    def __init__(self, session: Session):
        self.user_repository = UserRepository(session)

    def create_user(self,new_user: UserCreate) -> User:
        return self.user_repository.create_user(new_user)

    def get_user(self, user_id: int) -> User:
        return self.user_repository.get_user(user_id)

    def get_users(self) -> List[User]:
        return self.user_repository.get_users()

    def update_user(self, user_id: int, updated_user: UserUpdate) -> User:
        return self.user_repository.update_user(user_id, updated_user)

    def update_user_password(self, user_id: int, password: str) -> User:
        updated_user = User(password=password)
        return self.user_repository.update_user_password(user_id, updated_user)
    
    def authenticate_user(self, username: str, password: str) -> int:
        # retrieve user from database by username
        user = self.user_repository.get_user_by_username(username)

        # check password
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return user.id
        else:
            return None