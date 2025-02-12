import pytest

from app.models.job import Job
from app.services.job_service import service_get_job_by_id, service_create_job


def test_get_job_by_id(db_session, setup_company_and_country):
    company, country = setup_company_and_country
    job = Job(title="Test Job", description="Test Description", salary=50000, company_id=company.id, country_id=country.id, source="internal")
    db_session.add(job)
    db_session.commit()
    fetched_job = service_get_job_by_id(db_session, job.id)

    assert fetched_job.id == job.id
    assert fetched_job.title == "Test Job"
    assert fetched_job.source == "internal"

def test_create_job(db_session, setup_company_and_country, job_data):
    company, country = setup_company_and_country
    job_data["company"] = company.name
    job_data["country"] = country.name
    job = service_create_job(db_session, job_data)

    assert job.id is not None
    assert job.title == "Backend Engineer"
    assert job.company.name == "Avature"

def test_duplicate_job(db_session, setup_company_and_country, job_data):
    company, country = setup_company_and_country
    job_data["company"] = company.name
    job_data["country"] = country.name
    job_data["source"] = "internal"
    service_create_job(db_session, job_data)

    with pytest.raises(ValueError, match="Job already exists."):
        service_create_job(db_session, job_data)