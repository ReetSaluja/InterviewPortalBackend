from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from pydantic import EmailStr
from schemas.schemas import UserCreate,UserRead,UserLogin,UserPasswordUpdate
from db.database import get_db
from services.auth_service import (
    register_user_service,
    login_user_service,
    get_users_by_role_service,
    update_password_service,
)
from repository.user_repository import get_user_by_email
 
 
router = APIRouter(prefix="/auth", tags=["auth"])
 
 
# -------------------------------------------------
# REGISTER USER
# -------------------------------------------------
@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return register_user_service(db, user)
 
 
# -------------------------------------------------
# LOGIN USER
# -------------------------------------------------
@router.post("/login", response_model=UserRead)
def login_user(login_data: UserLogin, db: Session = Depends(get_db)):
    user = login_user_service(db, login_data)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return user
 
 
# -------------------------------------------------
# GET USERS BY ROLE (ADMIN / INTERVIEWER)
# -------------------------------------------------
@router.get("/users", response_model=List[UserRead])
def get_users_by_role(
    role: str = Query(..., description="Role to filter users (admin or interviewer)"),
    db: Session = Depends(get_db),
):
    users = get_users_by_role_service(db, role)
    return users
 
 
# -------------------------------------------------
# CHECK EMAIL EXISTS (USED IN FORGOT PASSWORD PAGE)
# -------------------------------------------------
@router.get("/check-email")
def check_email(
    email: EmailStr = Query(..., description="Email to verify"),
    db: Session = Depends(get_db)
):
    """
    Check if an email exists in the database.
    
    Returns:
        { "exists": true }  - If email exists in DB
        { "exists": false } - If email not found
    """
    user = get_user_by_email(db, email)
    
    if user:
        return {"exists": True}
    
    return {"exists": False}


# -------------------------------------------------
# UPDATE PASSWORD
# -------------------------------------------------
@router.put("/update-password", response_model=UserRead)
def update_password(
    password_data: UserPasswordUpdate,
    db: Session = Depends(get_db)
):
    """
    Update user password by email.
    
    Returns:
        Updated user information (without password)
    """
    return update_password_service(db, password_data)
