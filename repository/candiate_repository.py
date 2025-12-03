
from sqlalchemy.orm import Session
from typing import List

from models import Candidate
from schemas import CandidateCreate


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

