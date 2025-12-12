from sqlalchemy.orm import Session
from typing import List, Optional

from models.models import Candidate
from schemas.schemas import CandidateCreate, CandidateUpdate


def create_candidate_repo(db: Session, candidate_data: CandidateCreate):
    candidate = Candidate(
        CandidateName=candidate_data.CandidateName,
        TotalExperience=candidate_data.TotalExperience,
        SkillSet=candidate_data.SkillSet,
        CurrentOrganization=candidate_data.CurrentOrganization,
        NoticePeriod=candidate_data.NoticePeriod,
        Feedback=candidate_data.Feedback,
        Remarks=candidate_data.Remarks,
        ClientName=candidate_data.ClientName,
        ClientManagerName=candidate_data.ClientManagerName,
        InterviewerId=candidate_data.InterviewerId,
        ResumePath=candidate_data.ResumePath
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



def bulk_insert_candidates(db: Session, candidates: List[dict]):
    objects = [Candidate(**c) for c in candidates] #loops over each candidate dictionary.unpacks dictionary keys into model fields.objects becomes a list of Candidate ORM objects
    db.bulk_save_objects(objects)
    db.commit()
    return len(objects)                            #Returns the number of candidates inserted


