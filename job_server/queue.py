import uuid
from .models import JobPayload, JobStatus
from typing import Dict, List, Tuple, Optional

# Grouped job queue: (app_version_id, target) -> list of (job_id, JobPayload)
job_groups: Dict[Tuple[str, str], List[Tuple[str, JobPayload]]] = {}
jobs_status: Dict[str, JobStatus] = {}

def enqueue_job(job: JobPayload) -> str:
    job_id = str(uuid.uuid4())
    group_key = (job.app_version_id, job.target)
    if group_key not in job_groups:
        job_groups[group_key] = []
    job_groups[group_key].append((job_id, job))
    jobs_status[job_id] = JobStatus(job_id=job_id, status="queued")
    return job_id

def get_job_status(job_id: str) -> JobStatus:
    return jobs_status.get(job_id, JobStatus(job_id=job_id, status="not_found", message="Job not found"))

def get_next_group() -> Optional[Tuple[Tuple[str, str], List[Tuple[str, JobPayload]]]]:
    """Return the next group (app_version_id, target) and its jobs, or None if empty."""
    for group_key, jobs in job_groups.items():
        if jobs:
            return group_key, jobs
    return None

def remove_group(group_key: Tuple[str, str]):
    if group_key in job_groups:
        del job_groups[group_key] 