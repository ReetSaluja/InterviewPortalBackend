from sqlalchemy.orm import Session

from repository.interview_repository import get_all_interviewers

def fetch_all_interviewers_service(db: Session):
    return get_all_interviewers(db)