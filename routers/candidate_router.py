# routers/candidate_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas import CandidateCreate
from services.candidate_service import (
    create_candidate_service
)

router = APIRouter(
    prefix="/candidates",
    tags=["candidates"],
)


@router.post("/", response_model=CandidateCreate)
def create_candidate(candidate: CandidateCreate, db: Session = Depends(get_db)):
    return create_candidate_service(db, candidate)

