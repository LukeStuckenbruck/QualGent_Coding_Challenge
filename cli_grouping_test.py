#!/usr/bin/env python3
"""
CLI-based test script for job grouping functionality
Uses the existing qgjob CLI tool
"""
import subprocess
import time
import json
import requests

SERVER_URL = "http://localhost:8000"

def run_cli_command(cmd):
    """Run a qgjob CLI command and return the output"""
    try:
        result = subprocess.run(
            cmd.split(),
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ CLI command failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

def submit_job_via_cli(org_id, app_version_id, test_path, target, priority=1):
    """Submit a job using the qgjob CLI"""
    cmd = f"python -m qgjob.cli submit --org-id={org_id} --app-version-id={app_version_id} --test={test_path} --target={target} --priority={priority}"
    
    output = run_cli_command(cmd)
    if output:
        # Extract job ID from output
        if "Job ID:" in output:
            job_id = output.split("Job ID:")[1].strip()
            print(f"✅ Submitted job {job_id} for {app_version_id}/{target}")
            return job_id
        else:
            print(f"❌ Could not extract job ID from: {output}")
            return None
    return None

def get_groups():
    """Get current job groups via API"""
    response = requests.get(f"{SERVER_URL}/debug/groups")
    if response.status_code == 200:
        return response.json()
    else:
        return {}

def get_job_status(job_id):
    """Get job status via API"""
    response = requests.get(f"{SERVER_URL}/jobs/{job_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return {"status": "error", "message": f"HTTP {response.status_code}"}

def main():
    print("🧪 CLI-based Job Grouping Test")
    print("=" * 40)
    print("Make sure the job server is running at http://localhost:8000")
    print("Start it with: python -c \"import uvicorn; uvicorn.run('job_server.main:app', host='0.0.0.0', port=8000, reload=True)\"")
    print()
    
    # Test 1: Submit jobs with same grouping criteria using CLI
    print("📋 Test 1: Submit 3 jobs with same app_version_id and target using CLI")
    print("These should be grouped together.")
    
    job_ids_group1 = []
    for i in range(3):
        job_id = submit_job_via_cli(
            org_id="test_org",
            app_version_id="app_v1",
            test_path="tests/onboarding.spec.js",
            target="emulator"
        )
        if job_id:
            job_ids_group1.append(job_id)
    
    time.sleep(2)
    
    print("\n📊 Current groups:")
    groups = get_groups()
    print(json.dumps(groups, indent=2))
    
    input("\nPress Enter to continue to Test 2...")
    
    # Test 2: Submit jobs with different app_version_id using CLI
    print("\n📋 Test 2: Submit 2 jobs with different app_version_id using CLI")
    print("These should create a separate group.")
    
    job_ids_group2 = []
    for i in range(2):
        job_id = submit_job_via_cli(
            org_id="test_org",
            app_version_id="app_v2",  # Different app version
            test_path="tests/onboarding.spec.js",
            target="emulator"
        )
        if job_id:
            job_ids_group2.append(job_id)
    
    time.sleep(2)
    
    print("\n📊 Groups after adding different app_version_id:")
    groups = get_groups()
    print(json.dumps(groups, indent=2))
    
    input("\nPress Enter to continue to Test 3...")
    
    # Test 3: Submit jobs with different target using CLI
    print("\n📋 Test 3: Submit 2 jobs with different target using CLI")
    print("These should create another separate group.")
    
    job_ids_group3 = []
    for i in range(2):
        job_id = submit_job_via_cli(
            org_id="test_org",
            app_version_id="app_v1",  # Same as group 1
            test_path="tests/onboarding.spec.js",
            target="browserstack"  # Different target
        )
        if job_id:
            job_ids_group3.append(job_id)
    
    time.sleep(2)
    
    print("\n📊 Final groups:")
    groups = get_groups()
    print(json.dumps(groups, indent=2))
    
    # Test 4: Check job statuses using CLI
    print("\n📋 Test 4: Check job statuses using CLI")
    all_job_ids = job_ids_group1 + job_ids_group2 + job_ids_group3
    
    for job_id in all_job_ids:
        cmd = f"python -m qgjob.cli status --job-id={job_id}"
        output = run_cli_command(cmd)
        if output:
            print(f"Job {job_id}: {output}")
    
    print("\n🎉 CLI test completed!")

if __name__ == "__main__":
    main() 