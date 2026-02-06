"""
Technical Appendix: Implementation Examples
LLM-Assisted PRA COREP Reporting Assistant
"""

# ============================================================================
# APPENDIX A: Sample JSON Schema for COREP C 01.00 (Own Funds)
# ============================================================================

COREP_C0100_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "COREP C 01.00 - Own Funds",
    "type": "object",
    "required": ["template", "reporting_date", "currency", "fields"],
    "properties": {
        "template": {
            "type": "string",
            "const": "C01.00",
            "description": "COREP template identifier"
        },
        "reporting_date": {
            "type": "string",
            "format": "date",
            "description": "Reporting reference date (YYYY-MM-DD)"
        },
        "currency": {
            "type": "string",
            "enum": ["GBP", "EUR", "USD"],
            "description": "Reporting currency"
        },
        "fields": {
            "type": "object",
            "description": "Capital component fields",
            "properties": {
                "CET1_capital_instruments": {
                    "type": "object",
                    "required": ["value", "justification"],
                    "properties": {
                        "row": {"type": "string", "const": "010"},
                        "column": {"type": "string", "const": "010"},
                        "value": {"type": "number", "minimum": 0},
                        "justification": {
                            "type": "array",
                            "items": {"type": "string"},
                            "minItems": 1
                        },
                        "confidence": {
                            "type": "string",
                            "enum": ["high", "medium", "low"]
                        }
                    }
                },
                "share_premium": {
                    "type": "object",
                    "required": ["value", "justification"],
                    "properties": {
                        "row": {"type": "string", "const": "040"},
                        "column": {"type": "string", "const": "010"},
                        "value": {"type": "number", "minimum": 0},
                        "justification": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    }
                },
                "retained_earnings": {
                    "type": "object",
                    "required": ["value", "justification"],
                    "properties": {
                        "row": {"type": "string", "const": "050"},
                        "column": {"type": "string", "const": "010"},
                        "value": {"type": "number"},
                        "justification": {"type": "array", "items": {"type": "string"}}
                    }
                }
            }
        },
        "deductions": {
            "type": "object",
            "description": "CET1 deductions",
            "properties": {
                "intangible_assets": {
                    "type": "object",
                    "properties": {
                        "row": {"type": "string", "const": "120"},
                        "value": {"type": "number", "maximum": 0},
                        "justification": {"type": "array", "items": {"type": "string"}}
                    }
                }
            }
        }
    }
}


# ============================================================================
# APPENDIX B: RAG Retrieval Implementation
# ============================================================================

"""
RAG Retrieval System - Vector Database Setup
"""

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json

