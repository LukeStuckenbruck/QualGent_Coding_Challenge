from fastapi import FastAPI, HTTPException
from job_server.models import JobPayload, JobStatus
from job_server.queue import enqueue_job, get_job_status, job_groups
from job_server.scheduler import start_scheduler

app = FastAPI()

@app.on_event("startup")
def on_startup():
    start_scheduler()

@app.post("/jobs", response_model=dict)
def submit_job(job: JobPayload):
    job_id = enqueue_job(job)
    return {"job_id": job_id}

@app.get("/jobs/{job_id}", response_model=JobStatus)
def job_status(job_id: str):
    status = get_job_status(job_id)
    if status.status == "not_found":
        raise HTTPException(status_code=404, detail="Job not found")
    return status

@app.get("/debug/groups")
def debug_groups():
    # Return a dict of group_key to list of job_ids
    return {
        str(group_key): [job_id for job_id, _ in jobs]
        for group_key, jobs in job_groups.items() if jobs
    } 