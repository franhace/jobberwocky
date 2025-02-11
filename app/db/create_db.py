import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from app.models.base import Base
# models get registered with the Base metadata
from app.models.job import Job
from app.models.company import Company
from app.models.country import Country

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

def create_tables():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

def seed_initial_data():
    from sqlalchemy.orm import sessionmaker

    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        countries = [
            Country(name="Argentina"),
            Country(name="USA"),
            Country(name="Spain")
        ]
        db.add_all(countries)
        db.commit()

        companies = [
            Company(name="Avature"),
            Company(name="Google"),
            Company(name="Meta")
        ]
        db.add_all(companies)
        db.commit()

        jobs = [
            Job(
                title="Backend Engineer",
                description="Python expert needed",
                salary=80000,
                skills=["Python", "FastApi", "Docker"],
                company_id=1,
                country_id=1
            ),
            Job(
                title="Cloud Architect",
                description="AWS experience required",
                salary=120000,
                skills=["AWS", "Terraform"],
                company_id=2,
                country_id=2
            )
        ]
        db.add_all(jobs)
        db.commit()

        print("Initial data seeded.")
    except Exception as e:
        print(f"Error seeding data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # pass
    create_tables()
    seed_initial_data()