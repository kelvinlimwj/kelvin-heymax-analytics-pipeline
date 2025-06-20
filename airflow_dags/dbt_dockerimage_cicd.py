import sys
import os

from scripts.trigger_cloud_build import trigger_cloud_build

from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime

default_args = {
    'owner': 'airflow',
    'retries': 1
}

with DAG(
    dag_id='dbt_dockerimage_CICD_pipeline',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval='0 0 * * *',
    catchup=False,
    tags=['docker', 'cloudbuild', 'dbt','image']
) as dag:


    dbt_dockerimage_cicd_build_trigger = PythonOperator(
        task_id='dbt_dockerimage_trigger',
        python_callable=trigger_cloud_build,
        op_kwargs={
            "project_id": "heymax-kelvin-analytics",
            "trigger_id": "85c9d9d7-032f-4b7b-8515-52a7d1c4efee",
            "branch_name": "main"
        }
    )

    dbt_dockerimage_cicd_build_trigger