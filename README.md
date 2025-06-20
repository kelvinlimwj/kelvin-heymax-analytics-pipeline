# HeyMax Analytics Pipelines & Data Tables Repository

This repository contains the configuration, orchestration, and transformation layers of a modern data pipeline deployed on Google Cloud Platform (GCP), from Airflow DAGs to dbt configurations, and Kubernetes cluster configuration. This repo is organized into the following directories:

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
Includes individual folders for each dbt project, and anything that is related to dbt (configurations, profiles, dbt docker image generation etc), mainly responsible for transforming raw data in BigQuery into clean, structured models (e.g., dimensional models like `dim_users` and fact tables like `fct_events`).

## 📂 helm_config
Stores Helm charts and configuration values for deployed Airflow instance on Kubernetes cluster via GKE (Google Kubernetes Engine).

# Additional Information: 

### Analytics Dashboards:

HeyMax User Activity and User Attrition Dashboard : https://lookerstudio.google.com/reporting/819c1ac8-762e-4fb9-ac34-94d2ef2c20ba/page/p_sx1q7zgjtd

### Future Scalability:

- Usage of KubernetesExecutor (Already in use) over LocalExecutor for Kubernetes Cluster
- Use incremental build for dbt instead of building entire table
- CI/CD pipelines for DAGs (Using Github Actions and Cloud Build Triggers)
- Monitor Airflow instance health with Prometheus or Grafana
- Apache Kafka (if required) instead of Airflow (Self-hosted) for real-time data streaming and analytics.