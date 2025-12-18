from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from models.models import Interviewer, User, RoleEnum
from schemas.schemas import InterviewerCreate

def create_interviewer_repo(db: Session, interviewer_data: InterviewerCreate):
    # Check if email already exists in users table or interviewer table
    existing_user = db.query(User).filter(User.email == interviewer_data.Email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists in users table")
    
    existing_interviewer = db.query(Interviewer).filter(Interviewer.Email == interviewer_data.Email).first()
    if existing_interviewer:
        raise HTTPException(status_code=400, detail="Email already exists for another interviewer")
    
    # Create interviewer
    interviewer = Interviewer(
        InterviewerName=interviewer_data.InterviewerName,
        Email=interviewer_data.Email,
        PhoneNumber=interviewer_data.PhoneNumber,
        Designation=interviewer_data.Designation,
        PrimarySkill=interviewer_data.PrimarySkill,
        TotalExperience=interviewer_data.TotalExperience,
        CarrerLevel=interviewer_data.CarrerLevel
    )
    db.add(interviewer)
    db.flush()  # Flush to get the interviewer ID if needed
    
    # Create user login automatically
    user = User(
        email=interviewer_data.Email,
        password="string",
        role=RoleEnum.interviewer
    )
    db.add(user)
    
    try:
        db.commit()
        db.refresh(interviewer)
        return interviewer
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")

def get_all_interviewers(db: Session):
    return db.query(Interviewer).all()