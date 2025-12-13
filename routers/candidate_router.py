# routers/candidate_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional,Dict,Any
from fastapi import UploadFile, File, Form
from models.models import Candidate
from db.database import get_db
from schemas.schemas import CandidateCreate, CandidateUpdate
from services.candidate_service import (
    create_candidate_service,
    get_all_candidates_service,
    update_candidate_service,
    get_candidates_paginated_service,
    get_candidate_by_id_service,
    import_candidates_service
    
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
    Feedback:Optional[str]=Form(None),
    Remarks:Optional[str]=Form(None),
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

@router.put("/{candidate_id}", response_model=CandidateCreate)
def update_candidate(
    candidate_id: int,
    candidate: CandidateUpdate,
    db: Session = Depends(get_db)
):
    updated_candidate = update_candidate_service(db, candidate_id, candidate)
    if not updated_candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Candidate with id {candidate_id} not found"
        )
    return updated_candidate
 
 # get candidates by pagination
@router.get("/paginated")
def get_candidates_paginated(
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    result = get_candidates_paginated_service(db, skip=skip, limit=limit,search=search)
    # Manually exclude the interviewer nested object
    candidates_data = []
    for candidate in result["candidates"]:
        candidate_dict = {
            "id": candidate.id,
            "CandidateName": candidate.CandidateName,
            "TotalExperience": candidate.TotalExperience,
            "SkillSet": candidate.SkillSet,
            "CurrentOrganization": candidate.CurrentOrganization,
            "NoticePeriod": candidate.NoticePeriod,
            "Feedback": candidate.Feedback,
            "Remarks": candidate.Remarks,
            "ClientName": candidate.ClientName,
            "ClientManagerName": candidate.ClientManagerName,
            "InterviewerId": candidate.InterviewerId,
            "InterviewerName": candidate.InterviewerName,
            "ResumePath": candidate.ResumePath
        }
        candidates_data.append(candidate_dict)
    
    return {
        "totalcount": result["totalcount"],
        "candidates": candidates_data
    }

@router.get("/{candidate_id}")
def get_candidate_by_id(candidate_id:int,db: Session= Depends(get_db)):
    candidate=get_candidate_by_id_service(db,candidate_id)
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Candidate with id {candidate_id} not found"
        )
    return {
        "id": candidate.id,
        "CandidateName": candidate.CandidateName,
        "TotalExperience": candidate.TotalExperience,
        "SkillSet": candidate.SkillSet,
        "CurrentOrganization": candidate.CurrentOrganization,
        "NoticePeriod": candidate.NoticePeriod,
        "Feedback": candidate.Feedback,
        "Remarks": candidate.Remarks,
        "ClientName": candidate.ClientName,
        "ClientManagerName": candidate.ClientManagerName,
        "InterviewerId": candidate.InterviewerId,
        "InterviewerName": candidate.InterviewerName,
        "ResumePath": candidate.ResumePath
    }


@router.post("/import")
def import_candidates(rows: List[Dict[str, Any]], db: Session = Depends(get_db)):
    try:
        return import_candidates_service(db, rows)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

