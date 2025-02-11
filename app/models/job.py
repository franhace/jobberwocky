from typing import List

from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship


class Job(BaseModel):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    salary = Column(Integer, nullable=False)
    skills = Column(JSON, default=[])

    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)

    company = relationship("Company", back_populates="jobs")
    country = relationship("Country", back_populates="jobs")