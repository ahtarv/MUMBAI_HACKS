# inspect_data.py
import pickle
import json

def inspect_rag_data():
    print("🔍 Inspecting RAG Data Structure...")
    
    try:
        # Load the mapping file
        with open('temp_legal_mapping.pk1', 'rb') as f:
            mapping_data = pickle.load(f)
        
        print(f"📊 Type of mapping data: {type(mapping_data)}")
        print(f"📊 Length: {len(mapping_data) if hasattr(mapping_data, '__len__') else 'N/A'}")
        
        # Show first few items
        if isinstance(mapping_data, list):
            print(f"\n📄 First 3 items:")
            for i, item in enumerate(mapping_data[:3]):
                print(f"  {i}. Type: {type(item)}")
                print(f"     Preview: {str(item)[:100]}...")
        else:
            print(f"📄 Data: {str(mapping_data)[:200]}...")
        
        # Load config
        with open('temp_adapter_config.json', 'r') as f:
            config = json.load(f)
        print(f"\n⚙️  Model: {config.get('base_model_name_or_path', 'Unknown')}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    inspect_rag_data()