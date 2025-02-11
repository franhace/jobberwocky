from sqlalchemy.orm import Session
from app.models.job import Job
from app.services.job_service import service_get_job_by_id, service_create_job

def test_get_job_by_id(db: Session):
    job = Job(title="Test Job", description="Test Description", salary=50000, company_id=1, country_id=1)
    db.add(job)
    db.commit()
    fetched_job = service_get_job_by_id(db, job.id)
    assert fetched_job.id == job.id
    assert fetched_job.title == "Test Job"

def test_create_job(db: Session):
    job_data = {
        "title": "Backend Engineer",
        "description": "Python expert needed right away",
        "company_id": 1,
        "salary": 80000,
        "country_id": 1,
        "skills": ["AWS", "Docker"]
    }
    job = service_create_job(db, job_data)
    assert job.id is not None
    assert job.title == "Backend Engineer"
