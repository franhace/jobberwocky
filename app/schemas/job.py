from typing import List, Optional
from pydantic import BaseModel, condecimal
from app.schemas.company import Company
from app.schemas.country import Country

class JobBase(BaseModel):
    title: str
    salary: condecimal(gt=0)
    skills: List[str] = []
    source: str

class JobCreate(JobBase):
    description: str
    company: str
    country: str

class Job(JobBase):
    id: Optional[int]
    company: Optional[Company]
    country: Optional[Country]

    class Config:
        orm_mode = True
        from_attributes = True

class ExternalJob(JobBase):
    country: Optional[Country]

    class Config:
        orm_mode = True
        from_attributes = True
