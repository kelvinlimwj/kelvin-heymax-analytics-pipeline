# HeyMax Analytics Pipeline Repository

This repository contains the configuration, orchestration, and transformation layers of a modern data pipeline deployed on Google Cloud Platform (GCP), from Airflow DAGs to dbt configurations, and Kubernetes cluster configuration. The project is organized into the following directories:

## 📂 airflow_dags
Contains Apache Airflow DAGs used to orchestrate and schedule data pipeline tasks. These DAGs manage the flow of data from external sources into GCP services like Google Cloud Storage (GCS) and BigQuery.

Pipeline DAGs include:
- API data ingestion into GCS and automated uploads into BigQuery
- Kafka Streaming directly into BigQuery
- Triggering Cloud Build jobs
- Executing dbt transformations like dbt deps/test/run (configurations can be found in dbt folder)

## 📂 dbt
Includes anything that is related to dbt, mainly responsible for transforming raw data in BigQuery into clean, structured models (e.g., dimensional models like `dim_users` and fact tables like `fct_events`).

This folder contains:
- Sub folders for each individual dbt project, transformation logic can be found inside each subfolder's README.
- `dbt_docker_repo/`: Repo consisting of dbt docker image generation configurations into Artifact Registry
- `dbt_cloud_functions/` : Scripts for Google Cloud Functions and their corresponding requirements

## 📂 helm_config
Stores Helm charts and configuration values for deploying components (like Airflow) on a Kubernetes cluster, such as GKE (Google Kubernetes Engine).

This folder contains:
- `values.yaml`: Custom Helm values for intializing Airflow onto Kubernetes Cluster
- `pod_templates/`: Kubernetes pod templates for execution via KubernetesExecutor

### 🚀 What this project aims to do:
- Automate data ingestion from external API
- Leverage Kubernetes and Helm for cloud-native orchestration and deployment
- Build scalable and modular data pipelines using Airflow and dbt
- Create clean, trustworthy and usable datasets for downstream users to support analytics functions (e.g. Dashboarding in Looker) within HeyMax.

### 🛠 Requirements
- GCP project with BigQuery, Cloud Storage, Cloud Build, Cloud Functions enabled
- Kubernetes cluster (e.g., GKE)
- Helm repository installed on Google Cloud Server via Cloud Shell
- Airflow Instance on Kubernetes Cluster

