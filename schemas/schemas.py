from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str  # "admin" or "interviewer"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserPasswordUpdate(BaseModel):
    email: EmailStr
    new_password: str


class UserRead(BaseModel):
    id: int
    email: EmailStr
    role: str
    
    class Config:
        from_attributes = True
    
    

class CandidateCreate(BaseModel):
    id:Optional[int]=None
    CandidateName: str
    TotalExperience: str
    SkillSet: str
    CurrentOrganization: str
    NoticePeriod: str
    Feedback: Optional[str] = None  
    Remarks: Optional[str] = None
    ClientName: Optional[str] = None
    ClientManagerName: Optional[str] = None    
    InterviewerId: Optional[int] = None
    ResumePath: Optional[str] = None
 
   
    

    class Config:
        from_attributes = True

class CandidateUpdate(BaseModel):
    CandidateName: Optional[str] = None
    TotalExperience: Optional[str] = None
    SkillSet: Optional[str] = None
    CurrentOrganization: Optional[str] = None
    NoticePeriod: Optional[str] = None
    Feedback: Optional[str] = None   
    Remarks: Optional[str] = None
    
    class Config:
        from_attributes = True
        
class InterviewerSchema(BaseModel):
    id: int
    InterviewerName: str
    PrimarySkill: str
    Proficiency: str

    class Config:
        from_attributes = True