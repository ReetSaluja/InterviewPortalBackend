# services/candidate_service.py
from sqlalchemy.orm import Session
from typing import List, Optional, Dict,Any 
from fastapi import UploadFile
import os
import time
import shutil


from schemas.schemas import CandidateCreate, CandidateUpdate
from models.models import Candidate
from repository.candidate_repository import (
    create_candidate_repo,
    update_candidate_repo,
    get_candidate_by_id_repo,
    bulk_insert_candidates
)



UPLOAD_DIR = "uploads"                                 #folder name to store resumes.This folder will be created in the backend project directory if it doesn’t exist.
 
def create_candidate_service(
    db: Session,
    form_data: Dict,
    resume: Optional[UploadFile],
) -> Candidate:
    
   
    resume_path: Optional[str] = None                   # default: no file
 
    
    if resume is not None and resume.filename:          # Only try to save the file if it exists and has a name
        os.makedirs(UPLOAD_DIR, exist_ok=True)          #Create the folder uploads if it doesn’t already exist.
 
        
        timestamp = int(time.time())                    # create unique filenameGet current Unix time (seconds).
        safe_name = f"{timestamp}_{resume.filename}"    #Build a unique filename
        file_path = os.path.join(UPLOAD_DIR, safe_name) #build full file path
 
        
        with open(file_path, "wb") as buffer:           #Open the file in write-binary mode.A resume can be: text → .pdf, .docx, .pptx, .png, .jpg.if not python will treat pdf as text.
            shutil.copyfileobj(resume.file, buffer)     #Copy everything inside resume.file and write it into buffer.
 
        resume_path = f"{UPLOAD_DIR}/{safe_name}"                      # this is what we save in DB
 
    
    candidate_data = CandidateCreate(                   # build Pydantic model
        **form_data,                                    #Unpacks dictionary form_data to match fields in CandidateCreate.
        ResumePath=resume_path,
    )
 
    return create_candidate_repo(db, candidate_data)
 


def get_all_candidates_service(db: Session) -> List[Candidate]:
    return db.query(Candidate).all()

def update_candidate_service(db: Session, candidate_id: int, candidate_data: CandidateUpdate) -> Optional[Candidate]:
    # Here you can add extra business logic or validation later
    return update_candidate_repo(db, candidate_id, candidate_data)

def get_candidate_by_id_service(db: Session, candidate_id: int) -> Optional[Candidate]:
    return get_candidate_by_id_repo(db, candidate_id)

def get_candidates_paginated_service(
    db: Session,
    skip: int = 0,
    limit: int = 10
) -> List[Candidate]:
    
    # Validate pagination parameters
    if skip < 0:
        skip = 0
    if limit <= 0 or limit > 100:                   # Max limit to prevent performance issues
        limit = 10
    
    totalcount = db.query(Candidate).count()
    return {
        "totalcount": totalcount,
        "candidates": db.query(Candidate).offset(skip).limit(limit).all()
    }
    
    
    
def import_candidates_service(db: Session, rows: List[Dict[str, Any]]):
    if not rows:                                      #Checks if Excel file was empty or frontend sent []
        raise ValueError("No data to import")

    cleaned_rows = []                                  #This will store validated & cleaned rows,Only rows in this list will be inserted
                                                       #Extracts only fields that exist in the DB,Ignores extra Excel columns safely
    for r in rows:
        data = {
            "CandidateName": r.get("CandidateName"),
            "TotalExperience": r.get("TotalExperience"),
            "SkillSet": r.get("SkillSet"),
            "CurrentOrganization": r.get("CurrentOrganization"),
            "NoticePeriod": r.get("NoticePeriod"),
            "Feedback": r.get("Feedback"),
            "Remarks": r.get("Remarks"),
            "ClientName": r.get("ClientName"),
            "ClientManagerName": r.get("ClientManagerName"),
            "InterviewerId": r.get("InterviewerId"),
            "ResumePath": r.get("ResumePath"),
        }
        # Required fields check
        required = [
            "CandidateName",
            "TotalExperience",
            "SkillSet",
            "CurrentOrganization",
            "NoticePeriod",
        ]

        for field in required:
            if not data[field]:
                raise ValueError(f"Missing required field: {field}")

        # normalize empty strings
        for k, v in data.items():                         #Loop through each field:k = field name ("Feedback")v = value ("")
            if isinstance(v, str) and v.strip() == "":
                data[k] = None                            #Replace empty string with None.

    
        cleaned_rows.append(data)

    inserted = bulk_insert_candidates(db, cleaned_rows)
    return {"message": "Imported successfully", "inserted": inserted}
        "candidates": db.query(Candidate).order_by(Candidate.id).offset(skip).limit(limit).all()
    }
