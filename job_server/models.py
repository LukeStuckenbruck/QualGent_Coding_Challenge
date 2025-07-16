from pydantic import BaseModel
from typing import Optional

class JobPayload(BaseModel):
    org_id: str
    app_version_id: str
    test_path: str
    priority: int = 1
    target: str

class JobStatus(BaseModel):
    job_id: str
    status: str
    message: Optional[str] = None
    result: Optional[dict] = None 