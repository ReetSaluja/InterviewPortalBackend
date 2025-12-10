# services/auth_service.py
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from models.models import RoleEnum
from repository.user_repository import create_user_repo, login_user_repo, get_user_by_email, get_users_by_role
from schemas.schemas import UserCreate, UserLogin

def register_user_service(db: Session, user_data: UserCreate):
    # Check duplicate email
    existing = get_user_by_email(db, user_data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    try:
        return create_user_repo(db, user_data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")


def login_user_service(db: Session, login_data: UserLogin):
    return login_user_repo(db, login_data.email, login_data.password)


def get_users_by_role_service(db: Session, role: str):
    try:
        role_enum = RoleEnum(role)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid role. Must be one of: {[r.value for r in RoleEnum]}")
    return get_users_by_role(db, role_enum)
