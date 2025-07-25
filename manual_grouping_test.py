#!/usr/bin/env python3
"""
Manual test script for job grouping functionality
Run this after starting the job server manually
"""
import requests
import time
import json

SERVER_URL = "http://localhost:8000"

def submit_job(org_id, app_version_id, test_path, target, priority=1):
    """Submit a job and return the job ID"""
    payload = {
        "org_id": org_id,
        "app_version_id": app_version_id,
        "test_path": test_path,
        "priority": priority,
        "target": target
    }
    
    response = requests.post(f"{SERVER_URL}/jobs", json=payload)
    if response.status_code == 200:
        job_id = response.json()["job_id"]
        print(f"✅ Submitted job {job_id} for {app_version_id}/{target}")
        return job_id
    else:
        print(f"❌ Failed to submit job: {response.status_code}")
        return None

def get_groups():
    """Get current job groups"""
    response = requests.get(f"{SERVER_URL}/debug/groups")
    if response.status_code == 200:
        return response.json()
    else:
        return {}

def get_job_status(job_id):
    """Get job status"""
    response = requests.get(f"{SERVER_URL}/jobs/{job_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return {"status": "error", "message": f"HTTP {response.status_code}"}

def main():
    print("🧪 Manual Job Grouping Test")
    print("=" * 40)
    print("Make sure the job server is running at http://localhost:8000")
    print("Start it with: python -c \"import uvicorn; uvicorn.run('job_server.main:app', host='0.0.0.0', port=8000, reload=True)\"")
    print()
    
    # Test 1: Submit jobs with same grouping criteria
    print("📋 Test 1: Submit 3 jobs with same app_version_id and target")
    print("These should be grouped together.")
    
    job_ids_group1 = []
    for i in range(3):
        job_id = submit_job(
            org_id="test_org",
            app_version_id="app_v1",
            test_path="tests/onboarding.spec.js",
            target="emulator"
        )
        if job_id:
            job_ids_group1.append(job_id)
    
    print("\n📊 Current groups:")
    groups = get_groups()
    print(json.dumps(groups, indent=2))
    
    input("\nPress Enter to continue to Test 2...")
    
    # Test 2: Submit jobs with different app_version_id
    print("\n📋 Test 2: Submit 2 jobs with different app_version_id")
    print("These should create a separate group.")
    
    job_ids_group2 = []
    for i in range(2):
        job_id = submit_job(
            org_id="test_org",
            app_version_id="app_v2",  # Different app version
            test_path="tests/onboarding.spec.js",
            target="emulator"
        )
        if job_id:
            job_ids_group2.append(job_id)
    
    print("\n📊 Groups after adding different app_version_id:")
    groups = get_groups()
    print(json.dumps(groups, indent=2))
    
    input("\nPress Enter to continue to Test 3...")
    
    # Test 3: Submit jobs with different target
    print("\n📋 Test 3: Submit 2 jobs with different target")
    print("These should create another separate group.")
    
    job_ids_group3 = []
    for i in range(2):
        job_id = submit_job(
            org_id="test_org",
            app_version_id="app_v1",  # Same as group 1
            test_path="tests/onboarding.spec.js",
            target="browserstack"  # Different target
        )
        if job_id:
            job_ids_group3.append(job_id)
    
    print("\n📊 Final groups:")
    groups = get_groups()
    print(json.dumps(groups, indent=2))
    
    # Monitor execution
    print("\n📋 Monitoring job execution...")
    all_job_ids = job_ids_group1 + job_ids_group2 + job_ids_group3
    
    for i in range(12):  # Monitor for 60 seconds
        print(f"\n--- Status check {i+1}/12 ---")
        for job_id in all_job_ids:
            status = get_job_status(job_id)
            print(f"Job {job_id}: {status['status']}")
        
        time.sleep(5)
    
    print("\n🎉 Test completed!")

if __name__ == "__main__":
    main() 