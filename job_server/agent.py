import time
from job_server.models import JobStatus, JobPayload
from job_server.queue import jobs_status
from typing import List, Tuple

def run_group(group_key, jobs: List[Tuple[str, JobPayload]]):
    # Simulate running all jobs in a group
    for job_id, job in jobs:
        jobs_status[job_id].status = "running"
        time.sleep(1)  # Simulate test execution
        jobs_status[job_id].status = "completed"
        jobs_status[job_id].message = f"Job {job_id} completed successfully." 