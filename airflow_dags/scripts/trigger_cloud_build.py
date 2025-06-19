from airflow.operators.python import PythonOperator
from google.cloud.devtools import cloudbuild_v1

def trigger_cloud_build(project_id: str, trigger_id: str, branch_name: str = "main"):
    client = cloudbuild_v1.CloudBuildClient()

    # Construct the source
    repo_source = cloudbuild_v1.RepoSource(branch_name=branch_name)

    # Correct usage — no `parent` argument
    request = cloudbuild_v1.RunBuildTriggerRequest(
        project_id=project_id,
        trigger_id=trigger_id,
        source=repo_source
    )

    # Submit the build trigger
    operation = client.run_build_trigger(request=request)
    result = operation.result(timeout=600)
    print("Build triggered. Status:", result.status)