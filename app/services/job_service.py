jobs_db = []

def create_job(job_data: dict) -> dict:
    job = {"id:": len(jobs_db) + 1, **job_data}
    jobs_db.append(job)
    return job

def get_jobs() -> list:
    return jobs_db