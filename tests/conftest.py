import os
import tempfile
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.config.database import get_db
from app.models.base import Base
from app.models.company import Company
from app.models.country import Country
from app.models.job import Job
from app.services.job_service import service_create_job, service_get_job_by_id

# Fixture for the temporary test database
@pytest.fixture(scope='session')
def test_db():
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(db_fd)

    engine = create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(bind=engine)
    yield engine

    os.remove(db_path)

# Fixture for database session
@pytest.fixture(scope='function')
def db_session(test_db):
    connection = test_db.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    app.dependency_overrides[get_db] = lambda: session

    yield session

    transaction.rollback()
    session.close()
    connection.close()
    del app.dependency_overrides[get_db]

# Fixture for the FastAPI test client
@pytest.fixture(scope='function')
def client(db_session):
    yield TestClient(app)

# Fixture for job data
@pytest.fixture(scope='function')
def job_data():
    return {
        "title": "Backend Engineer",
        "description": "Python expert needed right away",
        "company": "Avature",
        "salary": 80000,
        "country": "Argentina",
        "skills": ["AWS", "Docker"]
    }

# Fixture for seeding company and country
@pytest.fixture(scope='function')
def setup_company_and_country(db_session):
    company = Company(name="Avature")
    country = Country(name="Argentina")
    db_session.add(company)
    db_session.add(country)
    db_session.commit()
    return company, country

# Test for getting a job by ID