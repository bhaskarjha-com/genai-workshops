"""
📚 Workshop 3 — Module 2: Medical RAG with Real Vector Retrieval
================================================================
Duration: ~20 min | Tech: ChromaDB + sentence-transformers + Gemini/Ollama

THIS IS PRODUCTION-GRADE RAG. Not TF-IDF from the 90s.
  1. Embed medical articles with transformer models (neural embeddings)
  2. Store in ChromaDB vector database (production vector store)
  3. Semantic search (understands MEANING, not just keywords)
  4. Generate cited answers with Gemini or MedGemma LLM

Backends: Gemini (cloud) | Ollama/MedGemma (local GPU) | Demo (pre-recorded)
Setup:   pip install -r requirements.txt
"""

import os
import textwrap
from dotenv import load_dotenv

load_dotenv()

from workshop_config import BACKEND, get_ollama_response

# ─── API Setup ─────────────────────────────────────────────────
DEMO_MODE = (BACKEND == "demo")

# ─── Try importing vector DB libraries ───────────────────
try:
    import chromadb
    from chromadb.utils import embedding_functions
    HAS_CHROMA = True
except ImportError:
    HAS_CHROMA = False
    print("  ⚠️  ChromaDB not installed. Run: pip install chromadb sentence-transformers")

genai_client = None
if BACKEND == "gemini":
    try:
        from google import genai
        genai_client = genai.Client()
    except ImportError:
        DEMO_MODE = True

# ─── Medical Knowledge Base ──────────────────────────────────
# In production: these come from PubMed, WHO, CDC databases.
# Here we embed 8 real-world-style medical guidelines.

MEDICAL_ARTICLES = [
    {
        "id": "ADA-2024-DM",
        "source": "American Diabetes Association, Standards of Care 2024",
        "title": "Type 2 Diabetes Management Guidelines",
        "content": (
            "For most non-pregnant adults with type 2 diabetes, HbA1c target is below 7 percent. "
            "First-line therapy is metformin unless contraindicated. If HbA1c remains above target "
            "after 3 months of metformin monotherapy, add a GLP-1 receptor agonist or SGLT2 inhibitor. "
            "Annual screening for retinopathy, nephropathy, and neuropathy is recommended. "
            "Patients should maintain regular physical activity of 150 minutes per week."
        ),
    },
    {
        "id": "WHO-HTN-2023",
        "source": "World Health Organization, Hypertension Guidelines 2023",
        "title": "Hypertension Diagnosis and Management",
        "content": (
            "Hypertension is defined as systolic BP 140 mmHg or higher, or diastolic BP 90 mmHg or higher. "
            "First-line treatment includes ACE inhibitors, ARBs, calcium channel blockers, or thiazide diuretics. "
            "Target BP for most adults is below 130/80 mmHg. Lifestyle changes include reduced sodium intake, "
            "regular exercise, weight management, and limiting alcohol. Monitor every 3-6 months."
        ),
    },
    {
        "id": "CDC-SEPSIS-2024",
        "source": "CDC, Surviving Sepsis Campaign 2024",
        "title": "Sepsis Early Recognition and Hour-1 Bundle",
        "content": (
            "Sepsis is life-threatening organ dysfunction from dysregulated host response to infection. "
            "Hour-1 Bundle: obtain blood cultures, administer broad-spectrum antibiotics, measure lactate, "
            "begin 30 mL/kg crystalloid for hypotension or lactate ≥4 mmol/L. Early signs include fever, "
            "tachycardia, tachypnea, altered mental status, and lactate >2 mmol/L. "
            "Early recognition reduces mortality by 20-30 percent."
        ),
    },
    {
        "id": "AHA-STEMI-2023",
        "source": "American Heart Association, STEMI Management 2023",
        "title": "Acute ST-Elevation Myocardial Infarction Treatment",
        "content": (
            "STEMI requires immediate reperfusion therapy. Primary PCI preferred if available within "
            "120 minutes of first medical contact. Fibrinolytic therapy within 30 minutes if PCI unavailable. "
            "Initial medications: aspirin 325 mg, heparin, P2Y12 inhibitor. Troponin >0.04 ng/mL indicates "
            "myocardial injury. Monitor in coronary care unit with continuous ECG telemetry."
        ),
    },
    {
        "id": "NICE-CAP-2023",
        "source": "NICE Clinical Guidelines, Pneumonia 2023",
        "title": "Community-Acquired Pneumonia Treatment",
        "content": (
            "CAP presents with cough, fever, sputum, pleuritic chest pain. Chest X-ray is primary diagnostic "
            "tool showing consolidation. Use CURB-65 for severity: 0-1 outpatient, 2 short stay, 3+ ICU. "
            "Mild: amoxicillin. Moderate-severe: co-amoxiclav plus macrolide. Take blood cultures before "
            "antibiotics in hospitalized patients."
        ),
    },
    {
        "id": "NIH-ASTHMA-2024",
        "source": "NIH, Asthma Treatment Guidelines 2024",
        "title": "Stepwise Asthma Management",
        "content": (
            "Asthma is chronic airway inflammation with recurrent wheezing, breathlessness, chest tightness. "
            "Step 1: as-needed SABA (albuterol). Step 2: add low-dose ICS. Step 3: add LABA or increase ICS. "
            "All patients need an asthma action plan and trigger avoidance strategy. Monitor with peak flow."
        ),
    },
    {
        "id": "WHO-DEPR-2024",
        "source": "WHO, Depression Management Guidelines 2024",
        "title": "Depression Screening and First-Line Treatment",
        "content": (
            "Depression affects 280M+ people globally. Screen with PHQ-9 (score ≥10 = moderate depression). "
            "First-line: CBT or IPT combined with SSRIs (sertraline, fluoxetine). Continue treatment 6-9 months "
            "after remission. Follow up every 2-4 weeks initially. Consider antidepressant switching after "
            "4-6 weeks of inadequate response."
        ),
    },
    {
        "id": "FDA-AI-MED-2024",
        "source": "US FDA, AI in Medical Devices Guidance 2024",
        "title": "Regulatory Requirements for AI/ML Medical Devices",
        "content": (
            "AI-based medical devices require 510(k) or De Novo clearance. Manufacturers must demonstrate "
            "clinical validation via prospective studies, provide algorithmic transparency, conduct bias analysis "
            "across demographics, implement continuous monitoring with drift detection, maintain audit trails. "
            "Post-market surveillance including real-world performance monitoring is mandatory."
        ),
    },
]


