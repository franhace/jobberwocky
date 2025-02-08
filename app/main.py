from fastapi import FastAPI
from app.api.endpoints import jobs
from app.config.settings import settings
# TODO: add error handling

app = FastAPI(title="JobberWocky API", version="1.0.0")

app.include_router(jobs, prefix="/api/v1/jobs", tags=["jobs"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app= "app.main:app",
                host= "0.0.0.0",
                port= settings.PORT,
                reload= True)