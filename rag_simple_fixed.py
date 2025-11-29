# rag_simple_fixed.py
from google.cloud import storage
import pickle
import json

class SimpleLegalRAG:
    def __init__(self, bucket_name='draftzi'):
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)
        self.document_texts = []  # Store document texts
        self.config = None
        
    def load_simple(self):
        """Load RAG with simple text handling"""
        print("🚀 Loading Simple RAG Pipeline...")
        
        try:
            # Download files
            self._download_file('legal_mapping.pk1', 'temp_mapping.pkl')
            self._download_file('adapter_config.json', 'temp_config.json')
            
            # Load mapping (it's a list of strings)
            with open('temp_mapping.pkl', 'rb') as f:
                document_data = pickle.load(f)
            
            # Handle different data types
            if isinstance(document_data, list):
                if all(isinstance(item, str) for item in document_data):
                    # It's a list of strings (document texts)
                    self.document_texts = document_data
                    print(f"📚 Loaded {len(self.document_texts)} document texts")
                elif all(isinstance(item, dict) for item in document_data):
                    # It's a list of dictionaries
                    self.document_texts = [item.get('text', str(item)) for item in document_data]
                    print(f"📚 Loaded {len(self.document_texts)} document dictionaries")
                else:
                    # Mixed types, convert to strings
                    self.document_texts = [str(item) for item in document_data]
                    print(f"📚 Loaded {len(self.document_texts)} mixed documents")
            else:
                # Single item, make it a list
                self.document_texts = [str(document_data)]
                print(f"📚 Loaded 1 document")
            
            # Load config
            with open('temp_config.json', 'r') as f:
                self.config = json.load(f)
            
            print(f"⚙️  Model: {self.config.get('base_model_name_or_path', 'Unknown')}")
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def _download_file(self, blob_name, local_path):
        """Download a file from GCS"""
        blob = self.bucket.blob(blob_name)
        blob.download_to_filename(local_path)
        print(f"   📥 Downloaded: {blob_name}")
    
    def query_documents(self, query):
        """Simple query using text matching"""
        print(f"\n🔍 Query: '{query}'")
        
        # Simple keyword matching
        query_lower = query.lower()
        relevant_docs = []
        
        for i, doc_text in enumerate(self.document_texts[:5]):  # Check first 5 docs
            doc_str = str(doc_text).lower()
            
            # Calculate simple relevance score
            score = 0
            keywords = query_lower.split()
            for keyword in keywords:
                if len(keyword) > 3 and keyword in doc_str:  # Only meaningful words
                    score += 0.2
            
            if score > 0:
                # Extract a preview of the document
                preview = doc_str[:100] + "..." if len(doc_str) > 100 else doc_str
                relevant_docs.append({
                    'doc_id': i,
                    'score': min(score, 1.0),
                    'preview': preview
                })
        
        # Sort by relevance
        relevant_docs.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            'query': query,
            'relevant_count': len(relevant_docs),
            'total_documents': len(self.document_texts),
            'relevant_docs': relevant_docs[:3],  # Top 3
            'answer': self._generate_answer(query, relevant_docs)
        }
    
    def _generate_answer(self, query, relevant_docs):
        """Generate answer based on relevant documents"""
        if not relevant_docs:
            return "No specific legal documents matched your query. Try using terms like 'NDA', 'contract', 'employment', or 'agreement'."
        
        # Analyze what we found
        doc_previews = [doc['preview'] for doc in relevant_docs]
        
        if any('nda' in query.lower() or 'non-disclosure' in query.lower() for keyword in ['nda', 'confidential']):
            return f"Found {len(relevant_docs)} NDA-related documents. Key elements include confidentiality definitions, permitted disclosures, term duration, and breach remedies."
        
        elif any(keyword in query.lower() for keyword in ['employment', 'hire', 'employee']):
            return f"Found {len(relevant_docs)} employment-related documents. Typical sections cover position details, compensation, termination conditions, and confidentiality."
        
        elif any(keyword in query.lower() for keyword in ['llc', 'partnership', 'business']):
            return f"Found {len(relevant_docs)} business formation documents. Key considerations include liability protection, governance structure, and ownership terms."
        
        else:
            return f"Found {len(relevant_docs)} relevant legal documents. The documents appear to cover standard legal clauses and structures."

# Test the simple version
def test_simple_rag():
    rag = SimpleLegalRAG()
    if rag.load_simple():
        print("\n🎉 SIMPLE RAG WORKING!")
        
        test_queries = [
            "Generate a mutual NDA",
            "Create employment contract", 
            "LLC operating agreement",
            "Partnership agreement requirements"
        ]
        
        for query in test_queries:
            result = rag.query_documents(query)
            print(f"\n💬 '{query}'")
            print(f"📊 Found {result['relevant_count']}/{result['total_documents']} relevant docs")
            print(f"💡 {result['answer']}")
            
            if result['relevant_docs']:
                print("🔍 Top matches:")
                for doc in result['relevant_docs']:
                    print(f"   • Score: {doc['score']:.1f} - {doc['preview']}")
    else:
        print("❌ Simple RAG failed")

if __name__ == "__main__":
    test_simple_rag()