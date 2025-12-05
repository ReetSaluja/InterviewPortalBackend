from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str  # "admin" or "candidate"


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
    id:Optional[int]=None
    CandidateName: str
    TotalExperience: str
    SkillSet: str
    CurrentOrganization: str
    NoticePeriod: str
    Feedback: Optional[str] = None   
    Remarks: Optional[str] = None
    

    class Config:
        orm_mode = True
        
class InterviewerSchema(BaseModel):
    id: int
    InterviewerName: str
    PrimarySkill: str
    Proficiency: int

    class Config:
        orm_mode = True 