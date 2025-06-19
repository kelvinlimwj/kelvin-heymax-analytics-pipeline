from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from google.auth import default

def log_gcp_identity():
    credentials, _ = default()
    print("🧠 Running as:", credentials.service_account_email)

default_args = {
    'owner': 'airflow',
    'retries': 0,
}

with DAG(
    dag_id='test_gcp_identity',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=['test', 'gcp', 'identity'],
) as dag:

    check_identity = PythonOperator(
        task_id='check_gcp_identity',
        python_callable=log_gcp_identity
    )
