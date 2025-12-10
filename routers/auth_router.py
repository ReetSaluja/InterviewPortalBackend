# routers/auth_router.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from db.database import get_db
from schemas.schemas import UserCreate, UserLogin, UserRead
from services.auth_service import register_user_service, login_user_service, get_users_by_role_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return register_user_service(db, user)


@router.post("/login", response_model=UserRead)
def login_user(login_data: UserLogin, db: Session = Depends(get_db)):
    user = login_user_service(db, login_data)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return user


@router.get("/users", response_model=List[UserRead])
def get_users_by_role(
    role: str = Query(..., description="Role to filter users (admin or interviewer)"),
    db: Session = Depends(get_db)
):
    users = get_users_by_role_service(db, role)
    return users
