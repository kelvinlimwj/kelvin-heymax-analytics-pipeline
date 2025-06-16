from google.auth import default
from google.auth import impersonated_credentials
from google.cloud.devtools import cloudbuild_v1
from google.cloud.devtools.cloudbuild_v1.types import Build, Source, RepoSource
from airflow.exceptions import AirflowException

def trigger_dbt_cloud_build(
    project_id: str,
    repo_name: str,
    branch: str,
    cloudbuild_dir: str,
    impersonate_service_account: str = "848785884148-compute@developer.gserviceaccount.com"
) -> None:
    """
    Trigger a Cloud Build job from a repo using impersonated credentials.

    Args:
        project_id (str): GCP project ID.
        repo_name (str): Name of the connected Cloud Source Repository.
        branch (str): Branch name (default is "main").
        cloudbuild_dir (str): Directory containing cloudbuild.yaml.
        impersonate_service_account (str): GSA to impersonate for triggering the build.
    """
    try:
        # Step 1: Get default credentials via Workload Identity
        source_credentials, _ = default()

        # Step 2: Impersonate the GSA with Cloud Build permissions
        target_credentials = impersonated_credentials.Credentials(
            source_credentials=source_credentials,
            target_principal=impersonate_service_account,
            target_scopes=["https://www.googleapis.com/auth/cloud-platform"],
            lifetime=3600,
        )

        # Step 3: Initialize Cloud Build client with impersonated credentials
        client = cloudbuild_v1.CloudBuildClient(credentials=target_credentials)

        # Step 4: Define build from source repo (triggerless build)
        build = Build(
            source=Source(
                repo_source=RepoSource(
                    project_id=project_id,
                    repo_name=repo_name,
                    branch_name=branch,
                    dir=cloudbuild_dir  # 👈 cloudbuild.yaml is inside this folder
                )
            ),
            timeout={"seconds": 1200}
        )

        print("[Cloud Build] Triggering manual build...")
        operation = client.create_build(project_id=project_id, build=build)
        result = operation.result()

        status = result.status.name
        build_id = result.id
        print(f"[Cloud Build] Build finished. ID: {build_id}, Status: {status}")

        if status != "SUCCESS":
            raise AirflowException(f"Build failed with status: {status}")

    except Exception as e:
        raise AirflowException(f"Failed to trigger Cloud Build: {e}")
