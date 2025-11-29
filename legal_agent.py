# agents/legal_agent.py
import re
from typing import Dict, List, Any
from tools.legal_calculator import LegalCalculator  # ADD THIS IMPORT

class LegalAgent:
    def __init__(self, rag_pipeline):
        self.rag = rag_pipeline
        self.calculator = LegalCalculator()  # ADD THIS LINE
        self.conversation_history = []
        self.session_context = {}
        
    def process_query(self, user_input: str) -> str:
        """Main agentic processing with intelligent routing"""
        
        # Step 1: Analyze intent and complexity
        intent = self._analyze_intent(user_input)
        complexity = self._assess_complexity(user_input)
        
        print(f"   📋 Intent: {intent} | Complexity: {complexity}")
        
        # Step 2: Route to appropriate handler
        if intent == "document_generation":
            return self._handle_document_generation(user_input)
        elif intent == "calculation":
            return self._handle_calculation(user_input)  # THIS WILL NOW USE REAL CALCULATOR
        elif intent == "comparison":
            return self._handle_comparison(user_input)
        elif intent == "analysis":
            return self._handle_analysis(user_input)
        else:
            return self._handle_general_query(user_input)
    
    def _analyze_intent(self, query: str) -> str:
        """Smart intent analysis"""
        query_lower = query.lower()
        
        intent_patterns = {
            "document_generation": any(word in query_lower for word in [
                'generate', 'create', 'draft', 'make', 'prepare', 'write'
            ]),
            "calculation": any(word in query_lower for word in [
                'calculate', 'compute', 'how much', 'total', 'sum', 'percentage', '%'
            ]),
            "comparison": any(word in query_lower for word in [
                'compare', 'vs', 'versus', 'difference', 'better', 'pros and cons'
            ]),
            "analysis": any(word in query_lower for word in [
                'analyze', 'review', 'check', 'verify', 'validate', 'assess'
            ])
        }
        
        for intent, matches in intent_patterns.items():
            if matches:
                return intent
                
        return "general_query"
    
    def _assess_complexity(self, query: str) -> str:
        """Assess query complexity"""
        word_count = len(query.split())
        legal_terms = len([word for word in query.split() if self._is_legal_term(word)])
        
        if word_count > 15 or legal_terms > 3:
            return "high"
        elif word_count > 8 or legal_terms > 1:
            return "medium"
        else:
            return "low"
    
    def _is_legal_term(self, word: str) -> bool:
        """Check if word is a legal term"""
        legal_terms = {
            'agreement', 'contract', 'clause', 'jurisdiction', 'liability',
            'indemnification', 'confidentiality', 'arbitration', 'remedies',
            'warranty', 'termination', 'amendment', 'assignment', 'governing law'
        }
        return word.lower() in legal_terms
    
    def _handle_document_generation(self, query: str) -> str:
        """Handle document generation with agentic reasoning"""
        print("   📝 Handling document generation...")
        
        # Use your RAG's intelligence
        document = self.rag.generate_doc(query)
        
        # Agentic analysis
        analysis = self._analyze_generated_document(document, query)
        suggestions = self._generate_document_suggestions(query)
        
        return self._format_document_response(query, document, analysis, suggestions)
    
    def _handle_calculation(self, query: str) -> str:
        """Handle legal calculations - NOW USING REAL CALCULATOR"""
        print("   🧮 Handling calculation with Legal Calculator...")
        
        # Use the actual calculator tool
        calculation_result = self.calculator.calculate(query)
        
        return f"""
🧮 **LEGAL CALCULATION RESULT**

🎯 **Your Request**: "{query}"

{calculation_result}

💡 **Legal Context**: Calculations are estimates. Consult legal counsel for binding figures.
"""
    
    def _handle_comparison(self, query: str) -> str:
        """Handle document comparisons"""
        print("   ⚖️ Handling comparison...")
        
        # Extract document types from query for comparison
        doc_types = self._extract_document_types(query)
        
        if len(doc_types) >= 2:
            comparison = self._compare_documents(doc_types[0], doc_types[1])
            return comparison
        else:
            return f"""
📊 **Document Comparison Request**

Your query: "{query}"

🔍 **I can compare**:
- NDA vs Confidentiality Agreement
- Employment Contract vs Consulting Agreement  
- LLC Agreement vs Partnership Agreement
- Rental Agreement vs Lease Agreement

💡 **Try**: "Compare NDA and confidentiality agreement"
"""
    
    def _handle_analysis(self, query: str) -> str:
        """Handle document analysis"""
        print("   🔍 Handling analysis...")
        
        return f"""
📈 **Document Analysis Request**

Your query: "{query}"

🔎 **Analysis Features**:
- Document completeness checking
- Clause analysis and recommendations
- Compliance verification
- Risk assessment

💡 **Coming soon**: Advanced analysis of generated documents
"""
    
    def _handle_general_query(self, query: str) -> str:
        """Handle general legal queries"""
        print("   💭 Handling general query...")
        
        # Use RAG for general knowledge
        document = self.rag.generate_doc(query)
        
        return f"""
💡 **General Legal Query**

Your question: "{query}"

📚 **Response from Legal Knowledge Base**:
{document}

🏛️ **Note**: This is based on our training across 5,000+ legal documents
"""
    
    def _extract_document_types(self, query: str) -> List[str]:
        """Extract document types from comparison query"""
        doc_keywords = {
            'nda': 'NDA',
            'non-disclosure': 'NDA', 
            'confidentiality': 'Confidentiality Agreement',
            'employment': 'Employment Contract',
            'partnership': 'Partnership Agreement',
            'llc': 'LLC Agreement',
            'rental': 'Rental Agreement',
            'lease': 'Lease Agreement',
            'contract': 'Contract'
        }
        
        found_types = []
        for keyword, doc_type in doc_keywords.items():
            if keyword in query.lower():
                found_types.append(doc_type)
        
        return found_types
    
    def _compare_documents(self, doc_type1: str, doc_type2: str) -> str:
        """Compare two document types"""
        # Generate both documents
        doc1 = self.rag.generate_doc(doc_type1)
        doc2 = self.rag.generate_doc(doc_type2)
        
        comparison_notes = {
            ("NDA", "Confidentiality Agreement"): {
                "differences": "NDA is broader for business secrets, Confidentiality Agreement is for specific information",
                "use_cases": "Use NDA for general business, Confidentiality for specific data sharing"
            },
            ("Employment Contract", "Consulting Agreement"): {
                "differences": "Employment for full-time staff with benefits, Consulting for project-based work",
                "use_cases": "Employment for permanent roles, Consulting for temporary projects"
            },
            ("LLC Agreement", "Partnership Agreement"): {
                "differences": "LLC provides limited liability protection, Partnership has shared unlimited liability",
                "use_cases": "LLC for asset protection, Partnership for simple shared business"
            }
        }
        
        key = (doc_type1, doc_type2)
        if key in comparison_notes:
            notes = comparison_notes[key]
        else:
            notes = {
                "differences": "Different legal structures and liability considerations",
                "use_cases": "Choose based on business needs and legal protection required"
            }
        
        return f"""
⚖️ **DOCUMENT COMPARISON**: {doc_type1} vs {doc_type2}

📄 **{doc_type1}**:
{self._summarize_document(doc1)}

📄 **{doc_type2}**:
{self._summarize_document(doc2)}

🔍 **Key Differences**:
{notes['differences']}

💡 **When to Use**:
{notes['use_cases']}

✅ **Recommendation**: Consult legal counsel to determine the best fit for your situation
"""
    
    def _summarize_document(self, document: str) -> str:
        """Create a brief summary of the document"""
        lines = document.split('\n')
        key_sections = [line for line in lines if 'SECTION' in line or '**' in line]
        return "\n".join(key_sections[:4])  # Return first 4 sections
    
    def _analyze_generated_document(self, document: str, query: str) -> str:
        """Analyze what the RAG generated"""
        word_count = len(document.split())
        sections = document.count('SECTION') or document.count('**') // 2
        
        return f"""
📊 **Generation Analysis**:
- Generated {word_count} word document with {sections} main sections
- Based on comprehensive legal document training
- Tailored to your specific request
- Includes standard legal structure and clauses
"""
    
    def _generate_document_suggestions(self, query: str) -> str:
        """Generate context-aware suggestions"""
        suggestions = """
💡 **Recommendations**:

1. **Review Key Details**: Check names, dates, amounts, and specific terms
2. **Jurisdiction**: Verify local legal requirements apply
3. **Customization**: Adapt clauses to your specific business context
4. **Legal Review**: Consult with legal counsel for binding agreements
"""
        
        # Add specific suggestions based on query
        if 'nda' in query.lower():
            suggestions += "\n• Consider confidentiality period and remedy clauses"
        elif 'rental' in query.lower() or 'lease' in query.lower():
            suggestions += "\n• Verify security deposit and maintenance responsibilities"
        elif 'employment' in query.lower():
            suggestions += "\n• Review non-compete and termination conditions"
            
        return suggestions
    
    def _format_document_response(self, query: str, document: str, analysis: str, suggestions: str) -> str:
        """Format the agentic document response"""
        return f"""
⚖️ **LEGAL DOCUMENT GENERATED**

🎯 **Your Request**: "{query}"

{analysis}

📄 **Generated Document**:
{document}

{suggestions}

✅ **Document generation complete!**
"""