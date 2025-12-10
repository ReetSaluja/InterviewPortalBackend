# repository/user_repository.py
from typing import Optional, List
from sqlalchemy.orm import Session
from models.models import User, RoleEnum
from schemas.schemas import UserCreate

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


def get_users_by_role(db: Session, role: RoleEnum) -> List[User]:
    return db.query(User).filter(User.role == role).all()
