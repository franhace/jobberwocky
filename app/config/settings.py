import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

class Settings(BaseSettings):
    PORT: int = 8000
    DB_URL: str = SQLALCHEMY_DATABASE_URL


settings = Settings()

# print(Settings().model_dump())