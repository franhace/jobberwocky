from pydantic import BaseModel

class JobCreate(BaseModel):
    title: str
    description: str
    company: str

class Job(JobCreate):
    id: int

    class Config:
        orm_mode = True