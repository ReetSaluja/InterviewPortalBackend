# services/candidate_service.py
from sqlalchemy.orm import Session
from typing import List,Dict,Optional
import os,shutil,time
from fastapi import UploadFile

from schemas import CandidateCreate
from models import Candidate
from repository.candiate_repository import create_candidate_repo

UPLOAD_DIR = "uploads" #folder name to store resumes.This folder will be created in the backend project directory if it doesn’t exist.

def create_candidate_service(
    db: Session,
    form_data: Dict,
    resume: Optional[UploadFile],
) -> Candidate:
    """
    If resume is provided, save it to uploads/ and set ResumePath.
    If no resume, keep ResumePath = None.
     Then build CandidateCreate and pass to repo.
    """

    # default: no file
    resume_path: Optional[str] = None

    # Only try to save the file if it exists and has a name
    if resume is not None and resume.filename:
        os.makedirs(UPLOAD_DIR, exist_ok=True) #Create the folder uploads if it doesn’t already exist.

        # create unique filename
        timestamp = int(time.time()) #Get current Unix time (seconds).
        safe_name = f"{timestamp}_{resume.filename}" #Build a unique filename
        file_path = os.path.join(UPLOAD_DIR, safe_name) #build full file path

        # save file to disk
        with open(file_path, "wb") as buffer: #Open the file in write-binary mode.A resume can be: text → .pdf, .docx, .pptx, .png, .jpg.if not python will treat pdf as text.
            shutil.copyfileobj(resume.file, buffer) #Copy everything inside resume.file and write it into buffer.

        resume_path = file_path  # this is what we save in DB

    # build Pydantic model
    candidate_data = CandidateCreate( 
        **form_data,#Unpacks dictionary form_data to match fields in CandidateCreate.
        ResumePath=resume_path,
    )

    return create_candidate_repo(db, candidate_data)


def get_all_candidates_service(db: Session) -> List[Candidate]:
    return db.query(Candidate).all()


