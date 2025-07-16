import click
from . import rest_client

@click.group()
def cli():
    """qgjob: QualGent Job CLI"""
    pass

@cli.command()
@click.option('--org-id', required=True, help='Organization ID')
@click.option('--app-version-id', required=True, help='App version ID')
@click.option('--test', 'test_path', required=True, help='Path to test script')
@click.option('--priority', default=1, show_default=True, help='Job priority (higher = more urgent)')
@click.option('--target', type=click.Choice(['emulator', 'device', 'browserstack']), required=True, help='Target environment')
def submit(org_id, app_version_id, test_path, priority, target):
    """Submit a test job."""
    payload = {
        'org_id': org_id,
        'app_version_id': app_version_id,
        'test_path': test_path,
        'priority': priority,
        'target': target
    }
    click.echo(f"Submitting job: {payload}")
    result = rest_client.submit_job(payload)
    click.echo(f"Job submitted. Job ID: {result.get('job_id')}")

@cli.command()
@click.option('--job-id', required=True, help='Job ID to check status')
def status(job_id):
    """Check the status of a job."""
    result = rest_client.get_job_status(job_id)
    click.echo(f"Job Status: {result}")

if __name__ == "__main__":
    cli() 