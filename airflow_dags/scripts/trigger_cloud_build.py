from airflow.operators.python import PythonOperator
from google.cloud.devtools import cloudbuild_v1

def trigger_cloud_build(project_id: str, trigger_id: str, branch_name: str = "main"):
    client = cloudbuild_v1.CloudBuildClient()

    # Construct request
    parent = f"projects/{project_id}/locations/global"
    request = cloudbuild_v1.RunBuildTriggerRequest(
        project_id=project_id,
        trigger_id=trigger_id,
        source=cloudbuild_v1.RepoSource(branch_name=branch_name)
    )

    operation = client.run_build_trigger(request=request, parent=parent)
    result = operation.result(timeout=600)
    print("Build triggered. Status:", result.status)