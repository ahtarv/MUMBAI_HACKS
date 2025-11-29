import os
from google.cloud import storage

def test_gcs_connection():
    print("🔍 Testing GCS connection with service account...")
    
    try:
        # Initialize the client (will use your service account key)
        client = storage.Client()
        
        # List all buckets to test general access
        buckets = list(client.list_buckets())
        print(f"✅ Connected to GCS! Found {len(buckets)} buckets")
        
        # Try to access the specific 'draftzi' bucket
        bucket_name = 'draftzi'
        bucket = client.bucket(bucket_name)
        
        if bucket.exists():
            print(f"✅ Successfully accessed bucket: {bucket_name}")
            
            # List files in the bucket
            print("📁 Listing files in 'draftzi' bucket:")
            blobs = list(bucket.list_blobs(max_results=10))
            
            if blobs:
                for i, blob in enumerate(blobs, 1):
                    print(f"   {i}. {blob.name} ({blob.size} bytes)")
            else:
                print("   📭 Bucket is empty")
                
        else:
            print(f"❌ Bucket '{bucket_name}' not found or no access")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Troubleshooting tips:")
        print("1. Check if the bucket name 'draftzi' is correct")
        print("2. Verify the service account has 'Storage Object Viewer' role")
        print("3. Make sure the JSON key file path is correct")

if __name__ == "__main__":
    test_gcs_connection()