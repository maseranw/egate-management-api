from pydantic import BaseModel, BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

JWT_SECRET = os.environ.get('JWT_SECRET')
    
class JWTSettings(BaseSettings):
    authjwt_secret_key: str = JWT_SECRET
    