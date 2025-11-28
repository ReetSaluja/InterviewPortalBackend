# models.py
from sqlalchemy import Column, Integer, String
from database import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    CandidateName = Column(String, nullable=False)
    TotalExperience = Column(String, nullable=False)
    SkillSet = Column(String, nullable=False)
    CurrentOrganization = Column(String, nullable=False)
    NoticePeriod = Column(String, nullable=False)
