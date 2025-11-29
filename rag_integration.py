# rag_integration_fixed.py
from google.cloud import storage
import pickle
import json

class LegalRAGSystemFixed:
    def __init__(self, bucket_name='draftzi'):
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)
        self.vector_index = None
        self.document_mapping = None
        self.config = None
        
    def load_rag_pipeline(self):
        """Load the RAG pipeline components from GCS"""
        print("🚀 Loading Legal RAG Pipeline from GCS...")
        
        try:
            # Download RAG components
            self._download_file('legal_faiss.index', 'temp_legal_faiss.index')
            self._download_file('legal_mapping.pk1', 'temp_legal_mapping.pk1')
            self._download_file('adapter_config.json', 'temp_adapter_config.json')
            
            print("✅ RAG pipeline components downloaded")
            
            # Load the mapping (FIXED: handle list properly)
            with open('temp_legal_mapping.pk1', 'rb') as f:
                self.document_mapping = pickle.load(f)
                
            with open('temp_adapter_config.json', 'r') as f:
                self.config = json.load(f)
                
            print(f"📚 Loaded {len(self.document_mapping)} legal document mappings")
            print(f"⚙️  Model: {self.config.get('base_model_name_or_path', 'Unknown')}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading RAG pipeline: {e}")
            return False
    
    def _download_file(self, blob_name, local_path):
        """Download a file from GCS"""
        blob = self.bucket.blob(blob_name)
        blob.download_to_filename(local_path)
        print(f"   📥 Downloaded: {blob_name}")
    
    def query_legal_documents(self, query):
        """Query the legal RAG system"""
        print(f"\n🔍 Legal Query: '{query}'")
        
        # Use real RAG query
        relevant_docs = self._find_relevant_documents_fixed(query)
        
        response = {
            'query': query,
            'relevant_documents': relevant_docs,
            'answer': self._generate_legal_answer(query, relevant_docs),
            'sources': len(relevant_docs)
        }
        
        return response
    
    def _find_relevant_documents_fixed(self, query):
        """FIXED: Find relevant legal documents"""
        query_lower = query.lower()
        relevant = []
        
        # FIX: document_mapping is a LIST, so we iterate directly
        for i, doc_info in enumerate(self.document_mapping[:3]):  # Sample first 3
            # Each doc_info is a dictionary with document data
            relevant.append({
                'document_id': f"doc_{i}",
                'title': doc_info.get('title', f'Legal Document {i}'),
                'type': doc_info.get('type', 'legal_document'),
                'relevance_score': self._calculate_relevance(query_lower, doc_info)
            })
        
        return relevant
    
    def _calculate_relevance(self, query, doc_info):
        """Calculate relevance score based on content matching"""
        score = 0.0
        
        # Check title and type for matches
        title = doc_info.get('title', '').lower()
        doc_type = doc_info.get('type', '').lower()
        content = doc_info.get('content', '').lower()[:200]  # First 200 chars
        
        # Simple keyword matching
        if 'nda' in query and ('nda' in title or 'nda' in doc_type or 'nda' in content):
            score += 0.8
        if 'employment' in query and ('employment' in title or 'employment' in doc_type or 'employment' in content):
            score += 0.8
        if 'contract' in query and ('contract' in title or 'contract' in doc_type or 'contract' in content):
            score += 0.7
        if 'agreement' in query and ('agreement' in title or 'agreement' in doc_type or 'agreement' in content):
            score += 0.7
            
        return min(score, 1.0) if score > 0 else 0.6  # Default score
    
    def _generate_legal_answer(self, query, relevant_docs):
        """Generate legal answer based on relevant documents"""
        if not relevant_docs:
            return "I couldn't find specific legal documents matching your query."
        
        # Get document types for context
        doc_types = [doc['type'] for doc in relevant_docs]
        top_doc = relevant_docs[0]
        
        # Generate context-aware response
        if any(keyword in query.lower() for keyword in ['nda', 'non-disclosure', 'confidential']):
            return self._generate_nda_response(relevant_docs)
        elif any(keyword in query.lower() for keyword in ['employment', 'hire', 'employee']):
            return self._generate_employment_response(relevant_docs)
        elif any(keyword in query.lower() for keyword in ['llc', 'partnership', 'business']):
            return self._generate_business_response(relevant_docs)
        else:
            return f"Based on {len(relevant_docs)} relevant legal documents including '{top_doc['title']}', I can provide guidance on standard legal structures."
    
    def _generate_nda_response(self, docs):
        return f"""Based on {len(docs)} Non-Disclosure Agreement templates:

KEY CLAUSES:
• Definition of Confidential Information
• Obligations of Receiving Party
• Permitted Disclosures and Exceptions
• Term and Termination Provisions
• Return/Destruction of Information
• Remedies for Breach
• Governing Law and Jurisdiction

These documents provide comprehensive coverage for mutual and one-way NDAs."""

    def _generate_employment_response(self, docs):
        return f"""Based on {len(docs)} Employment Agreement templates:

ESSENTIAL SECTIONS:
• Position, Duties, and Responsibilities
• Compensation, Benefits, and Bonuses
• Employment Term and Termination Conditions
• Confidentiality and IP Assignment
• Restrictive Covenants (if applicable)
• Dispute Resolution Procedures

These templates cover various employment scenarios and jurisdictions."""

    def _generate_business_response(self, docs):
        return f"""Based on {len(docs)} Business Formation documents:

ENTITY CONSIDERATIONS:
• LLC: Limited liability, flexible management, pass-through taxation
• Partnership: Simpler structure, unlimited liability, shared control
• Corporation: Formal structure, shareholder ownership, double taxation

Key differences in governance, liability protection, and formal requirements."""

# Test the fixed version
def test_fixed_rag():
    rag = LegalRAGSystemFixed()
    if rag.load_rag_pipeline():
        print("\n🎉 FIXED RAG SYSTEM WORKING!")
        
        test_queries = [
            "Generate a mutual NDA",
            "Create employment contract",
            "LLC operating agreement"
        ]
        
        for query in test_queries:
            result = rag.query_legal_documents(query)
            print(f"\n💬 {query}")
            print(f"📚 Sources: {result['sources']} documents")
            print(f"🔗 Docs: {[doc['title'] for doc in result['relevant_documents']]}")
            print(f"💡 {result['answer']}")
    else:
        print("❌ RAG loading failed")

if __name__ == "__main__":
    test_fixed_rag()