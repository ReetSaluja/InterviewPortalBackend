from sqlalchemy.orm import Session
from typing import List, Optional

from models.models import Candidate
from schemas.schemas import CandidateCreate, CandidateUpdate


def create_candidate_repo(db: Session, candidate_data: CandidateCreate) -> Candidate:
    candidate = Candidate(
        CandidateName=candidate_data.CandidateName,
        TotalExperience=candidate_data.TotalExperience,
        SkillSet=candidate_data.SkillSet,
        CurrentOrganization=candidate_data.CurrentOrganization,
        NoticePeriod=candidate_data.NoticePeriod,
        Feedback=candidate_data.Feedback,
        Remarks=candidate_data.Remarks
    )
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return candidate

def get_candidate_by_id_repo(db: Session, candidate_id: int) -> Optional[Candidate]:
    return db.query(Candidate).filter(Candidate.id == candidate_id).first()

def update_candidate_repo(db: Session, candidate_id: int, candidate_data: CandidateUpdate) -> Optional[Candidate]:
    candidate = get_candidate_by_id_repo(db, candidate_id)
    if not candidate:
        return None
    
    # Update only the fields that are provided
    update_data = candidate_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(candidate, field, value)
    
    db.commit()
    db.refresh(candidate)
    return candidate

