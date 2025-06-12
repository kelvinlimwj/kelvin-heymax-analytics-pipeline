import os
import uuid
from google.cloud import bigquery

def load_gcs_to_bq(project_id, dataset_id, table_id, bucket_name, file_name):
    client = bigquery.Client()

    if not (file_name.endswith('.csv') or file_name.endswith('.json')):
        print(f"Unsupported file type: {file_name}. Skipping.")
        return

    if not file_name.startswith('event_stream/'):
        print("File not in expected folder. Skipping.")
        return

    uri = f"gs://{bucket_name}/{file_name}"
    temp_table = f"{dataset_id}.temp_{uuid.uuid4().hex[:8]}"

    if file_name.endswith('.csv'):
        print("CSV file detected.")
        job_config = bigquery.LoadJobConfig(
            autodetect=True,
            skip_leading_rows=1,
            source_format=bigquery.SourceFormat.CSV,
            write_disposition="WRITE_TRUNCATE"
        )
    elif file_name.endswith('.json'):
        print("JSON file detected.")
        job_config = bigquery.LoadJobConfig(
            autodetect=True,
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
            write_disposition="WRITE_TRUNCATE"
        )

    load_job = client.load_table_from_uri(uri, f"{project_id}.{temp_table}", job_config=job_config)
    load_job.result()
    print(f"Loaded {uri} into temporary table {temp_table}")

    temp_cols = [field.name for field in client.get_table(f"{project_id}.{temp_table}").schema]
    target_cols = [field.name for field in client.get_table(f"{project_id}.{dataset_id}.{table_id}").schema]

    new_columns = list(set(temp_cols) - set(target_cols))
    if new_columns:
        print(f"New columns found in uploaded file (not in target table): {new_columns}")
    else:
        print("No new columns found in uploaded file.")

    common_cols = list(set(temp_cols) & set(target_cols))
    if not common_cols:
        print("No matching columns between staging and target table. Aborting merge.")
        return

    select_cols = ", ".join([f"`{col}`" for col in common_cols])
    merge_condition = " AND ".join([f"T.{col} = S.{col}" for col in common_cols])

    merge_sql = f"""
    MERGE `{project_id}.{dataset_id}.{table_id}` T
    USING (
      SELECT {select_cols}
      FROM `{project_id}.{temp_table}`
    ) S
    ON {merge_condition}
    WHEN NOT MATCHED THEN
      INSERT ({select_cols})
      VALUES ({select_cols})
    """

    client.query(merge_sql).result()
    print("Merge completed based on full-column match.")

    client.delete_table(f"{project_id}.{temp_table}")
    print(f"Temporary table {temp_table} deleted.")
