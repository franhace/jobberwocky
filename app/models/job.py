from typing import List

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from app.models.base import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    salary = Column(Float, nullable=False)
    skills = Column(JSON, default=list)
    source = Column(String, default="internal")

    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=True)

    company = relationship("Company", back_populates="jobs",foreign_keys=[company_id], uselist=False )
    country = relationship("Country", back_populates="jobs", foreign_keys=[country_id], uselist=False)