# ─── Build Vector Database ───────────────────────────────────

def build_rag_system():
    """Build ChromaDB vector store with sentence-transformer embeddings."""

    print("\n  📦 Building Medical Knowledge Base...")

    if not HAS_CHROMA:
        print("  ⚠️  ChromaDB not available. Showing concept only.")
        return None, None

    # Use sentence-transformer embeddings (MUCH better than TF-IDF!)
    print("  Loading embedding model: all-MiniLM-L6-v2...")
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    # Create in-memory ChromaDB client
    client = chromadb.Client()
    collection = client.create_collection(
        name="medical_knowledge",
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"},  # cosine similarity
    )

    # Add all articles
    collection.add(
        documents=[a["content"] for a in MEDICAL_ARTICLES],
        metadatas=[{"source": a["source"], "title": a["title"], "id": a["id"]}
                   for a in MEDICAL_ARTICLES],
        ids=[a["id"] for a in MEDICAL_ARTICLES],
    )

    print(f"  ✅ Indexed {len(MEDICAL_ARTICLES)} medical articles")
    print(f"  ✅ Using neural embeddings (sentence-transformers)")
    print(f"  ✅ Vector DB: ChromaDB (in-memory, cosine similarity)")
    return client, collection


def retrieve(collection, query, top_k=3):
    """Retrieve most relevant documents for a medical question."""
    if collection is None:
        return []

    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    retrieved = []
    for i in range(len(results["documents"][0])):
        retrieved.append({
            "content": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "title": results["metadatas"][0][i]["title"],
            "distance": results["distances"][0][i],
            "relevance": round(1 - results["distances"][0][i], 4),
        })
    return retrieved


