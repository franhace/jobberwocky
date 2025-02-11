from typing import Optional, List
from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.job import Job, JobCreate
from app.services.job_service import service_create_job, service_get_jobs, \
    service_get_job_by_id

router = APIRouter()
routes = router

@router.get("/", response_model=List[Job])
def get_jobs(
    description: Optional[str] = Query(None),
    country: Optional[str] = Query(None),
    salary_min: Optional[int] = Query(None, ge=0),
    salary_max: Optional[int] = Query(None, ge=0),
    db: Session = Depends(get_db)
):
    try:
        jobs = service_get_jobs(
            db=db,
            description=description,
            country=country,
            salary_min=salary_min,
            salary_max=salary_max
        )
        return jobs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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