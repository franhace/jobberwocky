from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from sqlalchemy.orm import relationship


class Country(BaseModel):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    jobs = relationship("Job", back_populates="countryies")