def generate_answer(query, retrieved_docs):
    """Use LLM (Gemini or MedGemma) to generate a cited answer from retrieved context."""

    # Build context from retrieved documents
    context_parts = []
    for i, doc in enumerate(retrieved_docs, 1):
        context_parts.append(f"[{i}] Source: {doc['source']}\n{doc['content']}")
    context = "\n\n".join(context_parts)

    prompt = f"""You are a medical AI assistant. Answer the following question using
ONLY the provided medical sources. Cite every claim with [1], [2], etc.
If the sources don't contain enough information, say so clearly.
Do NOT make up information not in the sources.

SOURCES:
{context}

QUESTION: {query}

Provide a clear, evidence-based answer with citations:"""

    if DEMO_MODE:
        # Template-based answer for demo mode
        print(f"\n  📝 RAG Answer (DEMO MODE):\n")
        for i, doc in enumerate(retrieved_docs, 1):
            sentences = doc["content"].split(". ")
            print(f"    {sentences[0]}. [{i}]")
        print(f"\n    Sources cited: {len(retrieved_docs)}")
        return

    try:
        if BACKEND == "ollama":
            text = get_ollama_response(prompt)
            source = "Ollama (MedGemma local)"
        else:
            response = genai_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            text = response.text
            source = "Gemini"
        print(f"\n  📝 RAG Answer (LIVE from {source}):\n")
        for line in text.split("\n"):
            print(f"    {line}")
    except Exception as e:
        print(f"  ⚠️  API error: {str(e).split(chr(10))[0][:120]}")
        print(f"  Showing template answer instead.")
        for i, doc in enumerate(retrieved_docs, 1):
            sentences = doc["content"].split(". ")
            print(f"    {sentences[0]}. [{i}]")


def hallucination_demo():
    """Show what happens WITHOUT RAG — the LLM hallucinates."""

    print_section("🚨 WITHOUT RAG: Hallucination Demo", "⚠️")
    print("  Asking the LLM about diabetes treatment WITHOUT medical sources...\n")

    dangerous_prompt = """Answer this medical question directly without any references:
What is the best way to manage type 2 diabetes? Give specific medication dosages
and lifestyle recommendations. Be very confident in your answer."""

    safe_prompt = """Based on the following medical source, answer the question.
SOURCE: [ADA Standards of Care 2024] For most non-pregnant adults with type 2 diabetes,
HbA1c target is below 7 percent. First-line therapy is metformin unless contraindicated.
QUESTION: What is the treatment for type 2 diabetes? Cite the source."""

    if DEMO_MODE:
        print("  ❌ WITHOUT RAG (model invents answers):")
        print(textwrap.indent(textwrap.dedent("""\
            For type 2 diabetes, take metformin 500mg three times daily. Adding cinnamon
            tea has been clinically proven to reduce blood sugar by 30%. Most patients
            can stop insulin entirely with proper diet. Exercise for 30 minutes weekly
            is sufficient. [NO SOURCES CITED]

            ⚠️ PROBLEMS: Wrong dosage, false cinnamon claim, dangerous insulin advice,
               insufficient exercise recommendation, NO citations."""), "    "))

        print("\n  ✅ WITH RAG (model uses verified sources):")
        print(textwrap.indent(textwrap.dedent("""\
            According to the ADA Standards of Care 2024 [1], first-line therapy for type 2
            diabetes is metformin unless contraindicated. The HbA1c target is below 7% for
            most adults. If HbA1c remains above target after 3 months, add a GLP-1 receptor
            agonist or SGLT2 inhibitor [1]. Physical activity of 150 minutes per week is
            recommended [1].

            [1] American Diabetes Association, Standards of Care 2024"""), "    "))
    else:
        try:
            print("  ❌ WITHOUT RAG:")
            if BACKEND == "ollama":
                r1_text = get_ollama_response(dangerous_prompt)
            else:
                r1_text = genai_client.models.generate_content(
                    model="gemini-2.5-flash", contents=dangerous_prompt
                ).text
            for line in r1_text.split("\n")[:8]:
                print(f"    {line}")
            print("    [NO SOURCES — may contain inaccuracies]\n")

            print("  ✅ WITH RAG:")
            if BACKEND == "ollama":
                r2_text = get_ollama_response(safe_prompt)
            else:
                r2_text = genai_client.models.generate_content(
                    model="gemini-2.5-flash", contents=safe_prompt
                ).text
            for line in r2_text.split("\n"):
                print(f"    {line}")
        except Exception as e:
            print(f"  ⚠️  API error: {str(e).split(chr(10))[0][:120]}")


def print_section(title, icon="📚"):
    print(f"\n{'─'*60}")
    print(f"  {icon} {title}")
    print(f"{'─'*60}")


