import os
import uuid
from google.cloud import bigquery, storage

def load_latest_file_to_bq(project_id, dataset_id, table_id, bucket_name, gcs_folder):
    bq_client = bigquery.Client()
    storage_client = storage.Client()

    prefix = gcs_folder.strip("/") + "/"

    blobs = list(storage_client.list_blobs(bucket_name, prefix=prefix))

    supported_blobs = [b for b in blobs if b.name.endswith(".csv") or b.name.endswith(".json")]

    if not supported_blobs:
        print(f"No CSV or JSON files found in gs://{bucket_name}/{prefix}")
        return

    latest_blob = sorted(supported_blobs, key=lambda b: b.updated or b.time_created, reverse=True)[0]
    file_name = latest_blob.name
    uri = f"gs://{bucket_name}/{file_name}"
    print(f"Latest file found: {file_name}")

    if file_name.endswith(".csv"):
        job_config = bigquery.LoadJobConfig(
            autodetect=True,
            skip_leading_rows=1,
            source_format=bigquery.SourceFormat.CSV,
            write_disposition="WRITE_TRUNCATE"
        )
        print("Detected CSV file.")
    elif file_name.endswith(".json"):
        print("Detected JSON file.")

        raw_data = latest_blob.download_as_bytes()
        try:
            import json
            parsed = json.loads(raw_data)

            if isinstance(parsed, list):
                print("JSON is an array, converting to NDJSON...")
                import tempfile

                ndjson_str = '\n'.join([json.dumps(record) for record in parsed])

                temp_blob_name = f"{prefix}temp_ndjson_{uuid.uuid4().hex[:8]}.json"
                temp_blob = storage_client.bucket(bucket_name).blob(temp_blob_name)
                temp_blob.upload_from_string(ndjson_str, content_type="application/json")

                uri = f"gs://{bucket_name}/{temp_blob_name}" 

            else:
                print("JSON is already in NDJSON format.")

        except json.JSONDecodeError:
            print("Invalid JSON. Skipping file.")
            return

        job_config = bigquery.LoadJobConfig(
            autodetect=True,
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
            write_disposition="WRITE_TRUNCATE"
        )
        
    temp_table = f"{dataset_id}.temp_{uuid.uuid4().hex[:8]}"
    load_job = bq_client.load_table_from_uri(uri, f"{project_id}.{temp_table}", job_config=job_config)
    load_job.result()
    print(f"Loaded {uri} into {temp_table}")

    if 'temp_blob' in locals():
        temp_blob.delete()
        print(f"Deleted temporary NDJSON blob: {temp_blob_name}")

    try:
        temp_cols = [field.name for field in bq_client.get_table(f"{project_id}.{temp_table}").schema]
        target_cols = [field.name for field in bq_client.get_table(f"{project_id}.{dataset_id}.{table_id}").schema]

        common_cols = list(set(temp_cols) & set(target_cols))
        if not common_cols:
            print("No matching columns between temp and target table. Aborting merge.")
            return

        new_columns = list(set(temp_cols) - set(target_cols))
        if new_columns:
            print(f"New columns found in temp not present in target: {new_columns}. Aborting merge.")
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

        bq_client.query(merge_sql).result()
        print("Merge completed.")

    finally:
        bq_client.delete_table(f"{project_id}.{temp_table}", not_found_ok=True)
        print(f"Deleted temp table: {temp_table}")

