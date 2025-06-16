# HeyMax Analytics Pipelines & Data Tables Repository

This repository contains the configuration, orchestration, and transformation layers of a modern data pipeline deployed on Google Cloud Platform (GCP), from Airflow DAGs to dbt configurations, and Kubernetes cluster configuration. The project is organized into the following directories:

## 📂 airflow_dags
Contains Apache Airflow DAGs used to orchestrate and schedule data pipeline tasks. These DAGs manage the flow of data from external sources into GCP services like Google Cloud Storage (GCS) and BigQuery. 

Source tables used in our dbt runs can be found in the README.md of this folder.

Pipeline DAGs include:
- API data ingestion into GCS and automated uploads into BigQuery
- Kafka Streaming directly into BigQuery
- Triggering Cloud Build jobs
- Executing dbt transformations like dbt deps/test/run (configurations can be found in dbt folder)

## 📂 dbt
Includes anything that is related to dbt, mainly responsible for transforming raw data in BigQuery into clean, structured models (e.g., dimensional models like `dim_users` and fact tables like `fct_events`).

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

# 📊 Table Data Dictionaries Summary

## 🧑 `heymax-kelvin-analytics.heymax_analytics.dim_users` – User Dimension Table
> **Source Table:** `heymax-kelvin-analytics.heymax_analytics.event_stream_raw`

Contains metadata about each user in the system.

| **Column Name** | **Data Type** | **Description** |
|-----------------|---------------|------------------|
| `user_id`       | STRING        | Unique identifier for each user. Primary key of the table. |
| `country`       | STRING        | Country of the user, typically based on registration IP or profile information. |

---

## 🎯 `heymax-kelvin-analytics.heymax_analytics.fct_events` – Events Table
> **Source Table:** `heymax-kelvin-analytics.heymax_analytics.event_stream_raw`  

Captures user-generated events such as transactions and platform interactions.

| **Column Name**        | **Data Type** | **Description** |
|------------------------|---------------|------------------|
| `user_id`              | STRING        | Foreign key linking to `dim_users.user_id`. Identifies the user performing the event. |
| `utm_source`           | STRING        | UTM source from marketing attribution (e.g., "facebook", "google", "email"). |
| `transaction_category` | STRING        | Category of the transaction or event (e.g., "purchase", "redemption"). |
| `platform`             | STRING        | Platform on which the event occurred (e.g., "iOS", "Android", "Web"). |
| `event_type`           | STRING        | Type of event (e.g., "signup", "purchase", "login"). |
| `event_time`           | TIMESTAMP     | Timestamp indicating when the event occurred. |
| `miles_amount`         | FLOAT         | Amount of miles (or reward points) earned or spent during the event. |
