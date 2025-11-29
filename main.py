# main.py - CORRECTED VERSION
from agents.legal_agent import LegalAgent
from tools.legal_calculator import LegalCalculator
import time

# FIXED IMPORT - Use the correct class name from your rag_final.py
from rag_final import ImprovedLegalRAG

class LegalAISystem:
    def __init__(self, rag_pipeline=None):
        # Use real RAG if provided, otherwise create mock for demo
        if rag_pipeline:
            self.rag = rag_pipeline
            self.rag_available = True
        else:
            self.rag = self._create_mock_rag()
            self.rag_available = False
            
        self.agent = LegalAgent(self.rag)
        self.calculator = LegalCalculator()
        
        print("⚖️ Legal Agentic AI System Initialized!")
        if self.rag_available:
            print("   ✅ Powered by REAL RAG with 5,069 legal documents")
        else:
            print("   ⚠️  Using DEMO MODE - RAG system not connected")
        print("   - Agentic reasoning with multi-tool capabilities")
        print("   - Ready for complex legal document generation\n")
    
    def _create_mock_rag(self):
        """Create mock RAG for demo purposes"""
        class MockRAG:
            def generate_doc(self, query):
                return f"""
**LEGAL DOCUMENT: {query.upper()}**

This is a comprehensive legal document generated from our 5,000+ document training corpus.

KEY SECTIONS:
1. Definitions and Interpretation
2. Core Obligations and Responsibilities  
3. Term and Termination
4. Confidentiality and Data Protection
5. Liability and Indemnification
6. Dispute Resolution and Governing Law
7. General Provisions

[Document tailored to your specific request]
"""
            
            def query_legal_documents(self, query):
                return {
                    'query': query,
                    'relevant_documents': [
                        {'title': 'Sample NDA Template', 'type': 'nda', 'relevance_score': 0.92},
                        {'title': 'Confidentiality Agreement', 'type': 'agreement', 'relevance_score': 0.87}
                    ],
                    'answer': f"Based on legal document analysis: {query} would typically include standard clauses for definitions, obligations, term, and termination.",
                    'sources': 2
                }
        return MockRAG()
    
    def process_request(self, user_input):
        """Main entry point for all legal requests"""
        print(f"🧠 Processing: {user_input}")
        
        # DEBUG: Show if we're using real RAG
        if hasattr(self.rag, 'documents'):
            print(f"🔍 MODE: REAL RAG with {len(self.rag.documents)} documents")
        else:
            print("🔍 MODE: DEMO (mock responses)")
            
        print("=" * 60)
        
        start_time = time.time()
        
        # Let the agent decide how to handle this request
        response = self.agent.process_query(user_input)
        
        end_time = time.time()
        
        print(f"\n⏱️  Processing time: {end_time - start_time:.2f}s")
        print("=" * 60)
        
        return response

def initialize_with_real_rag():
    """Initialize with REAL RAG system"""
    print("🔄 Initializing REAL RAG Pipeline...")
    try:
        rag_system = ImprovedLegalRAG()
        if rag_system.load_final():
            print("✅ REAL RAG Pipeline successfully loaded!")
            return rag_system
        else:
            print("❌ Failed to load RAG pipeline, using demo mode")
            return None
    except Exception as e:
        print(f"❌ Error initializing RAG: {e}")
        return None

def main():
    # Try to initialize with real RAG first
    rag_pipeline = initialize_with_real_rag()
    
    # Create the agentic system
    legal_ai = LegalAISystem(rag_pipeline)
    
    # Interactive demo
    print("\n🚀 LEGAL AGENTIC AI - INTERACTIVE MODE")
    print("Type 'quit' to exit\n")
    
    while True:
        user_input = input("\n💬 Your legal request: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("👋 Thank you for using Legal Agentic AI!")
            break
            
        if not user_input:
            continue
            
        response = legal_ai.process_request(user_input)
        print(f"\n{response}")

def demo_mode():
    """Run a quick demo with sample queries"""
    rag_pipeline = initialize_with_real_rag()
    legal_ai = LegalAISystem(rag_pipeline)
    
    demo_queries = [
        "Generate a mutual NDA for software development",
        "Create employment contract with non-compete clause",
        "LLC operating agreement requirements",
        "Partnership agreement for small business"
    ]
    
    print("🚀 QUICK DEMO: LEGAL AGENTIC AI")
    print("=" * 50)
    
    for query in demo_queries:
        print(f"\n💬 Query: {query}")
        print("-" * 40)
        legal_ai.process_request(query)

if __name__ == "__main__":
    # You can run either interactive mode or demo mode
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo_mode()
    else:
        main()