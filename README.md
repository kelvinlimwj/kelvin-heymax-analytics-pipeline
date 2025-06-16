# Kelvin HeyMax Analytics Pipeline Repository

This repository contains the configuration, orchestration, and transformation layers of a modern data pipeline deployed on Google Cloud Platform (GCP). The project is organized into the following directories:

## 📂 airflow_dags
Contains Apache Airflow DAGs used to orchestrate and schedule data pipeline tasks. These DAGs manage the flow of data from external sources into GCP services like Google Cloud Storage (GCS) and BigQuery.

Typical tasks include:
- API data ingestion
- Triggering Cloud Build jobs
- Executing dbt transformations
- Monitoring pipeline success/failure

## 📂 dbt
Includes the dbt (Data Build Tool) project responsible for transforming raw data in BigQuery into clean, structured models (e.g., dimensional models like `dim_users` and fact tables like `fct_events`).

This folder contains:
- `models/`: SQL models defining transformations
- `dbt_project.yml`: Configuration file for the dbt project
- `profiles.yml`: Connection profile to GCP BigQuery

## 📂 helm_config
Stores Helm charts and configuration values for deploying components (like Airflow) on a Kubernetes cluster, such as GKE (Google Kubernetes Engine).

This folder contains:
- `values.yaml`: Custom Helm values for Airflow or other services
- `pod_templates/`: Kubernetes pod templates for execution via KubernetesExecutor

### 🚀 What this project aims to do:
- Automate data ingestion from external API
- Leverage Kubernetes and Helm for cloud-native orchestration and deployment
- Build scalable and modular data pipelines using Airflow and dbt
- Create clean, trustworthy and usable datasets for downstream users to support analytics functions (Dashboarding in Looker) within HeyMax.

### 🛠 Requirements
- GCP project with BigQuery, Cloud Storage, Cloud Build, Cloud Functions enabled
- Kubernetes cluster (e.g., GKE)
- Helm repository installed on Google Cloud Server via Cloud Shell
- Airflow Deployment on Kubernetes Cluster

