# LLM-Assisted PRA COREP Reporting Assistant
## Internship Assignment Submission Package

**Candidate:** Mukesh Kumar  
**Institution:** IIT Delhi  
**Role:** Internship (Regulatory / Data / AI)  
**Date:** February 2026

---

## 📦 Submission Contents

This package contains a complete prototype proposal for an LLM-assisted regulatory reporting system:

### 1. **Main Document** 
`LLM_COREP_Reporting_Assistant_Internship_Assignment.docx`
- Comprehensive 25+ page proposal covering:
  - Problem statement and opportunity
  - System architecture and technical design
  - Implementation roadmap (12-week internship plan)
  - Risk mitigation and governance framework
  - Expected ROI and value proposition
  - Limitations and future enhancements

### 2. **Visual Architecture**
`System_Architecture_Diagram.html`
- Interactive system architecture diagram
- 6-layer modular design visualization
- Data flow examples
- Key features and security highlights
- Open in any web browser for best viewing experience

### 3. **Technical Implementation**
`Technical_Appendix_Implementation_Examples.py`
- Working code examples demonstrating:
  - JSON schema for COREP C 01.00
  - RAG (Retrieval-Augmented Generation) implementation
  - LLM prompt engineering patterns
  - Validation rules engine
  - Complete end-to-end workflow
- Fully executable Python code with detailed comments

---

## 🎯 Key Highlights

### Problem Addressed
UK banks face significant challenges in preparing PRA COREP returns:
- Manual interpretation of 100+ pages of regulatory text
- Inconsistent application across analysts and periods
- High risk of omissions and misclassifications
- Limited audit traceability

### Proposed Solution
An LLM-powered decision-support assistant that:
- ✅ Reduces regulatory research time by ~40%
- ✅ Provides schema-constrained outputs (prevents hallucination)
- ✅ Generates audit trails with regulatory citations
- ✅ Maintains human oversight for final decisions
- ✅ Supports regulatory examination readiness

### Why This Approach Works
1. **Scoped Appropriately**: Focus on 2 templates (C 01.00, C 02.00) rather than attempting full automation
2. **Regulatory Safety**: Human-in-the-loop validation, confidence scoring, escalation processes
3. **Auditability**: Every field traceable to source regulations
4. **Realistic Timeline**: 12-week implementation plan suitable for internship project

---

## 🏗️ System Architecture Overview

```
User Question + Scenario
        ↓
Regulatory Text Retrieval (RAG)
        ↓
LLM Structured Reasoning
        ↓
Schema Validation
        ↓
COREP Template Population
        ↓
Business Rule Validation
        ↓
Output: Template Extract + Audit Log
```

**Key Components:**
- **RAG Layer**: Semantic search over PRA Rulebook, EBA instructions, CRR articles
- **LLM Engine**: Schema-constrained output generation (prevents hallucination)
- **Validation**: Mandatory fields, arithmetic consistency, value ranges
- **Audit Trail**: Regulatory justifications, confidence scores, version tracking

---

## 📊 Expected Value

### Time Savings
- **Regulatory Research**: 40% reduction (8 hours → 5 hours per submission)
- **Template Mapping**: 30% faster scenario-to-COREP mapping
- **Audit Prep**: Eliminate manual citation lookup

### Quality Improvements
- **Consistency**: Standardized regulatory interpretations
- **Completeness**: Automated checks for missing mandatory fields
- **Traceability**: Clear audit trails for examiners

### Estimated ROI (2-template scope)
- Annual time savings: £7,200+
- Avoided rework costs: £10,000-£50,000/year
- **Total benefit: £17,000-£57,000 annually** (scales with additional templates)

---

## 🔒 Risk Mitigation

### Model Risk Controls
- ✅ Human-in-the-loop validation (no automated submissions)
- ✅ Confidence scoring (medium/low triggers mandatory review)
- ✅ Quarterly LLM audits against manual submissions
- ✅ Dual control for high-materiality fields

