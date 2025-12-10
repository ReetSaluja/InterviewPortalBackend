# models.py
from sqlalchemy import Column, Integer, String, Enum
from db.database import Base
import enum

class RoleEnum(str, enum.Enum):
    admin = "admin"
    interviewer = "interviewer"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    password = Column(String, nullable=False) 
    role = Column(Enum(RoleEnum), default=RoleEnum.interviewer, nullable=False)

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    CandidateName = Column(String, nullable=False)
    TotalExperience = Column(String, nullable=False)
    SkillSet = Column(String, nullable=False)
    CurrentOrganization = Column(String, nullable=False)
    NoticePeriod = Column(String, nullable=False)
    Feedback = Column(String, nullable=True)
    Remarks = Column(String, nullable=True)
    
    
class Interviewer(Base):
    __tablename__ = "interviewer"
    
    id=Column(Integer, primary_key=True, index=True)
    InterviewerName=Column(String,nullable=False)
    PrimarySkill=Column(String,nullable=False)
    Proficiency=Column(Integer,nullable=False)
    
    
    

    



