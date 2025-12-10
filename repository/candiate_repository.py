
from sqlalchemy.orm import Session
from typing import List

from models import Candidate
from schemas import CandidateCreate


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

