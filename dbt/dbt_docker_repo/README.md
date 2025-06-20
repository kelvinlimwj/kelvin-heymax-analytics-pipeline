## dbt_docker_repo

| **File Name**               | **Description** |
|----------------------------|-----------------|
| `Dockerfile`               | Docker image for running dbt, including dependencies and entrypoint setup. |
| `dockerimagecloudbuild.yaml` | CI/CD Cloud Build Pipeline for dbt Docker image generation to be pushed to Artifact Registry.<br><br> **Step Descriptions:** <br><br> 1. **Build Image**: Builds a fresh Docker image for `dbt` using the Dockerfile at `dbt/dbt_docker_repo/Dockerfile` (no cache). <br>  2. **Push Staging Image**: Pushes the image to Artifact Registry under the `staging` tag. <br> 3. **Run DBT Validation**: Creates a temporary `profiles.yml`, then runs `dbt debug` and `dbt parse` to validate the dbt project configuration. <br> 4. **Promote to Prod**: If validation passes, retags the staging image as `prod`. <br> 5. **Push Prod Image**: Pushes the production-ready image to Artifact Registry; the latest `prod` image is used in dbt runs. <br>|
