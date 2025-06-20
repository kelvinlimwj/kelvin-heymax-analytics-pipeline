## dbt_docker_repo

| **File Name**               | **Description** |
|----------------------------|-----------------|
| `Dockerfile`               | Docker image for running dbt, including dependencies and entrypoint setup. |
| `dockerimagecloudbuild.yaml` | CI/CD Cloud Build Pipeline for dbt Docker image generation to be pushed to Artifact Registry. |

---

### dockerimagecloudbuild.yaml Pipeline Configuration

| Step | Description |
|------|-------------|
| **Build Image** | Builds a fresh Docker image for `dbt` using the Dockerfile at `dbt/dbt_docker_repo/Dockerfile` (no cache). |
| **Push Staging Image** | Pushes the image to Artifact Registry under the `staging` tag. |
| **Run DBT Validation** | Creates a temporary `profiles.yml`, then runs `dbt debug` and `dbt parse` to validate the dbt project configuration. |
| **Promote to Prod** | If validation passes, retags the staging image as `prod`. |
| **Push Prod Image** | Pushes the production-ready image to Artifact Registry, latest prod image used in dbt runs. |