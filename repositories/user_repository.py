import datetime
from typing import List
import bcrypt
from sqlalchemy.orm import Session
from database import User
from schemas.user import UserCreate


class UserRepository:
    def __init__(self, session: Session):
        self.session = session
        self.salt = bcrypt.gensalt()

    # ----------- Create User--------------
    def create_user(self, user: UserCreate):

        existing_user = self.get_user_by_username(user.username)
        if existing_user:
            raise ValueError("Username already exists")
        
        password = user.password.encode("utf-8")
        hashed_password = bcrypt.hashpw(password,self.salt).decode("utf-8")
        user.password = hashed_password

        db_user = User(**user.dict(), create_date=datetime.datetime.now())
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user


    # ----------- Update user details--------------
    def update_user(self, user_id: int, updated_user: User) -> User:
        # get the user from the database
        user = self.get_user(user_id)

        if not user:
            return None

        # update the user's fields
        user.username = updated_user.username
        user.firstname = updated_user.firstname
        user.lastname = updated_user.lastname
        user.phone = updated_user.phone
        user.email = updated_user.email
        user.update_date = datetime.datetime.now()

        self.session.commit()

        return user
    
    # ----------- Update user password--------------
    def update_user_password(self, user_id: int, updated_user: User) -> User:
        # get the user from the database
        user = self.get_user(user_id)

        # if the password has changed, hash and store the new password
        if user.password != updated_user.password:
            password = updated_user.password.encode("utf-8")
            hashed_password = bcrypt.hashpw(password, self.salt).decode("utf-8")
            user.password = hashed_password

        self.session.commit()

        return user
    
    # ----------- Get user by username--------------
    def get_user_by_username(self, username: str) -> User:
        return self.session.query(User).filter(User.username == username).first()
    
    def get_user(self, user_id: int):
        return self.session.query(User).filter(User.id == user_id).first()

    # ----------- Get all users--------------
    def get_users(self) -> List[User]:
        return self.session.query(User).all()
    
    # ----------- Authenticate User--------------
    def authenticate_user(self, username: str, password: str) -> int:
        # retrieve user from database by username
        user = self.get_user_by_username(username)

        # check password
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return user.id
        else:
            return None