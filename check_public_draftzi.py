# check_public_draftzi.py
import requests
import os

def check_public_draftzi():
    """Check if draftzi bucket is publicly accessible"""
    bucket_name = "draftzi"
    
    print(f"🔍 Checking if '{bucket_name}' is publicly accessible...")
    
    # Common file patterns to check
    test_files = [
        "main.py",
        "app.py", 
        "requirements.txt",
        "README.md",
        "Python/main.py",
        "src/main.py",
        "backend/main.py",
        "api/main.py",
        "model/model.pth",
        "data/legal_docs.json"
    ]
    
    found_files = []
    
    for file_path in test_files:
        # Try different URL patterns
        urls = [
            f"https://storage.googleapis.com/{bucket_name}/{file_path}",
            f"https://{bucket_name}.storage.googleapis.com/{file_path}",
            f"https://storage.cloud.google.com/{bucket_name}/{file_path}"
        ]
        
        for url in urls:
            try:
                response = requests.head(url, timeout=5)
                if response.status_code == 200:
                    print(f"✅ FOUND: {file_path}")
                    print(f"   📎 URL: {url}")
                    found_files.append((file_path, url))
                    break
            except:
                continue
    
    if found_files:
        print(f"\n🎉 Found {len(found_files)} publicly accessible files!")
        
        # Download main.py if found
        for file_path, url in found_files:
            if 'main.py' in file_path:
                print(f"\n⬇️  Downloading {file_path}...")
                try:
                    response = requests.get(url)
                    with open("downloaded_main.py", "w", encoding="utf-8") as f:
                        f.write(response.text)
                    print("✅ Downloaded main.py successfully!")
                    
                    # Show content
                    with open("downloaded_main.py", "r") as f:
                        content = f.read()
                        print(f"\n📝 MAIN.PY CONTENT ({len(content)} characters):")
                        print("=" * 60)
                        print(content)
                        print("=" * 60)
                except Exception as e:
                    print(f"❌ Error downloading: {e}")
                
    else:
        print("❌ No publicly accessible files found.")
        print("\n💡 The bucket might be private. You have two options:")
        print("   1. Make the bucket public temporarily (for hackathon)")
        print("   2. Set up GCS credentials with a service account key")
    
    return found_files

if __name__ == "__main__":
    check_public_draftzi()