class RegulatoryRAG:
    """
    Retrieval-Augmented Generation system for regulatory text
    """
    
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """Initialize embedding model and vector store"""
        self.embedding_model = SentenceTransformer(model_name)
        self.dimension = 384  # MiniLM embedding dimension
        self.index = faiss.IndexFlatIP(self.dimension)  # Inner product (cosine sim)
        self.documents = []
        self.metadata = []
    
    def chunk_document(self, text, source, article=None, chunk_size=500):
        """
        Segment regulatory document into semantically coherent chunks
        
        Args:
            text: Full regulatory text
            source: Source document identifier (e.g., "PRA_Rulebook_OwnFunds_2024Q4")
            article: Article number (e.g., "Article 26")
            chunk_size: Target tokens per chunk
        
        Returns:
            List of (chunk_text, metadata) tuples
        """
        # Simple paragraph-based chunking (production would use semantic segmentation)
        paragraphs = text.split('\n\n')
        chunks = []
        
        current_chunk = ""
        for para in paragraphs:
            if len(current_chunk.split()) + len(para.split()) <= chunk_size:
                current_chunk += para + "\n\n"
            else:
                if current_chunk:
                    chunks.append((
                        current_chunk.strip(),
                        {
                            "source": source,
                            "article": article,
                            "chunk_id": f"{source}_{len(chunks)}"
                        }
                    ))
                current_chunk = para + "\n\n"
        
        if current_chunk:
            chunks.append((current_chunk.strip(), {
                "source": source, "article": article,
                "chunk_id": f"{source}_{len(chunks)}"
            }))
        
        return chunks
    
    def index_documents(self, document_chunks):
        """
        Generate embeddings and index documents
        
        Args:
            document_chunks: List of (text, metadata) tuples
        """
        texts = [chunk[0] for chunk in document_chunks]
        self.metadata = [chunk[1] for chunk in document_chunks]
        
        # Generate embeddings
        embeddings = self.embedding_model.encode(
            texts, 
            normalize_embeddings=True,  # For cosine similarity
            show_progress_bar=True
        )
        
        # Add to FAISS index
        self.index.add(embeddings.astype('float32'))
        self.documents = texts
        
        print(f"Indexed {len(texts)} document chunks")
    
    def retrieve(self, query, top_k=5):
        """
        Retrieve top-k most relevant regulatory passages
        
        Args:
            query: User question (e.g., "Where do I report retained earnings?")
            top_k: Number of passages to retrieve
        
        Returns:
            List of (text, metadata, similarity_score) tuples
        """
        # Embed query
        query_embedding = self.embedding_model.encode(
            [query], 
            normalize_embeddings=True
        ).astype('float32')
        
        # Search
        similarities, indices = self.index.search(query_embedding, top_k)
        
        # Format results
        results = []
        for idx, sim in zip(indices[0], similarities[0]):
            results.append({
                "text": self.documents[idx],
                "metadata": self.metadata[idx],
                "similarity": float(sim)
            })
        
        return results


# Example Usage
if __name__ == "__main__":
    # Initialize RAG system
    rag = RegulatoryRAG()
    
    # Example: Index PRA Rulebook Article 26 (CET1 components)
    pra_article_26 = """
    Article 26 - Common Equity Tier 1 items
    
    (1) Common Equity Tier 1 items shall comprise the following:
    
    (a) capital instruments, provided the conditions laid down in Article 28 or, 
    where applicable, Article 29 are met;
    
    (b) share premium accounts related to the instruments referred to in point (a);
    
    (c) retained earnings;
    
    (d) accumulated other comprehensive income;
    
    (e) other reserves;
    
    (f) funds for general banking risk referred to in Article 26(1)(f) of Regulation (EU) No 575/2013.
    
    (2) Minority interests shall be recognised in Common Equity Tier 1 capital only 
    where the conditions laid down in Article 84 are met.
    """
    
    chunks = rag.chunk_document(
        pra_article_26, 
        source="PRA_Rulebook_OwnFunds_2024Q4",
        article="Article 26"
    )
    
    rag.index_documents(chunks)
    
    # Test retrieval
    query = "Where should I report retained earnings in COREP C 01.00?"
    results = rag.retrieve(query, top_k=3)
    
    print("\n=== Retrieval Results ===")
    for i, result in enumerate(results, 1):
        print(f"\nResult {i} (Similarity: {result['similarity']:.3f})")
        print(f"Source: {result['metadata']['source']}")
        print(f"Article: {result['metadata']['article']}")
        print(f"Text: {result['text'][:200]}...")


# ============================================================================
# APPENDIX C: LLM Prompt Engineering for Schema-Constrained Output
# ============================================================================

SYSTEM_PROMPT = """
You are an expert regulatory reporting assistant specializing in PRA COREP returns.

Your task is to help analysts map business scenarios to COREP template fields based 
on PRA Rulebook and EBA instructions.

CRITICAL REQUIREMENTS:
1. Output ONLY valid JSON matching the provided schema - no additional commentary
2. Every field must include regulatory justification with specific article references
3. Assign confidence scores: "high" (clear guidance), "medium" (requires interpretation), 
   "low" (ambiguous or conflicting guidance)
4. If uncertain, prefer to flag for manual review rather than guess

You will be provided:
- User question/scenario
- Retrieved regulatory passages (from RAG system)
- JSON schema to populate

Generate structured output mapping the scenario to COREP fields.
"""

