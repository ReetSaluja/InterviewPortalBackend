from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str  # "admin" or "interviewer"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    email: EmailStr
    role: str
    
    class Config:
        orm_mode = True


class CandidateCreate(BaseModel):
    CandidateName: str
    TotalExperience: str
    SkillSet: str
    CurrentOrganization: str
    NoticePeriod: str
    
class CandidateRead(CandidateCreate):
    id: int

    class Config:
        orm_mode = True