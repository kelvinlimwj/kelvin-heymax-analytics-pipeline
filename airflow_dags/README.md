# Airflow DAGs

This directory contains Apache Airflow DAGs for orchestrating data ingestion and processing pipelines on Google Cloud Platform.

## 📄 DAGs Overview

| File Name                | Description                                                                 |
|-------------------------|-----------------------------------------------------------------------------|
| `gcs_to_bq_dag.py`      | Ingests data from a Google Cloud Storage bucket and loads it into BigQuery. |
| `test_gcs_logging_dag.py` | Test DAG to validate logging and GCS event handling logic.               |

## 📁 Other Files and Folders

| Name             | Type        | Description                                                         |
|------------------|-------------|-----------------------------------------------------------------------------|
| `.airflowignore` | Config file | Config file to indicate to Airflow which files/folders to ignore when parsing DAGs.             |
| `scripts/`       | Folder      | Contains helper modules or utility functions used across DAGs.              |


## 🚀 How to use:

1. Drop DAGs into the root of `airflow_dags` directory (This is the directory!).
2. Drop DAG task scripts into `scripts/` folder.
3. Make sure DAG py script references the correct task scripts from the `scripts/` folder!
4. Test/Trigger/Monitor DAGs from the Airflow UI or CLI.



