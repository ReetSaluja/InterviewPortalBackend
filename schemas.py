from pydantic import BaseModel

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