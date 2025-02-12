from typing import Optional, Union

import httpx
from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.job import Job, JobCreate, ExternalJob
from app.services.job_service import (
    service_get_jobs,
    service_get_job_by_id, service_create_job, normalize_external_jobs, merge_jobs, fetch_external_jobs, EXTERNAL_SOURCE
)

router = APIRouter()
routes = router


@router.get("/", response_model=list[Union[Job, ExternalJob]])
async def search_jobs(
    description: Optional[str] = Query(None),
    country: Optional[str] = Query(None),
    salary_min: Optional[int] = Query(None, ge=0),
    salary_max: Optional[int] = Query(None, ge=0),
    skills: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    internal_jobs = service_get_jobs(
        db,
        title=description,
        country=country,
        salary_min=salary_min,
        salary_max=salary_max,
        skills=skills
    )

    external_params = {
        "description": description,
        "country": country,
        "salary_min": salary_min,
        "salary_max": salary_max,
        "skills": skills
    }
    external_data = await fetch_external_jobs(external_params)
    external_jobs = normalize_external_jobs(external_data, db)

    combined_jobs = merge_jobs(internal_jobs, external_jobs)
    return [Job.model_validate(job) if hasattr(job, "__table__") else ExternalJob.model_validate(job) for job in combined_jobs]



@router.get("/{job_id}", response_model=Job)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = service_get_job_by_id(db, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.post("/", response_model=Job, status_code=201)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    try:
        new_job = service_create_job(db, job.model_dump())
        return new_job
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/health/", response_model=dict)
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1")).fetchone()
        return {"status": "healthy"}
    except Exception:
        raise HTTPException(status_code=500, detail="Database connection failed")


@router.get("/health/external")
async def check_external_health():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                EXTERNAL_SOURCE,
                params={"limit": 1},
                timeout=3.0
            )
            response.raise_for_status()
            return {"status": "healthy", "external_source": "jobberwocky-extra-source"}
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        raise HTTPException(status_code=503, detail=f"External source is unavailable: {e}")