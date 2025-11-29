# check_gcs_bucket.py
from google.cloud import storage

def list_bucket_files(bucket_name):
    """List all files in your GCS bucket"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    
    print(f"📁 Files in bucket '{bucket_name}':")
    blobs = bucket.list_blobs()
    
    for blob in blobs:
        print(f"   📄 {blob.name} (Size: {blob.size} bytes)")
    
    return [blob.name for blob in blobs]

# Replace with your bucket name
your_bucket_name = "draftzi"  # ← CHANGE THIS
list_bucket_files(your_bucket_name)