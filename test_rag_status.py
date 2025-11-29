# test_rag_status.py
from main import initialize_with_real_rag

def test_rag_status():
    print("🔍 Testing RAG Pipeline Status...")
    
    rag = initialize_with_real_rag()
    
    if rag:
        print("✅ REAL RAG IS WORKING!")
        print(f"📊 Document mappings: {len(rag.document_mapping) if hasattr(rag, 'document_mapping') else 'None'}")
        
        # Test a real query
        result = rag.query_legal_documents("test NDA")
        print(f"🔍 Query test: {result['sources']} sources found")
        print(f"💡 Response type: {'REAL' if 'Based on' in result['answer'] else 'MOCK'}")
    else:
        print("❌ RAG IS IN DEMO MODE")
        print("💡 You're seeing generic template responses")

if __name__ == "__main__":
    test_rag_status()