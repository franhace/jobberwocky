from app import Base
from app.config.database import get_db
from app.models.company import Company
from app.models.country import Country

def clear_all_tables(db):
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())
        print(f"Clearing table {table}")
    db.commit()

def get_or_create_country(db, country_name: str):
    country = db.query(Country).filter(Country.name == country_name).first()
    if not country:
        country = Country(name=country_name)
        db.add(country)
        db.commit()
        db.refresh(country)
    return country

def get_or_create_company(db, company_name):
    company = db.query(Company).filter(Company.name == company_name).first()
    if not company:
        company = Company(name=company_name)
        db.add(company)
        db.commit()
        db.refresh(company)
    return company
