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

    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)

    company = relationship("Company", back_populates="jobs")
    country = relationship("Country", back_populates="jobs")