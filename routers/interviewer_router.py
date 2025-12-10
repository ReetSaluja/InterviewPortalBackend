from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session  
from typing import List
from db.database import get_db
from services.Interviewer_service import fetch_all_interviewers_service
from schemas.schemas import InterviewerSchema
router = APIRouter(
    prefix="/interviewers", 
    tags=["Interviewers"]
)
@router.get("/", response_model=List[InterviewerSchema])
def get_all_interviewers(db: Session = Depends(get_db)):
    interviewers = fetch_all_interviewers_service(db)
    return interviewers