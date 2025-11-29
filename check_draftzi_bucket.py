# check_draftzi_bucket.py
from google.cloud import storage
import os

def explore_draftzi_bucket():
    """Explore your draftzi GCS bucket"""
    BUCKET_NAME = "draftzi"
    
    try:
        print(f"🔍 Exploring bucket: {BUCKET_NAME}")
        
        # Setup client
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        
        # Check if bucket exists
        if not bucket.exists():
            print(f"❌ Bucket '{BUCKET_NAME}' does not exist or you don't have access")
            print("💡 You might need to set up GCS credentials first")
            return
        
        print(f"✅ Bucket '{BUCKET_NAME}' exists!")
        
        # List all files
        blobs = list(bucket.list_blobs())
        print(f"📊 Total files found: {len(blobs)}")
        
        if not blobs:
            print("📭 Bucket is empty")
            return
        
        # Group by folder
        folders = {}
        for blob in blobs:
            folder = os.path.dirname(blob.name) if '/' in blob.name else "root"
            if folder not in folders:
                folders[folder] = []
            folders[folder].append({
                'name': blob.name,
                'size': blob.size,
                'updated': blob.updated
            })
        
        # Print folder structure
        print("\n📁 BUCKET STRUCTURE:")
        for folder, files in sorted(folders.items()):
            print(f"\n📂 {folder}/:")
            for file_info in sorted(files, key=lambda x: x['name']):
                size_str = f"({file_info['size']} bytes)" if file_info['size'] > 0 else "(empty)"
                print(f"   📄 {file_info['name']} {size_str}")
        
        # Look for Python files specifically
        python_files = [blob for blob in blobs if blob.name.endswith('.py')]
        if python_files:
            print(f"\n🐍 PYTHON FILES FOUND ({len(python_files)}):")
            for py_file in python_files:
                print(f"   🔸 {py_file.name}")
                
                # Download main.py if found
                if 'main.py' in py_file.name.lower():
                    print(f"   ⬇️  Downloading {py_file.name}...")
                    local_filename = f"downloaded_{os.path.basename(py_file.name)}"
                    py_file.download_to_filename(local_filename)
                    print(f"   ✅ Downloaded to {local_filename}")
                    
                    # Show first lines
                    try:
                        with open(local_filename, 'r', encoding='utf-8') as f:
                            content = f.read()
                            print(f"   📝 First 10 lines of {py_file.name}:")
                            print("-" * 50)
                            for i, line in enumerate(content.split('\n')[:10]):
                                if line.strip():  # Skip empty lines
                                    print(f"   {i+1}: {line}")
                            print("-" * 50)
                    except Exception as e:
                        print(f"   ❌ Error reading file: {e}")
        
        # Also look for model files
        model_files = [blob for blob in blobs if any(ext in blob.name for ext in ['.pth', '.bin', '.safetensors', '.faiss', '.index'])]
        if model_files:
            print(f"\n🤖 MODEL FILES FOUND ({len(model_files)}):")
            for model_file in model_files:
                print(f"   🔹 {model_file.name} ({model_file.size} bytes)")
        
        return blobs
        
    except Exception as e:
        print(f"❌ Error accessing bucket: {e}")
        print("\n💡 You might need to set up GCS credentials:")
        print("   1. Download service account key from Google Cloud Console")
        print("   2. Save as 'service-account-key.json' in this folder")
        print("   3. Or set: set GOOGLE_APPLICATION_CREDENTIALS=path/to/key.json")
        return []

if __name__ == "__main__":
    explore_draftzi_bucket()