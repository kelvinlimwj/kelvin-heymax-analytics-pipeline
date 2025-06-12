from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="test_gcs_bash_log",
    start_date=datetime(2025, 6, 11),
    schedule_interval=None,
    catchup=False,
    tags=["debug"],
) as dag:

    test_task = BashOperator(
        task_id="echo_hello",
        bash_command="echo 'This is a test GCS log upload.'"
    )