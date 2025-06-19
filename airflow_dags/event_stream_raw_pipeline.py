import sys
import os

from scripts.api_to_gcs import fetch_api_and_upload_to_gcs
from scripts.gcs_to_bq_utils import load_latest_file_to_bq

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.cloud_build import CloudBuildTriggerJobRunOperator
from google.cloud.devtools.cloudbuild_v1.types import Build, Source, RepoSource

from datetime import datetime

# Update here for file name when API is called

today_str = datetime.now().strftime("%d%m%y")
dynamic_filename = f"event_data_{today_str}.json"
#dynamic_filename = f"event_data_{today_str}.csv"

default_args = {
    'owner': 'airflow',
    'retries': 1
}

with DAG(
    dag_id='api_to_gcs_then_bq',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    tags=['api', 'gcs', 'bigquery', 'cloudbuild', 'dbt']
) as dag:

    upload_to_gcs = PythonOperator(
        task_id='fetch_api_and_upload_to_gcs',
        python_callable=fetch_api_and_upload_to_gcs,
        op_kwargs={
            "api_url": "https://jsonplaceholder.typicode.com/posts", 
            "bucket_name": "heymax_kelvin_raw_data_sg",
            "gcs_folder": "event_stream_data", 
            "gcs_file_name": dynamic_filename 
        }
    )

    load_to_bq = PythonOperator(
        task_id='load_latest_to_bigquery',
        python_callable=load_latest_file_to_bq,
        op_kwargs={
            "project_id": "heymax-kelvin-analytics",
            "dataset_id": "heymax_analytics",
            "table_id": "event_stream_raw",
            "bucket_name": "heymax_kelvin_raw_data_sg",
            "gcs_folder": "event_stream_data"
        }
    )

    eventstream_build = CloudBuildCreateBuildOperator(
        task_id="eventstream_cloudbuild",
        project_id="heymax-kelvin-analytics",
        gcp_conn_id="google_cloud_default",
        build={
            "source": {
                "repo_source": {  
                    "project_id": "heymax-kelvin-analytics",
                    "repo_name": "kelvinlimwj-kelvin-heymax-analytics-pipeline",
                    "branch_name": "main",
                    "dir": "dbt/dbt_bigquery_analytics"
                }
            },
            "steps": [
                {
                    "name": "gcr.io/cloud-builders/gcloud",
                    "args": ["dbt", "run"]
                }
            ],
            "timeout": "1200s",
            "options": {
                "requested_verify_option": "NOT_VERIFIED" 
            }
        }
    )

    upload_to_gcs >> load_to_bq >> eventstream_build
