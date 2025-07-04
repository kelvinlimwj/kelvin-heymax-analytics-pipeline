# HeyMax Datasets and Data Tables Repository and Analytics Pipelines (Airflow)

Project: `heymax-kelvin-analytics`

Datasets:

1. `heymax_source` : Raw data ingested from external sources such as CSV uploads, APIs, or production databases. Layer contains the untransformed source-of-truth data.
2. `heymax_staging` : Initial transformation layer where raw data is cleaned, standardized, and prepared for modeling into core tables.. 
3. `heymax_core` : Core modeling layer that applies business logic to create reusable core tables such as dim_users and events_tables. 
4. `heymax_analytics` : Final layer of aggregated tables (Generated in views usually) optimized for dashboarding and business intelligence usage/analytics.

---

This repo is organized into the following directories:

## 📂 airflow_dags
Contains Apache Airflow DAGs and their respective <b>source tables</b>. These DAGs manage the flow of data from external sources into GCP services like Google Cloud Storage (GCS) and BigQuery via REST APIs or Kafka Streaming.

### Airflow Set Up:
- GCP project with BigQuery, Cloud Storage, Cloud Build, Cloud Functions enabled
- Kubernetes cluster (e.g., GKE)
- Helm repository installed on Google Cloud Server via Cloud Shell
- Airflow Instance on Kubernetes Cluster

### DAG tasks include:
- Daily Refresh of dbt Docker Image to latest updated version (Includes running dbt debug/test to ensure no version conflicts during dbt run)
- API data ingestion into GCS
- Automated uploads into BigQuery
- Kafka Streaming directly into BigQuery
- Triggering Cloud Build jobs
- Executing dbt transformations like dbt deps/test/run (configurations can be found in dbt folder)

## 📂 dbt
Includes individual folders for each dbt project, and anything that is related to dbt (configurations, profiles, dbt docker image generation etc, dbt tests(`schema.yml` files)), mainly responsible for transforming raw data in BigQuery into clean, structured models (e.g., dimensional models like `dim_users` and fact tables like `fct_events`).

## 📂 helm_config
Stores Helm charts and configuration values for deployed Airflow instance on Kubernetes cluster via GKE (Google Kubernetes Engine).

# Additional Information: 

### Analytics Dashboards:

HeyMax User Activity and User Attrition Dashboard : https://lookerstudio.google.com/reporting/819c1ac8-762e-4fb9-ac34-94d2ef2c20ba/page/p_sx1q7zgjtd

### Future Scalability:

- Create sandbox/staging environment off main branch (everything is done in main right now)
- Usage of KubernetesExecutor (Already in use) over LocalExecutor for Kubernetes Cluster
- Use incremental build for dbt instead of building entire table
- CI/CD pipelines for DAGs (Using Github Actions and Cloud Build Triggers)
- Monitor Airflow instance health with Prometheus or Grafana
- Explore usage of 3rd party tools such as Fivetran, Windsor.ai, Airbyte to manage data integration into BigQuery. (Current set up manages REST API calls and responses are placed into GCS buckets via steps in Airflow DAG)
- Apache Kafka (if required) instead of Airflow (Self-hosted) for real-time data streaming and analytics.
