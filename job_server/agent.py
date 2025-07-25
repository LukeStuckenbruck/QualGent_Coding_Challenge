import time
import subprocess
from job_server.models import JobStatus, JobPayload
from job_server.queue import jobs_status
from typing import List, Tuple

NPX_PATH = r"C:\Program Files\nodejs\npx.cmd"

def run_group(group_key, jobs: List[Tuple[str, JobPayload]]):
    # Run all jobs in a group using Playwright
    for job_id, job in jobs:
        jobs_status[job_id].status = "running"
        test_path = job.test_path
        command = [
            NPX_PATH, "playwright", "test", test_path, "--headed"
        ]
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=600  # 10 minutes max per job
            )
            jobs_status[job_id].status = "completed" if result.returncode == 0 else "failed"
            jobs_status[job_id].message = f"Job {job_id} finished with exit code {result.returncode}."
            jobs_status[job_id].result = {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode
            }
        except Exception as e:
            jobs_status[job_id].status = "failed"
            jobs_status[job_id].message = f"Job {job_id} failed to run: {str(e)}"
            jobs_status[job_id].result = {
                "stdout": "",
                "stderr": str(e),
                "exit_code": -1
            } 