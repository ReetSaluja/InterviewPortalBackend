# services/auth_service.py
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from repository.user_repository import create_user_repo, login_user_repo, get_user_by_email
from schemas import UserCreate, UserLogin

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
