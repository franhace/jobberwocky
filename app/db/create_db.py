import os
import sys
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
    return True

if __name__ == "__main__":
    if create_tables():
        sys.exit(0)
    else:
        sys.exit(1)