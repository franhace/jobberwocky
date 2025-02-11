from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session, selectinload
from app.models.company import Company
from app.models.country import Country
from app.models.job import Job

def service_get_job_by_id(db: Session, job_id: int) -> Job:
    job = (
        db.query(Job)
        .options(selectinload(Job.company), selectinload(Job.country))
        .filter(Job.id == job_id)
        .first()
    )
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

def service_create_job(db: Session, job_data: dict) -> Job:
    company = db.query(Company).filter(Company.name == job_data["company"]).first()
    if not company:
        company = Company(name=job_data["company"])
        db.add(company)
        db.commit()
        db.refresh(company)

    country = db.query(Country).filter(Country.name == job_data["country"]).first()
    if not country:
        country = Country(name=job_data["country"])
        db.add(country)
        db.commit()
        db.refresh(country)

    existing_job = db.query(Job).filter(
        Job.title == job_data["title"],
        Job.company_id == company.id,
        Job.country_id == country.id
    ).first()

    if existing_job:
        raise ValueError("Job already exists.")

    job = Job(
        title=job_data["title"],
        description=job_data["description"],
        salary=job_data["salary"],
        skills=job_data["skills"],
        company_id=company.id,
        country_id=country.id
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

def service_get_jobs(
    db: Session,
    description: Optional[str] = None,
    country: Optional[str] = None,
    salary_min: Optional[int] = None,
    salary_max: Optional[int] = None
):
    query = db.query(Job).options(
        selectinload(Job.company),
        selectinload(Job.country)
    )

    if description:
        query = query.filter(Job.description.ilike(f"%{description}%"))
    if country:
        query = query.join(Country).filter(Country.name.ilike(country))
    if salary_min:
        query = query.filter(Job.salary >= salary_min)
    if salary_max:
        query = query.filter(Job.salary <= salary_max)

    return query.all()
