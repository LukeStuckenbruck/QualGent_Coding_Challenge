#!/usr/bin/env python3
"""
Test script for job grouping functionality
"""
import requests
import time
import json
import subprocess
import threading
from typing import Dict, List

# Configuration
SERVER_URL = "http://localhost:8000"
TEST_FILES = [
    "tests/onboarding.spec.js",
    "tests/onboarding.spec.js",  # Same test, different job
    "tests/onboarding.spec.js"   # Same test, different job
]

def start_server():
    """Start the job server in a separate thread"""
    def run_server():
        subprocess.run([
            "python", "-c", 
            "import uvicorn; uvicorn.run('job_server.main:app', host='0.0.0.0', port=8000, reload=False)"
        ], capture_output=True)
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(3)  # Wait for server to start
    return server_thread

def wait_for_server():
    """Wait for server to be ready"""
    max_attempts = 30
    for i in range(max_attempts):
        try:
            response = requests.get(f"{SERVER_URL}/debug/groups")
            if response.status_code == 200:
                print("✅ Server is ready")
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
        print(f"Waiting for server... ({i+1}/{max_attempts})")
    return False

def submit_job(org_id: str, app_version_id: str, test_path: str, target: str, priority: int = 1) -> str:
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

def get_job_status(job_id: str) -> Dict:
    """Get job status"""
    response = requests.get(f"{SERVER_URL}/jobs/{job_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return {"status": "error", "message": f"HTTP {response.status_code}"}

def get_groups() -> Dict:
    """Get current job groups"""
    response = requests.get(f"{SERVER_URL}/debug/groups")
    if response.status_code == 200:
        return response.json()
    else:
        return {}

def test_job_grouping():
    """Test the job grouping functionality"""
    print("🚀 Starting job grouping test...")
    
    # Start server
    print("📡 Starting job server...")
    server_thread = start_server()
    
    if not wait_for_server():
        print("❌ Server failed to start")
        return False
    
    # Test 1: Submit jobs with same app_version_id and target (should group together)
    print("\n📋 Test 1: Jobs with same app_version_id and target")
    job_ids_group1 = []
    
    # Submit 3 jobs with same grouping criteria
    for i in range(3):
        job_id = submit_job(
            org_id="test_org",
            app_version_id="app_v1",
            test_path=TEST_FILES[0],
            target="emulator",
            priority=1
        )
        if job_id:
            job_ids_group1.append(job_id)
    
    time.sleep(2)  # Wait for jobs to be processed
    
    # Check groups
    groups = get_groups()
    print(f"📊 Current groups: {json.dumps(groups, indent=2)}")
    
    # Test 2: Submit jobs with different app_version_id (should create separate group)
    print("\n📋 Test 2: Jobs with different app_version_id")
    job_ids_group2 = []
    
    for i in range(2):
        job_id = submit_job(
            org_id="test_org",
            app_version_id="app_v2",  # Different app version
            test_path=TEST_FILES[0],
            target="emulator",
            priority=1
        )
        if job_id:
            job_ids_group2.append(job_id)
    
    time.sleep(2)
    
    # Check groups again
    groups = get_groups()
    print(f"📊 Groups after adding different app_version_id: {json.dumps(groups, indent=2)}")
    
    # Test 3: Submit jobs with different target (should create separate group)
    print("\n📋 Test 3: Jobs with different target")
    job_ids_group3 = []
    
    for i in range(2):
        job_id = submit_job(
            org_id="test_org",
            app_version_id="app_v1",  # Same as group 1
            test_path=TEST_FILES[0],
            target="browserstack",  # Different target
            priority=1
        )
        if job_id:
            job_ids_group3.append(job_id)
    
    time.sleep(2)
    
    # Final groups check
    groups = get_groups()
    print(f"📊 Final groups: {json.dumps(groups, indent=2)}")
    
    # Test 4: Monitor job execution
    print("\n📋 Test 4: Monitoring job execution")
    all_job_ids = job_ids_group1 + job_ids_group2 + job_ids_group3
    
    max_wait_time = 60  # 60 seconds max
    start_time = time.time()
    
    while time.time() - start_time < max_wait_time:
        completed_jobs = 0
        running_jobs = 0
        queued_jobs = 0
        
        for job_id in all_job_ids:
            status = get_job_status(job_id)
            if status["status"] == "completed":
                completed_jobs += 1
            elif status["status"] == "running":
                running_jobs += 1
            elif status["status"] == "queued":
                queued_jobs += 1
        
        print(f"📈 Status: {completed_jobs} completed, {running_jobs} running, {queued_jobs} queued")
        
        if completed_jobs == len(all_job_ids):
            print("✅ All jobs completed!")
            break
        
        time.sleep(5)
    
    # Final status check
    print("\n📋 Final job statuses:")
    for job_id in all_job_ids:
        status = get_job_status(job_id)
        print(f"  Job {job_id}: {status['status']}")
        if status.get('message'):
            print(f"    Message: {status['message']}")
    
    return True

def main():
    """Main test function"""
    try:
        success = test_job_grouping()
        if success:
            print("\n🎉 Job grouping test completed successfully!")
        else:
            print("\n❌ Job grouping test failed!")
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 