from typing import Optional

from fastapi import APIRouter, Query
from app.models.job import Job, JobCreate
from app.services.job_service import create_job as service_create_job, get_jobs as service_get_jobs

router = APIRouter()

@router.post("/jobs/", response_model=Job, status_code=201)
def create_job(job: JobCreate):
    new_job = service_create_job(job.model_dump())
    return new_job

@router.get("/jobs/", response_model=list[Job])
def get_job(description: Optional[str] = Query(None)):
    jobs = service_get_jobs()
    if description:
        jobs = [job for job in jobs if description.lower() in job.description.lower()]

    return jobs