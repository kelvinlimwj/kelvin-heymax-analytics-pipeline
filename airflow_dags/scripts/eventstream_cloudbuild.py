from google.auth import default
from google.auth import impersonated_credentials
from google.cloud.devtools import cloudbuild_v1
from google.cloud.devtools.cloudbuild_v1.types import RepoSource
from airflow.exceptions import AirflowException

def trigger_dbt_cloud_build(project_id: str, trigger_id: str, branch: str = "main") -> None:
    """
    Triggers a Cloud Build trigger using impersonated credentials.

    :param project_id: Your GCP project ID
    :param trigger_id: The ID of the Cloud Build trigger
    :param branch: Git branch to build from (default: main)
    """
    try:
        # 1. Get default credentials from environment (Workload Identity)
        source_credentials, _ = default()

        # 2. Impersonate the target service account
        target_credentials = impersonated_credentials.Credentials(
            source_credentials=source_credentials,
            target_principal="848785884148-compute@developer.gserviceaccount.com",
            target_scopes=["https://www.googleapis.com/auth/cloud-platform"],
            lifetime=3600,
        )

        # 3. Use impersonated credentials for Cloud Build client
        client = cloudbuild_v1.CloudBuildClient(credentials=target_credentials)

        # 4. Trigger the build
        build_operation = client.run_build_trigger(
            project_id=project_id,
            trigger_id=trigger_id,
            source=RepoSource(branch_name=branch)
        )

        print(f"[Cloud Build] Trigger started. Waiting for build to complete...")
        build_result = build_operation.result()  # Waits for build to finish

        status = build_result.status.name
        build_id = build_result.id
        print(f"[Cloud Build] Build finished. ID: {build_id}, Status: {status}")

        if status != "SUCCESS":
            raise AirflowException(f"Build failed with status: {status}")

    except Exception as e:
        raise AirflowException(f"Failed to trigger Cloud Build: {e}")
