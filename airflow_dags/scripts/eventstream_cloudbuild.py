from google.cloud.devtools import cloudbuild_v1
from google.cloud.devtools.cloudbuild_v1.types import RepoSource
from airflow.exceptions import AirflowException

def trigger_dbt_cloud_build(project_id: str, trigger_id: str, branch: str = "main") -> None:
    """
    Triggers a Cloud Build trigger created in Google Cloud Console.

    :param project_id: Your GCP project ID
    :param trigger_id: The ID of the Cloud Build trigger
    :param branch: Git branch to build from (default: main)
    """
    client = cloudbuild_v1.CloudBuildClient()

    try:
        build_operation = client.run_build_trigger(
            project_id=project_id,
            trigger_id=trigger_id,
            source=RepoSource(branch_name=branch)
        )
        print(f"[Cloud Build] Trigger started. Waiting for build to complete...")

        build_result = build_operation.result()  # Blocks until build completes
        status = build_result.status.name
        build_id = build_result.id

        print(f"[Cloud Build] Build finished. ID: {build_id}, Status: {status}")

        if status != "SUCCESS":
            raise AirflowException(f"Build failed with status: {status}")

    except Exception as e:
        raise AirflowException(f"Failed to trigger Cloud Build: {e}")
