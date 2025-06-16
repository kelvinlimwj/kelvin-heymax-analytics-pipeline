# HeyMax Analytics Pipelines & Data Tables Repository

This repository contains the configuration, orchestration, and transformation layers of a modern data pipeline deployed on Google Cloud Platform (GCP), from Airflow DAGs to dbt configurations, and Kubernetes cluster configuration. The project is organized into the following directories:

## 📂 airflow_dags
Contains Apache Airflow DAGs and their respective <b>source tables</b>. These DAGs manage the flow of data from external sources into GCP services like Google Cloud Storage (GCS) and BigQuery via REST APIs or Kafka Streaming.

DAG tasks include:
- API data ingestion into GCS
- Automated uploads into BigQuery
- Kafka Streaming directly into BigQuery
- Triggering Cloud Build jobs
- Executing dbt transformations like dbt deps/test/run (configurations can be found in dbt folder)

## 📂 dbt
Includes individual folders for each dbt project, and anything that is related to dbt (configurations, profiles, dbt docker image generation etc), mainly responsible for transforming raw data in BigQuery into clean, structured models (e.g., dimensional models like `dim_users` and fact tables like `fct_events`).

## 📂 helm_config
Stores Helm charts and configuration values for deploying Airflow on a Kubernetes cluster via GKE (Google Kubernetes Engine).

# 📊 Table Data Dictionaries Summary

Data Dictionaries can be found in the individual project folders.

## `heymax-kelvin-analytics.heymax_analytics.dim_users` – User Dimension Table

> **Project:** `dbt\heymax_eventstream_data\`
> 
> **Source Table:** `heymax-kelvin-analytics.heymax_analytics.event_stream_raw`
>
> Description: Contains metadata about each user in the system.

---

## `heymax-kelvin-analytics.heymax_analytics.fct_events` – Events Table

> **Project:** `dbt\heymax_eventstream_data\`
> 
> **Source Table:** `heymax-kelvin-analytics.heymax_analytics.event_stream_raw`
>
> Description: Captures user-generated events, platform interactions and event miles accumulation.

# Additional Information: 

### What this project aims to do:
- Automate data ingestion from external API
- Leverage Kubernetes and Helm for cloud-native orchestration and deployment
- Build scalable and modular data pipelines using Airflow and dbt
- Create clean, trustworthy and usable datasets for downstream users to support analytics functions (e.g. Dashboarding in Looker) within HeyMax.

### Requirements
- GCP project with BigQuery, Cloud Storage, Cloud Build, Cloud Functions enabled
- Kubernetes cluster (e.g., GKE)
- Helm repository installed on Google Cloud Server via Cloud Shell
- Airflow Instance on Kubernetes Cluster
