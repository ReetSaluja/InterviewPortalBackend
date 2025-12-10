# routers/candidate_router.py
from fastapi import APIRouter, Depends,Form,File,UploadFile
from sqlalchemy.orm import Session
from typing import List,Optional

from database import get_db
from schemas import CandidateCreate
from services.candidate_service import (
    create_candidate_service,
    get_all_candidates_service,
)

router = APIRouter(
    prefix="/candidates",
    tags=["candidates"],
)


@router.post("/", response_model=CandidateCreate)
def create_candidate(
    CandidateName:str=Form(...),
    TotalExperience:str=Form(...),
    SkillSet:str=Form(...),     
    CurrentOrganization:str=Form(...),
    NoticePeriod:str=Form(...),
    Feedback:Optional[str]=Form(...),
    Remarks:Optional[str]=Form(...),
    ClientName:Optional[str]=Form(...),     
    ClientManagerName:Optional[str]=Form(...),
    InterviewerId:Optional[int]=Form(...),
    resume: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    
    form_data={
        "CandidateName":CandidateName,
        "TotalExperience":TotalExperience,
        "SkillSet":SkillSet,
        "CurrentOrganization":CurrentOrganization,
        "NoticePeriod":NoticePeriod,
        "Feedback":Feedback,
        "Remarks":Remarks,
        "ClientName":ClientName,
        "ClientManagerName":ClientManagerName,
        "InterviewerId":InterviewerId
    }
    
    
    return create_candidate_service(db, form_data,resume)

@router.get("/", response_model=List[CandidateCreate])
def get_all_candidates(db: Session = Depends(get_db)):
    return get_all_candidates_service(db)

