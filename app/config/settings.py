from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PORT: int = 8000
    DB_URL: str = "sqlite:///./jobs.db"

    class Config:
        env_file = ".env"


settings = Settings()

# print(Settings().model_dump())