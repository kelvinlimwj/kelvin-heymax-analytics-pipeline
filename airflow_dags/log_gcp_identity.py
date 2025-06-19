from airflow.operators.python import PythonOperator
from google.auth import default

def log_gcp_identity():
    credentials, _ = default()
    print("🧠 Running as:", credentials.service_account_email)

check_identity = PythonOperator(
    task_id='check_gcp_identity',
    python_callable=log_gcp_identity
)