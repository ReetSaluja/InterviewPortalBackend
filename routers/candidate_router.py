# routers/candidate_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from db.database import get_db
from schemas.schemas import CandidateCreate
from services.candidate_service import (
    create_candidate_service,
    get_all_candidates_service,
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


# get candidates by pagination
@router.get("/paginated", response_model=List[CandidateCreate])
def get_candidates_paginated(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    candidates = db.query(CandidateCreate).offset(skip).limit(limit).all()
    return candidates

