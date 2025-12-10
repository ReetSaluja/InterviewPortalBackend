# routers/candidate_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas import CandidateCreate, CandidateUpdate
from services.candidate_service import (
    create_candidate_service,
    get_all_candidates_service,
    update_candidate_service,
)

router = APIRouter(
    prefix="/candidates",
    tags=["candidates"],
)


@router.post("/", response_model=CandidateCreate)
def create_candidate(candidate: CandidateCreate, db: Session = Depends(get_db)):
    return create_candidate_service(db, candidate)

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

