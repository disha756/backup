from celery_app import celery

@celery.task
def execute_workflow(workflow_id: int):
    print(f"Executing workflow with ID: {workflow_id}")