USER_PROMPT_TEMPLATE = """
User Question: {question}

Business Scenario:
{scenario}

Retrieved Regulatory Guidance:
{retrieved_passages}

Target Schema:
{json_schema}

Generate JSON output mapping this scenario to COREP fields. Include regulatory 
justifications with specific article references.
"""


# Example Prompt Construction
def construct_llm_prompt(question, scenario, rag_results, schema):
    """
    Build complete prompt for LLM
    
    Args:
        question: User's natural language question
        scenario: Structured business data (dict)
        rag_results: Retrieved regulatory passages from RAG
        schema: Target JSON schema
    
    Returns:
        Complete prompt string
    """
    # Format retrieved passages
    passages = "\n\n".join([
        f"--- Passage {i+1} ---\n"
        f"Source: {r['metadata']['source']}\n"
        f"Article: {r['metadata']['article']}\n"
        f"Text: {r['text']}"
        for i, r in enumerate(rag_results)
    ])
    
    # Format scenario
    scenario_str = json.dumps(scenario, indent=2)
    schema_str = json.dumps(schema, indent=2)
    
    # Construct prompt
    user_prompt = USER_PROMPT_TEMPLATE.format(
        question=question,
        scenario=scenario_str,
        retrieved_passages=passages,
        json_schema=schema_str
    )
    
    return SYSTEM_PROMPT, user_prompt


# ============================================================================
# APPENDIX D: Validation Rules Implementation
# ============================================================================

class COREPValidator:
    """
    Validation rules for COREP C 01.00 submissions
    """
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def validate_c0100(self, corep_output):
        """
        Apply C 01.00 validation rules
        
        Args:
            corep_output: Structured JSON output from LLM
        
        Returns:
            dict with validation results
        """
        self.errors = []
        self.warnings = []
        
        # Rule 1: Mandatory fields check
        self._check_mandatory_fields(corep_output)
        
        # Rule 2: Arithmetic consistency
        self._check_arithmetic_consistency(corep_output)
        
        # Rule 3: Value range validation
        self._check_value_ranges(corep_output)
        
        # Rule 4: Confidence-based warnings
        self._check_confidence_scores(corep_output)
        
        return {
            "validation_status": "passed" if not self.errors else "failed",
            "errors": self.errors,
            "warnings": self.warnings
        }
    
    def _check_mandatory_fields(self, data):
        """Ensure mandatory COREP rows are populated"""
        mandatory_fields = [
            'CET1_capital_instruments',
            'share_premium',
            'retained_earnings'
        ]
        
        for field in mandatory_fields:
            if field not in data.get('fields', {}):
                self.errors.append({
                    "rule": "MANDATORY_FIELD",
                    "field": field,
                    "message": f"Mandatory field '{field}' is missing"
                })
    
    def _check_arithmetic_consistency(self, data):
        """Validate that totals equal sum of components"""
        fields = data.get('fields', {})
        
        # Example: CET1 total should equal sum of components
        components = ['CET1_capital_instruments', 'share_premium', 'retained_earnings']
        component_sum = sum(
            fields.get(c, {}).get('value', 0) 
            for c in components
        )
        
        # Deductions should be negative
        deductions = data.get('deductions', {})
        deduction_sum = sum(
            d.get('value', 0) 
            for d in deductions.values()
        )
        
        if deduction_sum > 0:
            self.errors.append({
                "rule": "DEDUCTION_SIGN",
                "message": "Deductions must be negative values"
            })
    
    def _check_value_ranges(self, data):
        """Check for invalid value ranges"""
        fields = data.get('fields', {})
        
        for field_name, field_data in fields.items():
            value = field_data.get('value', 0)
            
            # Capital components should be non-negative
            if value < 0:
                self.errors.append({
                    "rule": "VALUE_RANGE",
                    "field": field_name,
                    "value": value,
                    "message": f"Capital component '{field_name}' cannot be negative"
                })
    
    def _check_confidence_scores(self, data):
        """Flag medium/low confidence outputs for review"""
        fields = data.get('fields', {})
        
        for field_name, field_data in fields.items():
            confidence = field_data.get('confidence', 'high')
            
            if confidence in ['medium', 'low']:
                self.warnings.append({
                    "severity": "medium" if confidence == "medium" else "high",
                    "field": field_name,
                    "message": f"Field marked as {confidence} confidence - requires analyst review",
                    "justification": field_data.get('justification', [])
                })


