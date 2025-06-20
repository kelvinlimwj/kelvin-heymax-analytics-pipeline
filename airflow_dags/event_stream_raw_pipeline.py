import sys
import os

from scripts.api_to_gcs import fetch_api_and_upload_to_gcs
from scripts.gcs_to_bq_utils import load_latest_file_to_bq
from scripts.trigger_cloud_build import trigger_cloud_build

from airflow import DAG
from airflow.operators.python import PythonOperator
from google.cloud.devtools import cloudbuild_v1

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
    dag_id='dbt_tables_refresh',
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
            "dataset_id": "heymax_source",
            "table_id": "event_stream_raw",
            "bucket_name": "heymax_kelvin_raw_data_sg",
            "gcs_folder": "event_stream_data"
        }
    )

    dbt_tables_build_trigger = PythonOperator(
        task_id='dbt_run_trigger',
        python_callable=trigger_cloud_build,
        op_kwargs={
            "project_id": "heymax-kelvin-analytics",
            "trigger_id": "27913271-5713-4023-a2dc-64ea260788c9",
            "branch_name": "main"
        }
    )

    upload_to_gcs >> load_to_bq >> dbt_tables_build_trigger
