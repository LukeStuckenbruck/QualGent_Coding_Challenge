import requests

API_BASE_URL = "http://localhost:8000"  # Change as needed

def submit_job(payload):
    # Stub: Replace with actual POST request
    response = requests.post(f"{API_BASE_URL}/jobs", json=payload)
    return response.json()

def get_job_status(job_id):
    # Stub: Replace with actual GET request
    response = requests.get(f"{API_BASE_URL}/jobs/{job_id}")
    return response.json() 