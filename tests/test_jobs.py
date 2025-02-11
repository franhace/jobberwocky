from sqlalchemy.orm import Session
from app.models.job import Job
from app.services.job_service import service_create_job


def test_duplicate_job(db: Session):
    job = Job(title="Job 1", description="Description for Job 1")
    db.add(job)
    db.commit()
    duplicate_job = Job(title="Job 1", description="Description for Job 1")

    try:
        db.add(duplicate_job)
        db.commit()
        assert False, "Expected an integrity error for duplicate job"
    except Exception as e:
        assert "duplicate key value violates unique constraint" in str(e)

def test_create_job(db: Session):
    job_data = {
        "title": "Backend Engineer",
        "description": "Python expert needed right away",
        "company": "Avature",
        "salary": 80000,
        "country": "Argentina",
        "skills": ["AWS", "Docker"]
    }
    job = service_create_job(db, job_data)
    assert job.id is not None
    assert job.title == "Backend Engineer"

