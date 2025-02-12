import os
from typing import Optional, List
from xml.etree import ElementTree

import httpx
from dotenv import load_dotenv
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import or_
from sqlalchemy.orm import Session, selectinload

from app.config.database import get_db
from app.db.crud import get_or_create_country
from app.models.company import Company
from app.models.country import Country
from app.models.job import Job
from app.schemas.job import ExternalJob

load_dotenv()
EXTERNAL_SOURCE = os.getenv("EXTERNAL_API_URL")

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
        source=job_data.get("source", "internal"),
        company_id=company.id,
        country_id=country.id
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

def service_get_jobs(
    db: Session,
    title: Optional[str] = None,
    country: Optional[str] = None,
    salary_min: Optional[int] = None,
    salary_max: Optional[int] = None,
    source: Optional[str] = None,
    skills: Optional[List[str]] = None
):
    query = db.query(Job).options(
        selectinload(Job.company),
        selectinload(Job.country)
    )

    if title:
        query = query.filter(Job.description.ilike(f"%{title}%"))
    if country:
        query = query.join(Country).filter(Country.name.ilike(country))
    if salary_min:
        query = query.filter(Job.salary >= salary_min)
    if salary_max:
        query = query.filter(Job.salary <= salary_max)
    if source:
        query = query.filter(Job.source.ilike(f"%{source}%"))
    if skills:
        query = query.filter(Job.skills.contains(skills))
    return query.all()


# TODO: make url customizable to adapt to multiple external sources


async def fetch_external_jobs(params: dict):
    filtered_params = {k: v for k, v in params.items() if v is not None}
    print(filtered_params)
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                EXTERNAL_SOURCE,
                params=filtered_params,
                timeout=3.0
            )
            return response.json()
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        print("External API error: {}".format(e))
        raise HTTPException(status_code=500, detail="Error fetching external jobs.")


def parse_skills(xml_str: str) -> list:
    if not xml_str:
        return []
    try:
        root = ElementTree.fromstringlist(xml_str)
        return [skill.text for skill in root.findall('skill')]
    except ElementTree.ParseError:
        return []

from sqlalchemy.orm import Session
from app.schemas.country import Country as CountrySchema

def normalize_external_jobs(external_datas: dict, db: Session) -> List[ExternalJob]:
    jobs = []
    for country_name, job_list in external_datas.items():
        country = get_or_create_country(db, country_name=country_name)
        country_data = CountrySchema.from_orm(country)
        for job_array in job_list:
            if len(job_array) < 3:
                continue
            job = ExternalJob(
                title=job_array[0],
                salary=job_array[1],
                skills=parse_skills(job_array[2]),
                source="external",
                country=country_data
            )
            jobs.append(job)
    return jobs

def merge_jobs(internal_jobs: list, external_jobs: list) -> list:
    seen = set()
    combined_jobs = []

    for job in internal_jobs:
        key = f"{job.title} - {job.company} - {job.salary} - {job.source}"
        if key not in seen:
            seen.add(key)
            combined_jobs.append(job)

    for job in external_jobs:
        key = f"{job.title} - {job.salary} - {job.source}"
        if key not in seen:
            seen.add(key)
            combined_jobs.append(job)
    return combined_jobs