# services/candidate_service.py
from sqlalchemy.orm import Session
from typing import List, Optional

from schemas import CandidateCreate, CandidateUpdate
from models import Candidate
from repository.candiate_repository import (
    create_candidate_repo,
    update_candidate_repo,
    get_candidate_by_id_repo
)



def create_candidate_service(db: Session, candidate_data: CandidateCreate) -> Candidate:
    # Here you can add extra business logic or validation later
    return create_candidate_repo(db, candidate_data)


def get_all_candidates_service(db: Session) -> List[Candidate]:
    return db.query(Candidate).all()

def update_candidate_service(db: Session, candidate_id: int, candidate_data: CandidateUpdate) -> Optional[Candidate]:
    # Here you can add extra business logic or validation later
    return update_candidate_repo(db, candidate_id, candidate_data)

def get_candidate_by_id_service(db: Session, candidate_id: int) -> Optional[Candidate]:
    return get_candidate_by_id_repo(db, candidate_id)

