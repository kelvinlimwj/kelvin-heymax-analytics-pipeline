import requests
import json
import tempfile
from google.cloud import storage

def fetch_api_and_upload_to_gcs(api_url, bucket_name, gcs_folder, gcs_file_name):

    print(">>> Task started — entering fetch logic")
    
    response = requests.get(api_url)
    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}")

    data = response.json()

    with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as temp_file:
        json.dump(data, temp_file, indent=2)
        temp_file_path = temp_file.name

    destination_blob = f"{gcs_folder}/{gcs_file_name}"
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob)
    blob.upload_from_filename(temp_file_path)

    print(f"Uploaded to gs://{bucket_name}/{destination_blob}")
