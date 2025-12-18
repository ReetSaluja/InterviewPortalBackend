from sqlalchemy.orm import Session

from repository.interview_repository import get_all_interviewers, create_interviewer_repo
from schemas.schemas import InterviewerCreate

def create_interviewer_service(db: Session, interviewer_data: InterviewerCreate):
    return create_interviewer_repo(db, interviewer_data)

def fetch_all_interviewers_service(db: Session):
    return get_all_interviewers(db)