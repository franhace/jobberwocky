from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_get_job_endpoint():
    response = client.get("/api/v1/jobs/1")
    assert response.status_code == 200


def test_search_jobs():
    response = client.get("/jobs/?description=Docker")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_invalid_salary():
    response = client.post("/jobs/", json={
        "title": "Invalid Job",
        "description": "Test invalid salary",
        "company": "Avature",
        "salary": -100,
        "country": "Argentina"
    })
    assert response.status_code == 422

