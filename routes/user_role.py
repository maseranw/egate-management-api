from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.user_role import UserRoleCreate, UserRoleResponse
from services.user_role_service import UserRoleService
from fastapi_jwt_auth import AuthJWT

router = APIRouter(prefix="/api", tags=["User Roles"])

@router.post("/user-roles", response_model=UserRoleResponse)
def create_user_role(role: UserRoleCreate, db: Session = Depends(get_db),auth: AuthJWT = Depends()):
    auth.jwt_required()
    role_service = UserRoleService(db)
    created_role = role_service.create_user_role(role)
    return created_role

@router.get("/user-roles/{role_id}", response_model=UserRoleResponse)
def get_user_role(role_id: int, db: Session = Depends(get_db),auth: AuthJWT = Depends()):
    auth.jwt_required()
    role_service = UserRoleService(db)
    role = role_service.get_user_role(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.get("/user-roles", response_model=List[UserRoleResponse])
def get_all_user_roles(db: Session = Depends(get_db),auth: AuthJWT = Depends()):
    auth.jwt_required()
    role_service = UserRoleService(db)
    roles = role_service.get_all_user_roles()
    return roles

@router.delete("/user-roles/{role_id}")
def delete_user_role(role_id: int, db: Session = Depends(get_db),auth: AuthJWT = Depends()):
    auth.jwt_required()
    role_service = UserRoleService(db)
    deleted = role_service.delete_user_role(role_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"detail": "Role deleted successfully"}
