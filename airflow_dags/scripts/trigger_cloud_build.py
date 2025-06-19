from google.cloud.devtools import cloudbuild_v1
from google.auth.transport.requests import Request
from google.auth.compute_engine.credentials import Credentials

def trigger_cloud_build(project_id: str, trigger_id: str, branch_name: str = "main"):
    credentials = Credentials()
    credentials.refresh(Request())
    print("🧠 Using identity:", credentials.service_account_email)

    client = cloudbuild_v1.CloudBuildClient(credentials=credentials)

    request = cloudbuild_v1.RunBuildTriggerRequest(
        project_id=project_id,
        trigger_id=trigger_id,
        source=cloudbuild_v1.RepoSource(branch_name=branch_name)
    )

    operation = client.run_build_trigger(request=request)
    result = operation.result(timeout=600)
    print("✅ Build triggered. Status:", result.status)
