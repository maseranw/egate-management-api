from typing import List
from sqlalchemy.orm import Session
from schemas.token import Token
from repositories.token_repository import TokenRepository

class TokenService:
    def __init__(self, session: Session):
        self.token_repository = TokenRepository(session)

    def create_token(self, visitor_id: str) -> Token:
        return self.token_repository.create_token(visitor_id)

    def get_token_by_id(self, token_id: int) -> Token:
        return self.token_repository.get_token_by_id(token_id)

    def get_tokens_by_visitor_id(self, visitor_id: str) -> List[Token]:
        return self.token_repository.get_tokens_by_visitor_id(visitor_id)
    
    def get_tokens_by_user_id(self, user_id: str,) -> List[Token]:
        return self.token_repository.get_tokens_by_user_id(user_id)