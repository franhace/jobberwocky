import os
import sys

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

from app.models.base import Base
from app.models.company import Company
from app.models.country import Country
from app.models.job import Job

current_dir = os.path.dirname(os.path.abspath(__file__))
database_file_path = os.path.join(current_dir, 'jobs.db')
SQLALCHEMY_DATABASE_URL = f"sqlite:///{database_file_path}"

if not os.path.isfile(database_file_path):
    print(f"Database file does not exist at: {database_file_path}")
    sys.exit(1)


print("DB URL: {}".format(SQLALCHEMY_DATABASE_URL))

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
        return True
    except Exception as e:
        print(f"Error seeding data: {e}")
        return False
    finally:
        db.close()


if __name__ == "__main__":
    if seed_initial_data():
        sys.exit(0)
    else:
        sys.exit(1)