### Data Security
- ✅ On-premises deployment (no external API calls)
- ✅ Role-based access controls
- ✅ 7-year audit log retention (PRA compliance)

### Escalation Process
- Ambiguous scenarios → Manual expert review
- Conflicting guidance → Present multiple interpretations
- Complex cases → Escalate to compliance/legal team

---

## 🗓️ Implementation Roadmap (12 Weeks)

| Phase | Duration | Key Deliverables |
|-------|----------|------------------|
| **Research & Data Collection** | Weeks 1-2 | Regulatory text corpus, analyst workflow analysis |
| **RAG Setup** | Weeks 3-4 | Vector database, embedding pipeline, retrieval testing |
| **LLM Integration** | Weeks 5-7 | Schema development, prompt engineering, validation layer |
| **UI Development** | Weeks 8-9 | Web interface, template rendering, audit exports |
| **Testing & Validation** | Weeks 10-11 | Blind testing vs. historical submissions, red-teaming |
| **Documentation** | Week 12 | Technical docs, user manual, final presentation |

---

## 🚀 Future Enhancements

**Phase 2:** Expand to C 04.00-C 09.00 (Credit/Market/Operational Risk)  
**Phase 3:** XBRL validation integration  
**Phase 4:** Automated regulatory update monitoring  
**Phase 5:** Data integration with GL and risk systems  
**Phase 6:** Multi-jurisdiction support (ECB FINREP, Fed FR Y-9C)

---

## 💡 Technical Innovation

This proposal demonstrates:
1. **Practical AI Application**: Solving real regulatory pain points
2. **Risk-Aware Design**: Appropriate guardrails for high-stakes domain
3. **Scalable Architecture**: Modular design enables future expansion
4. **Explainable AI**: Every decision traceable to regulatory sources

### Technologies Used
- **RAG**: Sentence Transformers + FAISS/ChromaDB
- **LLM**: Claude Sonnet 4 (or equivalent)
- **Validation**: Python business rules engine
- **UI**: React/Vue web interface

---

## 📝 How to Review This Submission

### For Technical Reviewers
1. **Read Main Document** for comprehensive proposal
2. **View Architecture Diagram** (open HTML in browser) for visual system design
3. **Review Python Code** for implementation feasibility

### For Business Stakeholders
1. **Main Document Sections 1-3**: Problem statement and value prop
2. **Section 9**: Expected benefits and ROI
3. **Architecture Diagram**: High-level system overview

### Suggested Review Questions
- How does this differ from generic ChatGPT for regulatory questions?
- What prevents the LLM from "hallucinating" incorrect COREP mappings?
- How is regulatory compliance maintained?
- What's the fallback if the system provides uncertain guidance?

---

## 📞 Contact

**Mukesh Kumar**  
**IIT Delhi**  
**Email:** [Your Email]  
**LinkedIn:** [Your Profile]

---

## 🙏 Acknowledgments

This proposal synthesizes best practices from:
- Regulatory technology literature (RAG for compliance)
- LLM safety research (schema constraints, confidence scoring)
- Banking industry practices (PRA/EBA guidance)

**References:**
- PRA Rulebook – Own Funds (Bank of England, 2024)
- EBA COREP Reporting Framework (2024)
- CRR (Regulation EU No 575/2013)
- Lewis et al. (2020) - "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"

---

## ⚖️ Disclaimer

This is a conceptual prototype proposal for internship evaluation purposes. Implementation would require:
- Formal model risk assessment
- Legal/compliance review
- Production-grade infrastructure
- Regulatory approval (if applicable)

The system is designed as a **decision-support tool**, not a replacement for qualified analysts. Final COREP submissions remain the responsibility of the reporting entity.

---

**Prepared with attention to:**
✓ Regulatory safety and auditability  
✓ Practical implementation feasibility  
✓ Clear business value proposition  
✓ Realistic scoping for internship timeline  

Thank you for considering this submission!