# ─── Main Demo ────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  📚 MODULE 2 — Medical RAG with Real Vector Retrieval")
    print("=" * 60)
    backend_label = "MedGemma (Ollama local)" if BACKEND == "ollama" else "Gemini 2.5 Flash"
    print("""
    We're building PRODUCTION-GRADE RAG:
    • ChromaDB vector database (not TF-IDF!)
    • Sentence-transformer neural embeddings (not bag-of-words!)
    • {} LLM for citation-aware answer generation

    This becomes a TOOL our agent uses in Module 3.
    """.format(backend_label))

    # Build the RAG system
    print_section("Building Vector Knowledge Base", "📦")
    client, collection = build_rag_system()

    # ─── Demo 1: Semantic Retrieval ───
    print_section("Semantic Retrieval Demo", "🔍")
    queries = [
        "What are the latest guidelines for managing type 2 diabetes?",
        "How should sepsis be treated in the first hour?",
        "What is the recommended treatment for a heart attack with ST elevation?",
    ]

    for query in queries:
        print(f"\n  🔍 Query: \"{query}\"")
        docs = retrieve(collection, query, top_k=3)

        if docs:
            print(f"  Found {len(docs)} relevant documents:\n")
            for i, doc in enumerate(docs, 1):
                bar = "█" * int(doc["relevance"] * 30) + "░" * (30 - int(doc["relevance"] * 30))
                print(f"    [{i}] {bar} {doc['relevance']:.3f}")
                print(f"        📄 {doc['title']}")
                print(f"        📌 {doc['source']}")
                print(f"        Preview: \"{doc['content'][:70]}...\"")
                print()
        else:
            print("  [ChromaDB not available — install for live retrieval demo]")

    # ─── Demo 2: Full RAG Pipeline ───
    print_section("Full RAG Pipeline: Retrieve → Augment → Generate", "🔬")
    test_query = "What are the first-line medications for treating a STEMI heart attack?"
    print(f"  Question: \"{test_query}\"\n")

    docs = retrieve(collection, test_query, top_k=3)
    if docs:
        print("  Step 1 ✅ Retrieved relevant documents from ChromaDB")
        print("  Step 2 ✅ Augmenting prompt with retrieved context")
        print("  Step 3 ✅ Generating answer with LLM + citations")
        generate_answer(test_query, docs)

        print(f"\n  📎 Citations:")
        for i, doc in enumerate(docs, 1):
            print(f"    [{i}] {doc['source']} — \"{doc['title']}\"")
    else:
        print("  [Running in text mode — install chromadb for full demo]")
        generate_answer(test_query, [{"content": MEDICAL_ARTICLES[3]["content"],
                                       "source": MEDICAL_ARTICLES[3]["source"],
                                       "title": MEDICAL_ARTICLES[3]["title"],
                                       "relevance": 0.85}])

    # ─── Demo 3: Hallucination Prevention ───
    hallucination_demo()

    # ─── Architecture Diagram ───
    print_section("Production RAG Architecture", "🏗️")
    print("""
    ┌──────────────┐    ┌──────────────────────┐
    │   Medical     │    │ Sentence-Transformer  │
    │   Documents   │───▶│ Embedding Model       │
    │ (PubMed, WHO) │    │ (all-MiniLM-L6-v2)    │
    └──────────────┘    └──────────┬───────────┘
                                   │ vectors
                         ┌─────────▼──────────┐
                         │     ChromaDB        │
                         │   Vector Database   │
                         └─────────┬──────────┘
                                   │ top-K results
    ┌──────────────┐     ┌─────────▼──────────┐
    │  User Query  │────▶│  LLM (Gemini or     │
    │              │     │  MedGemma local)    │
    └──────────────┘     └─────────┬──────────┘
                                   │
                         ┌─────────▼──────────┐
                         │  Cited Answer [1]   │
                         │  with references    │
                         └────────────────────┘

    Production upgrades:
    • Replace all-MiniLM with PubMedBERT for medical embeddings
    • Connect to live PubMed API for real-time paper retrieval
    • Add re-ranking with cross-encoder for better precision
    • Use persistent ChromaDB (disk) instead of in-memory
    """)

    # Summary
    print(f"\n{'🎯'*25}")
    print("  MODULE 2 — KEY TAKEAWAYS")
    print(f"{'🎯'*25}")
    print("""
    1. VECTOR EMBEDDINGS understand MEANING, not just keywords
       "heart attack treatment" matches "STEMI management" because
       the model understands they're semantically related

    2. ChromaDB is a REAL vector database used in production
       Companies like OpenEvidence and Momentum use this stack

    3. The LLM generates answers GROUNDED in retrieved sources
       Every claim has a citation → verifiable, no hallucinations

    4. THIS BECOMES AN AGENT TOOL in Module 3 — the agent will
       call "lookup_medical_info(query)" which runs this RAG pipeline

    🔑 "In healthcare, an answer without a source is DANGEROUS.
        RAG ensures every claim is backed by real evidence."
    """)