# ============================================================================
# APPENDIX E: End-to-End Workflow Example
# ============================================================================

def complete_workflow_example():
    """
    Demonstrates complete workflow from user query to COREP output
    """
    
    print("="*80)
    print("LLM-ASSISTED COREP REPORTING - COMPLETE WORKFLOW EXAMPLE")
    print("="*80)
    
    # Step 1: User Input
    print("\n[STEP 1: USER INPUT]")
    user_question = "We have £50M retained earnings and £20M share premium. Where do these go in C 01.00?"
    
    scenario = {
        "retained_earnings": 50000000,
        "share_premium": 20000000,
        "currency": "GBP"
    }
    
    print(f"Question: {user_question}")
    print(f"Scenario: {json.dumps(scenario, indent=2)}")
    
    # Step 2: RAG Retrieval
    print("\n[STEP 2: REGULATORY TEXT RETRIEVAL]")
    print("Retrieving relevant PRA Rulebook passages...")
    print("✓ Retrieved Article 26 (CET1 components)")
    print("✓ Retrieved COREP C 01.00 instructions")
    
    # Step 3: LLM Output (simulated)
    print("\n[STEP 3: LLM STRUCTURED OUTPUT]")
    llm_output = {
        "template": "C01.00",
        "reporting_date": "2025-12-31",
        "currency": "GBP",
        "fields": {
            "share_premium": {
                "row": "040",
                "column": "010",
                "value": 20000000,
                "justification": [
                    "PRA Rulebook – Own Funds, Article 26(1)(b): Share premium accounts related to CET1 instruments",
                    "COREP C01.00 Instructions – Row 040: Share premium"
                ],
                "confidence": "high"
            },
            "retained_earnings": {
                "row": "050",
                "column": "010",
                "value": 50000000,
                "justification": [
                    "PRA Rulebook – Own Funds, Article 26(1)(c): Retained earnings",
                    "COREP C01.00 Instructions – Row 050"
                ],
                "confidence": "medium",
                "notes": "Verify these are post-audit retained earnings per COREP instructions"
            }
        }
    }
    
    print(json.dumps(llm_output, indent=2))
    
    # Step 4: Validation
    print("\n[STEP 4: VALIDATION]")
    validator = COREPValidator()
    validation_result = validator.validate_c0100(llm_output)
    
    print(f"Status: {validation_result['validation_status']}")
    print(f"Errors: {len(validation_result['errors'])}")
    print(f"Warnings: {len(validation_result['warnings'])}")
    
    if validation_result['warnings']:
        print("\nWarnings:")
        for warning in validation_result['warnings']:
            print(f"  - {warning['message']}")
    
    # Step 5: Output Generation
    print("\n[STEP 5: HUMAN-READABLE OUTPUT]")
    print("\n" + "="*80)
    print("COREP C 01.00 – Own Funds (Extract)")
    print("Reporting Date: 2025-12-31")
    print("="*80)
    
    print(f"\n{'Row':<6} {'Description':<35} {'Amount (£M)':<15} {'Reference'}")
    print("-"*80)
    
    for field_name, field_data in llm_output['fields'].items():
        row = field_data['row']
        desc = field_name.replace('_', ' ').title()
        amount = field_data['value'] / 1_000_000
        ref = field_data['justification'][0].split(':')[0] if field_data['justification'] else "N/A"
        
        print(f"{row:<6} {desc:<35} {amount:>15.1f} {ref}")
    
    print("\n" + "="*80)
    print("ANALYST REVIEW REQUIRED:")
    print("  ✓ Verify retained earnings are post-final audit")
    print("  ✓ Confirm share premium instruments meet CRR Article 28 criteria")
    print("="*80)


if __name__ == "__main__":
    complete_workflow_example()
