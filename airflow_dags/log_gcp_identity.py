from airflow.operators.python import PythonOperator
from google.auth.transport.requests import Request
from google.auth.compute_engine.credentials import Credentials

def log_gcp_identity():
    credentials = Credentials()
    credentials.refresh(Request())
    print("🧠 Running as:", credentials.service_account_email)

with DAG(
    dag_id='test_gcp_identity_force_metadata',
    default_args={'owner': 'airflow'},
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:
    
    check_identity = PythonOperator(
        task_id='check_gcp_identity',
        python_callable=log_gcp_identity
    )
