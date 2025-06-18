# dbt

This folder contains:
- `heymax_dbt_data_tables`: Repo for dbt build tasks for both core tables (for downstream end users) and analytics tables (scheduled views and dashboarding in Looker). Transformation logic and data dictionaries for each table can be found inside subfolder `models\core` and `models\analytics`.

- `dbt_docker_repo\`: Repo consisting of dbt docker image generation configurations into Artifact Registry

- `dbt_cloud_functions\` : Scripts for Google Cloud Functions and their corresponding requirements

Click into each individual folder for in-depth documentation of the files in each folder.
