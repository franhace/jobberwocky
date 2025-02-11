from typing import List

from pydantic import BaseModel, condecimal

from app.schemas.company import Company
from app.schemas.country import Country


class JobBase(BaseModel):
    title: str
    description: str
    salary: condecimal(gt=0)
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