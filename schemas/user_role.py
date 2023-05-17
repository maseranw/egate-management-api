from pydantic import BaseModel

class UserRoleBase(BaseModel):
    name: str

class UserRoleCreate(UserRoleBase):
    pass

class UserRoleResponse(UserRoleBase):
    id: int

    class Config:
        orm_mode = True
        
class UserRole(UserRoleBase):
    id: int
    name: str
    class Config:
        orm_mode = True