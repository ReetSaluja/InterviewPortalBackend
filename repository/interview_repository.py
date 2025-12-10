from sqlalchemy.orm import Session

from models.models import Interviewer

def get_all_interviewers(db: Session):
    return db.query(Interviewer).all()