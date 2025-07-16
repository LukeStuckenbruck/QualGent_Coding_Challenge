import threading
import time
from job_server.queue import get_next_group, remove_group
from job_server.agent import run_group

scheduler_running = False

def scheduler_loop():
    global scheduler_running
    scheduler_running = True
    while scheduler_running:
        group = get_next_group()
        if group:
            group_key, jobs = group
            run_group(group_key, jobs)
            remove_group(group_key)
        else:
            time.sleep(1)  # Wait before checking again

def start_scheduler():
    t = threading.Thread(target=scheduler_loop, daemon=True)
    t.start() 