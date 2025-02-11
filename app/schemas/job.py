from typing import List

from pydantic import BaseModel

from app.schemas.company import Company
from app.schemas.country import Country


class JobBase(BaseModel):
    title: str
    description: str
    salary: float
    skills: List[str] = []


class JobCreate(JobBase):
    company: str
    country: str

class Job(JobBase):
    id: int
    company: Company
    country: Country

    class Config:
        orm_mode = True