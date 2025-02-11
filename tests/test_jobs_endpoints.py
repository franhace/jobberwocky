from app.models.company import Company
from app.models.country import Country

def test_valid_id(client, db_session):
    job_data = {
        "title": "Test Job",
        "description": "This is a test job",
        "company": "Test Company",
        "country": "Test Country",
        "salary": 50000,
        "skills": ["Python", "FastAPI"]
    }
    create_response = client.post("/api/v1/jobs", json=job_data)

    print(create_response.status_code, create_response.json())

    assert create_response.status_code == 201

def test_invalid_salary(client):
    response = client.post("/api/v1/jobs", json={
        "title": "Invalid Job",
        "description": "Test invalid salary",
        "company": "Avature",
        "salary": -100,
        "country": "Argentina",
        "skills": ["Python"]
    })
    assert response.status_code == 422


def test_create_job(client, db_session):
    company = Company(name="Test Corp")
    country = Country(name="Test Country")
    db_session.add(company)
    db_session.add(country)
    db_session.commit()

    job_data = {
        "title": "Test Job",
        "description": "Test Description",
        "company": "Test Corp",
        "salary": 50000,
        "country": "Test Country",
        "skills": ["Python"]
    }
    response = client.post("/api/v1/jobs", json=job_data)

    assert response.status_code == 201, f"Expected 201, got {response.status_code}. Response: {response.json()}"
    assert response.json()["title"] == "Test Job"
    assert response.json()["company"]["name"] == "Test Corp"
    assert response.json()["country"]["name"] == "Test Country"
