# repository/user_repository.py
from typing import Optional
from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate

def create_user_repo(db: Session, user_data: UserCreate) -> User:
    user = User(
        email=user_data.email,
        password=user_data.password,
        role=user_data.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user_repo(db: Session, email: str, password: str) -> Optional[User]:
    return db.query(User).filter(User.email == email, User.password == password).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()
