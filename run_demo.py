# run_demo.py
from main import LegalAISystem

# Mock RAG for testing
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

def quick_demo():
    print("🚀 QUICK DEMO: LEGAL AGENTIC AI")
    print("=" * 50)
    
    rag = MockRAG()
    legal_ai = LegalAISystem(rag)
    
    test_queries = [
        "Generate a mutual NDA for software development",
        "Calculate 5% late fee on $2000 rent for 15 days",
        "Create employment contract with non-compete clause",
        "Compare partnership agreement and LLC operating agreement"
    ]
    
    for query in test_queries:
        print(f"\n💬 Query: {query}")
        print("-" * 40)
        response = legal_ai.process_request(query)
        print(response)
        print("=" * 50)

if __name__ == "__main__":
    quick_demo()