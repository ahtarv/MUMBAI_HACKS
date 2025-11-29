# rag_final_improved.py
from google.cloud import storage
import pickle
import json
import re

class ImprovedLegalRAG:
    def __init__(self, bucket_name='draftzi'):
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)
        self.documents = []
        self.config = None
        
    # Add this to your rag_final.py file in the ImprovedLegalRAG class
def query_legal_documents(self, query):
    """Compatibility method for legal_agent.py"""
    return self.query_documents(query)

    def load_final(self):
        """Load the improved RAG pipeline"""
        print("🚀 Loading IMPROVED RAG Pipeline...")
        
        try:
            self._download_file('legal_mapping.pk1', 'temp_mapping.pkl')
            self._download_file('adapter_config.json', 'temp_config.json')
            
            with open('temp_mapping.pkl', 'rb') as f:
                raw_data = pickle.load(f)
            
            self.documents = self._parse_documents_improved(raw_data)
            
            with open('temp_config.json', 'r') as f:
                self.config = json.load(f)
            
            print(f"📚 Loaded {len(self.documents)} legal documents")
            print(f"⚙️  Model: {self.config.get('base_model_name_or_path', 'Unknown')}")
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def _parse_documents_improved(self, raw_data):
        """Improved document parsing with better classification"""
        documents = []
        
        for doc_str in raw_data:
            if "Answer:" in doc_str:
                parts = doc_str.split("Answer:", 1)
                prompt = parts[0].strip()
                answer = parts[1].strip() if len(parts) > 1 else ""
                
                doc_name = self._extract_doc_name(prompt)
                
                documents.append({
                    'prompt': prompt,
                    'answer': answer,
                    'name': doc_name,
                    'type': self._classify_document_improved(doc_name, answer)
                })
        
        return documents
    
    def _classify_document_improved(self, doc_name, answer):
        """Improved document classification"""
        doc_lower = doc_name.lower()
        answer_lower = answer.lower()
        
        # More specific classification
        if any(keyword in doc_lower for keyword in ['nda', 'non-disclosure', 'confidentiality']):
            return 'nda'
        elif any(keyword in doc_lower for keyword in ['employment', 'employee', 'work contract']):
            return 'employment'
        elif any(keyword in doc_lower for keyword in ['llc', 'operating agreement', 'partnership', 'business']):
            return 'business'
        elif any(keyword in doc_lower for keyword in ['contract', 'agreement']):
            return 'contract'
        elif any(keyword in doc_lower for keyword in ['policy', 'guideline', 'procedure']):
            return 'policy'
        elif any(keyword in doc_lower for keyword in ['notice', 'warning', 'termination']):
            return 'hr'
        elif any(keyword in doc_lower for keyword in ['safety', 'health', 'workplace']):
            return 'compliance'
        else:
            return 'general'
    
    def _extract_doc_name(self, prompt):
        """Extract document name from prompt"""
        match = re.search(r'Generate a document:\s*(.+)', prompt)
        if match:
            return match.group(1).strip()
        return "Unknown Document"
    
    def _download_file(self, blob_name, local_path):
        """Download a file from GCS"""
        blob = self.bucket.blob(blob_name)
        blob.download_to_filename(local_path)
        print(f"   📥 Downloaded: {blob_name}")
    
    def query_documents(self, query):
        """Query documents with improved relevance"""
        print(f"\n🔍 Query: '{query}'")
        
        query_lower = query.lower()
        relevant_docs = []
        
        for doc in self.documents[:200]:  # Search more documents
            score = self._calculate_improved_relevance(query_lower, doc)
            
            if score > 0.2:  # Higher threshold for better quality
                relevant_docs.append({
                    'name': doc['name'],
                    'type': doc['type'],
                    'score': score,
                    'preview': doc['answer'][:200] + "..." if len(doc['answer']) > 200 else doc['answer']
                })
        
        # Sort by relevance and filter by type match
        relevant_docs.sort(key=lambda x: x['score'], reverse=True)
        
        # Filter to only show truly relevant documents
        filtered_docs = [doc for doc in relevant_docs if self._is_truly_relevant(query_lower, doc)]
        
        return {
            'query': query,
            'relevant_count': len(filtered_docs),
            'total_documents': len(self.documents),
            'relevant_docs': filtered_docs[:5],
            'answer': self._generate_improved_answer(query, filtered_docs)
        }
    
    def _calculate_improved_relevance(self, query, doc):
    """More accurate relevance scoring"""
    score = 0.0  # Remove the "???? IG" part
    
    # Handle both dictionary and string document types
    if isinstance(doc, dict):
        doc_name_lower = doc.get('name', '').lower()
        doc_content_lower = doc.get('answer', '').lower()
    else:
        doc_name_lower = str(doc).lower()
        doc_content_lower = str(doc).lower()
    
    query_lower = query.lower()
    query_words = set(query_lower.split())
    
    # Check for exact document type matches
    if 'nda' in query_lower and any(keyword in doc_name_lower for keyword in ['nda', 'non-disclosure']):
        score += 1.0
    if 'employment' in query_lower and any(keyword in doc_name_lower for keyword in ['employment', 'employee']):
        score += 1.0
    if 'llc' in query_lower and 'llc' in doc_name_lower:
        score += 1.0
    if 'partnership' in query_lower and 'partnership' in doc_name_lower:
        score += 1.0
    if 'contract' in query_lower and 'contract' in doc_name_lower:
        score += 0.8
    if 'agreement' in query_lower and 'agreement' in doc_name_lower:
        score += 0.8
        
    # Content matching (lower weight)
    for word in query_words:
        if len(word) > 4 and word in doc_content_lower:
            score += 0.1
    
    return min(score, 1.0)
    return min(score, 1.0)
    
    def _is_truly_relevant(self, query, doc):
        """Check if document is truly relevant to query"""
        if doc['score'] < 0.3:
            return False
            
        # Type-based relevance checks
        if 'nda' in query and doc['type'] != 'nda':
            return False
        if 'employment' in query and doc['type'] not in ['employment', 'hr']:
            return False
        if any(keyword in query for keyword in ['llc', 'partnership', 'business']) and doc['type'] != 'business':
            return False
            
        return True
    
    def _generate_improved_answer(self, query, relevant_docs):
        """Generate better answers based on actual document content"""
        if not relevant_docs:
            return "No specific legal documents matched your query exactly. Try using more specific terms or browse general legal templates."
        
        # Count documents by type
        type_counts = {}
        for doc in relevant_docs:
            type_counts[doc['type']] = type_counts.get(doc['type'], 0) + 1
        
        top_type = max(type_counts.items(), key=lambda x: x[1])[0] if type_counts else 'general'
        
        if 'nda' in query.lower():
            return f"Found {len(relevant_docs)} Non-Disclosure Agreement templates. These include mutual and one-way NDAs with comprehensive confidentiality clauses."
        
        elif 'employment' in query.lower():
            return f"Found {len(relevant_docs)} employment-related documents including contracts, policies, and workplace guidelines."
        
        elif any(keyword in query.lower() for keyword in ['llc', 'partnership', 'business']):
            return f"Found {len(relevant_docs)} business formation documents covering entity structure, governance, and operational agreements."
        
        else:
            return f"Found {len(relevant_docs)} relevant legal documents. The most common type is {top_type} documents."

# Test the improved version
def test_improved_rag():
    rag = ImprovedLegalRAG()
    if rag.load_final():
        print("\n🎉 IMPROVED RAG SYSTEM READY!")
        
        test_queries = [
            "Generate a mutual NDA",
            "Create employment contract", 
            "LLC operating agreement",
            "Partnership agreement"
        ]
        
        for query in test_queries:
            result = rag.query_documents(query)
            print(f"\n{'='*50}")
            print(f"💬 {query}")
            print(f"📊 {result['relevant_count']} relevant of {result['total_documents']} total")
            print(f"💡 {result['answer']}")
            
            if result['relevant_docs']:
                print("\n🔍 Top Documents:")
                for i, doc in enumerate(result['relevant_docs'][:3], 1):
                    print(f"   {i}. {doc['name']}")
                    print(f"      Type: {doc['type']}, Score: {doc['score']:.2f}")
    else:
        print("❌ Improved RAG failed")

if __name__ == "__main__":
    test_improved_rag()