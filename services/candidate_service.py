# services/candidate_service.py
from sqlalchemy.orm import Session
from typing import List

from schemas import CandidateCreate
from models import Candidate
from repository.candiate_repository import create_candidate_repo



def create_candidate_service(db: Session, candidate_data: CandidateCreate) -> Candidate:
    # Here you can add extra business logic or validation later
    return create_candidate_repo(db, candidate_data)


