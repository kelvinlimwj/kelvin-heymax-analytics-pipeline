# dbt

This folder contains:
- `heymax_dbt_data_tables`: Repo for dbt build tasks for both core tables (for downstream end users) and analytics tables (scheduled views and dashboarding in Looker). Transformation logic and data dictionaries for each table can be found inside subfolder `models\marts\core_tables` and `models\marts\analytics_tables`.

- `dbt_docker_repo\`: Repo for CI/CD pipelines (Cloud Build) to automate build, validation, and deployment of Docker images for running `dbt`.

- `dbt_cloud_functions\` : Scripts for Google Cloud Functions and their corresponding requirements

Click into each individual folder for in-depth documentation of the files in each folder.
