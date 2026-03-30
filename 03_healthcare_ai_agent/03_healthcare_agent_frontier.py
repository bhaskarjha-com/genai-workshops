"""
🤖 Workshop 3 — Module 3: Healthcare AI Agent with Function Calling
===========================================================================
Duration: ~30 min (⭐ CENTERPIECE) | Tech: Gemini 2.5 Flash or MedGemma 1.5

THIS IS REAL AGENTIC AI. The LLM autonomously decides:
  - WHICH tools to call
  - In WHAT order
  - With WHAT arguments
  - And CHAINS multiple tool calls to solve complex problems

The agent ACTUALLY USES the capabilities built in Modules 1 & 2:
  → analyze_patient_xray()   = Module 1's multimodal vision
  → search_medical_knowledge() = Module 2's vector RAG pipeline

Setup: pip install google-genai chromadb sentence-transformers
       export GEMINI_API_KEY="your_key"
"""

import os
import json
import textwrap
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

from workshop_config import (
    BACKEND, OLLAMA_MODEL, OLLAMA_TOOL_MODEL,
    get_ollama_vision_response, get_ollama_response,
    run_ollama_agent, build_ollama_tool_schema,
)

# ─── API Setup ─────────────────────────────────────────────────
DEMO_MODE = (BACKEND == "demo")

client = None
if BACKEND == "gemini":
    from google import genai
    from google.genai import types
    client = genai.Client()

# ─── Try importing libraries for integrated tools ────────────
HAS_CHROMA = False
try:
    import chromadb
    from chromadb.utils import embedding_functions
    HAS_CHROMA = True
except ImportError:
    pass

HAS_PIL = False
try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    pass


# ─── Medical Knowledge Base (same as Module 2) ───────────────
# The agent uses the SAME knowledge base and RAG approach as Module 2.
# In production: this would be a shared service both modules connect to.

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
]

# ─── Build Vector Database for Agent RAG Tool ────────────────
_rag_collection = None  # Lazy-initialized

def _get_rag_collection():
    """Build or return the ChromaDB collection (same approach as Module 2)."""
    global _rag_collection
    if _rag_collection is not None:
        return _rag_collection
    if not HAS_CHROMA:
        return None
    try:
        ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        client = chromadb.Client()
        _rag_collection = client.create_collection(
            name="agent_medical_kb",
            embedding_function=ef,
            metadata={"hnsw:space": "cosine"},
        )
        _rag_collection.add(
            documents=[a["content"] for a in MEDICAL_ARTICLES],
            metadatas=[{"source": a["source"], "title": a["title"]} for a in MEDICAL_ARTICLES],
            ids=[a["id"] for a in MEDICAL_ARTICLES],
        )
        return _rag_collection
    except Exception:
        return None


# ─── Simulated Hospital State ────────────────────────────────
# In production, these tools would call real hospital APIs/databases.

HOSPITAL_DB = {
    "beds": {
        "ICU-01": {"patient_id": "P-101", "name": "Ramesh K.",  "severity": 7, "days": 3, "condition": "Post-CABG recovery"},
        "ICU-02": {"patient_id": "P-102", "name": "Priya S.",   "severity": 9, "days": 1, "condition": "Septic shock"},
        "ICU-03": {"patient_id": "P-103", "name": "Amit D.",    "severity": 3, "days": 5, "condition": "Pneumonia (stable, recovering)"},
        "ICU-04": {"patient_id": "P-104", "name": "Sunita M.",  "severity": 8, "days": 2, "condition": "Acute MI"},
        "ICU-05": {"patient_id": "P-105", "name": "Vikram R.",  "severity": 3, "days": 7, "condition": "Post-surgery (ready for step-down)"},
        "ICU-06": {"patient_id": "P-106", "name": "Anita P.",   "severity": 6, "days": 4, "condition": "Respiratory failure"},
        "ICU-07": None,  # EMPTY
        "ICU-08": {"patient_id": "P-108", "name": "Rajesh G.",  "severity": 5, "days": 6, "condition": "Diabetic ketoacidosis"},
    },
    "incoming": {
        "P-201": {"name": "Meera T.", "age": 62, "sex": "Female", "severity": 9,
                  "condition": "STEMI — ST elevation in leads II, III, aVF",
                  "vitals": {"bp": "85/55", "hr": 120, "spo2": 89, "temp": 37.2, "rr": 28},
                  "labs": {"troponin": 0.15, "lactate": 1.8, "wbc": 11000},
                  "has_xray": True},
        "P-202": {"name": "Arjun B.", "age": 45, "sex": "Male", "severity": 7,
                  "condition": "Severe community-acquired pneumonia with hypoxia",
                  "vitals": {"bp": "110/70", "hr": 105, "spo2": 88, "temp": 39.1, "rr": 24},
                  "labs": {"troponin": 0.01, "lactate": 2.5, "wbc": 18000},
                  "has_xray": True},
    },
}


# ══════════════════════════════════════════════════════════════
# TOOL DEFINITIONS — These are the functions the agent can call
# ══════════════════════════════════════════════════════════════
# Gemini reads the function names, docstrings, and type hints
# to understand what each tool does and when to use it.

def check_bed_availability() -> dict:
    """Check current ICU bed availability. Returns total beds, how many are occupied,
    and the list of available (empty) bed IDs."""
    occupied = {k: v for k, v in HOSPITAL_DB["beds"].items() if v is not None}
    empty = [k for k, v in HOSPITAL_DB["beds"].items() if v is None]
    return {
        "total_beds": len(HOSPITAL_DB["beds"]),
        "occupied": len(occupied),
        "available": len(empty),
        "empty_bed_ids": empty,
        "status": "CRITICAL" if len(empty) <= 1 else "OK",
    }


def get_patient_info(patient_id: str) -> dict:
    """Get detailed information about an incoming patient including their vitals,
    lab results, and condition. Use this to understand a patient's medical status."""
    if patient_id in HOSPITAL_DB["incoming"]:
        return HOSPITAL_DB["incoming"][patient_id]
    # Check current ICU patients
    for bed_id, info in HOSPITAL_DB["beds"].items():
        if info and info.get("patient_id") == patient_id:
            return {"name": info["name"], "severity": info["severity"],
                    "days_in_icu": info["days"], "condition": info["condition"],
                    "bed": bed_id}
    return {"error": f"Patient {patient_id} not found in system"}


def analyze_patient_xray(patient_id: str) -> dict:
    """Analyze a patient's chest X-ray using multimodal AI (same approach as Module 1).
    Sends the X-ray image to the vision model for radiological analysis.
    Use this when a patient has imaging data that needs interpretation."""

    # Check if patient exists and has X-ray
    patient = HOSPITAL_DB["incoming"].get(patient_id)
    if not patient:
        return {"error": f"Patient {patient_id} not found"}
    if not patient.get("has_xray"):
        return {"error": f"No X-ray on file for {patient['name']}"}

    # In DEMO_MODE or if dependencies missing, return pre-recorded analysis
    if DEMO_MODE or not HAS_PIL:
        return {
            "patient": patient["name"],
            "modality": "Chest X-ray (AP view)",
            "analysis": (
                "Findings: (1) Cardiomegaly — cardiac silhouette enlarged (CTR > 0.5). "
                "(2) Right lower lobe opacity suggesting consolidation or atelectasis. "
                "(3) Right costophrenic angle blunting — possible small pleural effusion. "
                "(4) No pneumothorax. (5) No acute fractures."
            ),
            "impression": "Cardiomegaly with right lower lobe consolidation and possible small right pleural effusion.",
            "confidence": "Moderate — clinical correlation recommended",
            "method": "Gemini 2.5 Flash multimodal analysis (DEMO — pre-recorded)",
        }

    # LIVE: Load X-ray image and send to multimodal model
    try:
        xray_paths = [
            Path(__file__).parent / "sample_chest_xray.png",
            Path("sample_chest_xray.png"),
        ]
        img_bytes = None
        for p in xray_paths:
            if p.exists():
                with open(str(p), "rb") as f:
                    img_bytes = f.read()
                break

        if img_bytes is None:
            return {
                "patient": patient["name"],
                "error": "X-ray image file not found on disk",
                "fallback": "Request radiology department to upload image to PACS",
            }

        xray_prompt = (
            f"You are a radiologist AI. Analyze this chest X-ray for patient "
            f"{patient['name']} ({patient['age']}y {patient['sex']}), "
            f"presenting with: {patient['condition']}. "
            f"Provide systematic findings and clinical impression."
        )

        if BACKEND == "ollama":
            analysis_text = get_ollama_vision_response(xray_prompt, img_bytes)
            method = "MedGemma 1.5 multimodal analysis (Ollama local)"
        else:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Part.from_bytes(data=img_bytes, mime_type="image/png"),
                    xray_prompt,
                ],
            )
            analysis_text = response.text
            method = "Gemini 2.5 Flash multimodal analysis (LIVE)"

        return {
            "patient": patient["name"],
            "modality": "Chest X-ray (AP view)",
            "analysis": analysis_text,
            "method": method,
        }
    except Exception as e:
        return {"patient": patient["name"], "error": f"Multimodal analysis failed: {e}"}


def search_medical_knowledge(query: str) -> dict:
    """Search the medical knowledge base using vector RAG (same approach as Module 2).
    Uses semantic embeddings to find the most relevant treatment guidelines,
    protocols, and evidence-based recommendations for a medical condition or question.
    Returns cited sources from authoritative medical organizations."""

    # Try real ChromaDB vector retrieval first (Module 2's approach)
    collection = _get_rag_collection()
    if collection is not None:
        try:
            results = collection.query(
                query_texts=[query],
                n_results=3,
                include=["documents", "metadatas", "distances"],
            )
            retrieved = []
            for i in range(len(results["documents"][0])):
                relevance = round(1 - results["distances"][0][i], 4)
                retrieved.append({
                    "source": results["metadatas"][0][i]["source"],
                    "title": results["metadatas"][0][i]["title"],
                    "content": results["documents"][0][i],
                    "relevance_score": relevance,
                })
            return {
                "query": query,
                "method": "Vector RAG — ChromaDB + sentence-transformers (LIVE)",
                "results_found": len(retrieved),
                "top_results": retrieved,
            }
        except Exception:
            pass  # Fall through to keyword fallback

    # Fallback: keyword-based retrieval (if ChromaDB unavailable)
    fallback_guidelines = {
        "stemi": {
            "source": "AHA STEMI Management Guidelines 2023",
            "title": "Acute ST-Elevation Myocardial Infarction Treatment",
            "content": (
                "STEMI requires immediate reperfusion therapy. Primary PCI preferred if available "
                "within 120 minutes of first medical contact. Fibrinolytic therapy within 30 minutes "
                "if PCI unavailable. Initial medications: aspirin 325 mg, heparin, P2Y12 inhibitor. "
                "Troponin >0.04 ng/mL indicates myocardial injury. Monitor in CCU with continuous ECG."
            ),
            "relevance_score": 0.95,
        },
        "pneumonia": {
            "source": "NICE Community-Acquired Pneumonia Guidelines 2023",
            "title": "Community-Acquired Pneumonia Treatment",
            "content": (
                "CURB-65 scoring for severity. 0-1: outpatient. 2: short stay. 3+: ICU. "
                "Mild: amoxicillin. Moderate-severe: co-amoxiclav + macrolide. "
                "Blood cultures before antibiotics."
            ),
            "relevance_score": 0.92,
        },
        "sepsis": {
            "source": "Surviving Sepsis Campaign 2024",
            "title": "Sepsis Early Recognition and Hour-1 Bundle",
            "content": (
                "Hour-1 Bundle: blood cultures, broad-spectrum antibiotics, lactate measurement, "
                "30 mL/kg crystalloid for hypotension. Monitor for organ dysfunction. "
                "Every hour of delay increases mortality 7%."
            ),
            "relevance_score": 0.93,
        },
    }

    # Match by keyword
    for key, guide in fallback_guidelines.items():
        if key in query.lower():
            return {
                "query": query,
                "method": "Keyword fallback (ChromaDB not available — install for vector RAG)",
                "results_found": 1,
                "top_results": [guide],
            }

    return {
        "query": query,
        "method": "Keyword fallback",
        "results_found": 0,
        "top_results": [],
        "note": "No matching guidelines found. Recommend specialist consultation.",
    }


def assess_discharge_readiness(bed_id: str) -> dict:
    """Evaluate whether a current ICU patient is ready for step-down or discharge.
    Checks severity score, length of stay, and condition stability."""
    info = HOSPITAL_DB["beds"].get(bed_id)
    if info is None:
        return {"bed_id": bed_id, "status": "EMPTY — no patient in this bed"}
    ready = info["severity"] <= 4 and info["days"] >= 3
    return {
        "bed_id": bed_id,
        "patient": info["name"],
        "severity": info["severity"],
        "days_in_icu": info["days"],
        "condition": info["condition"],
        "ready_for_stepdown": ready,
        "recommendation": "Ready for step-down unit" if ready else
                          f"Continue ICU care — severity {info['severity']}/10",
    }


def assign_patient_to_bed(patient_id: str, bed_id: str, reason: str) -> dict:
    """Assign an incoming patient to an ICU bed. This is a CRITICAL action that
    REQUIRES physician approval before execution. Always provide the clinical
    reasoning for the assignment."""
    patient = HOSPITAL_DB["incoming"].get(patient_id)
    bed = HOSPITAL_DB["beds"].get(bed_id)
    if not patient:
        return {"success": False, "error": f"Patient {patient_id} not found"}
    if bed is not None:
        return {"success": False, "error": f"Bed {bed_id} is occupied"}
    return {
        "success": True,
        "status": "PENDING_PHYSICIAN_APPROVAL",
        "assignment": f"{patient['name']} → {bed_id}",
        "reason": reason,
        "message": f"⚠️ Assignment of {patient['name']} to {bed_id} requires "
                   f"attending physician approval before execution.",
    }


def send_alert(message: str, urgency: str = "NORMAL", target_team: str = "ICU_TEAM", **kwargs) -> dict:
    """Send an alert notification to hospital staff. Use for notifying care teams
    about incoming patients, bed assignments, or emergencies."""
    from datetime import datetime
    return {
        "sent": True,
        "urgency": urgency,
        "target": target_team,
        "message": message,
        "timestamp": datetime.now().isoformat(),
    }


# All tools the agent can use
AGENT_TOOLS = [
    check_bed_availability,
    get_patient_info,
    analyze_patient_xray,          # ← Module 1's multimodal vision
    search_medical_knowledge,      # ← Module 2's vector RAG pipeline
    assess_discharge_readiness,
    assign_patient_to_bed,
    send_alert,
]


# ─── Agent Trace Printer ─────────────────────────────────────

def print_agent_trace(history):
    """Print the agent's reasoning and tool-use trace from chat history."""
    step = 0
    for msg in history:
        if msg.role == "user":
            print(f"\n  👤 USER INPUT:")
            for part in msg.parts:
                if hasattr(part, "text") and part.text:
                    for line in part.text.split("\n")[:3]:
                        print(f"      {line}")
                    if len(part.text.split("\n")) > 3:
                        print(f"      ...")
        elif msg.role == "model":
            for part in msg.parts:
                if hasattr(part, "function_call") and part.function_call:
                    step += 1
                    fc = part.function_call
                    args = dict(fc.args) if fc.args else {}
                    args_str = ", ".join(f'{k}="{v}"' for k, v in args.items())
                    print(f"\n  🤖 Step {step} — Agent calls: {fc.name}({args_str})")
                if hasattr(part, "text") and part.text:
                    print(f"\n  🤖 Agent's Final Response:")
                    for line in part.text.split("\n"):
                        print(f"      {line}")
        elif msg.role == "function":
            for part in msg.parts:
                if hasattr(part, "function_response") and part.function_response:
                    fr = part.function_response
                    result = dict(fr.response) if fr.response else {}
                    # Pretty print the result compactly
                    result_str = json.dumps(result, indent=2, default=str)
                    print(f"  📋 Tool returned ({fr.name}):")
                    for line in result_str.split("\n")[:6]:
                        print(f"      {line}")
                    if len(result_str.split("\n")) > 6:
                        print(f"      ...")


# ─── Demo: Pre-recorded trace for demo mode ──────────────────

def run_demo_mode():
    """Show pre-recorded agent trace when no API key is available."""
    print(textwrap.dedent("""
    📋 PRE-RECORDED AGENT TRACE:
    (Set GEMINI_API_KEY to see LIVE autonomous reasoning)

    👤 USER: "INCOMING EMERGENCY: Patient P-201, Meera T., 62F, presenting
       with STEMI. BP 85/55, HR 120, SpO2 89%. Needs immediate ICU admission."

    🤖 Step 1 — Agent calls: check_bed_availability()
    📋 Tool returned: {"total": 8, "occupied": 7, "available": 1,
        "empty_bed_ids": ["ICU-07"], "status": "CRITICAL"}

    🤖 Step 2 — Agent calls: get_patient_info(patient_id="P-201")
    📋 Tool returned: {"name": "Meera T.", "age": 62, "severity": 9,
        "condition": "STEMI", "vitals": {"bp": "85/55", "hr": 120, "spo2": 89}}

    🤖 Step 3 — Agent calls: analyze_patient_xray(patient_id="P-201")
       ⬆️ THIS IS MODULE 1's MULTIMODAL VISION — the agent SEES the X-ray!
    📋 Tool returned: {"analysis": "Cardiomegaly, right lower lobe opacity,
        possible pleural effusion", "impression": "Cardiomegaly with
        consolidation", "method": "Gemini 2.5 Flash multimodal"}

    🤖 Step 4 — Agent calls: search_medical_knowledge(query="STEMI treatment
        guidelines acute myocardial infarction")
       ⬆️ THIS IS MODULE 2's VECTOR RAG — the agent searches the knowledge base!
    📋 Tool returned: {"method": "Vector RAG — ChromaDB + sentence-transformers",
        "top_results": [{"source": "AHA 2023", "content": "Primary PCI within
        120 min. Aspirin 325mg + heparin...", "relevance": 0.95}]}

    🤖 Step 5 — Agent calls: assign_patient_to_bed(patient_id="P-201",
        bed_id="ICU-07", reason="Severity 9/10 STEMI requiring immediate
        PCI. Hemodynamically unstable. X-ray confirms cardiomegaly with
        pulmonary congestion. AHA guidelines mandate PCI within 120 min.")
    📋 Tool returned: {"success": true, "status": "PENDING_PHYSICIAN_APPROVAL",
        "assignment": "Meera T. → ICU-07"}

    🤖 Step 6 — Agent calls: send_alert(message="CRITICAL: STEMI patient
        Meera T. assigned to ICU-07. Activate cath lab for primary PCI.
        X-ray shows cardiomegaly + pulmonary congestion. Door-to-balloon
        < 90 min.", urgency="CRITICAL",
        target_team="Cardiology + ICU Team")
    📋 Tool returned: {"sent": true, "urgency": "CRITICAL"}

    🤖 Agent's Final Response:
        I've handled the emergency admission for Meera T. Here's my
        reasoning chain:

        1. **Checked bed availability** — Only 1 ICU bed (ICU-07) available.
           Status: CRITICAL.
        2. **Reviewed patient data** — 62F, severity 9/10, STEMI with
           hemodynamic instability (BP 85/55, SpO2 89%).
        3. **Analyzed chest X-ray** 📷 — Cardiomegaly with right lower lobe
           opacity and possible pleural effusion, consistent with acute
           cardiac decompensation.
        4. **Searched medical guidelines** 📚 — AHA 2023 mandates primary PCI
           within 120 minutes for STEMI. Initial meds: aspirin 325mg +
           heparin + P2Y12 inhibitor.
        5. **Assigned ICU bed** — ICU-07 (⚠️ PENDING physician approval).
           Reasoning integrates X-ray findings + patient severity + guidelines.
        6. **Alerted care team** — Cardiology + ICU team notified, cath lab
           activation requested.

        ⚠️ CRITICAL ACTIONS PENDING:
        - Attending physician must APPROVE bed assignment
        - Cath lab team must CONFIRM availability
        - Door-to-balloon timer started

        💡 Notice how I used BOTH the multimodal vision (X-ray analysis)
        AND the RAG knowledge base (treatment guidelines) — the same
        capabilities we built in Modules 1 and 2!
    """))


# ─── Main Demo ────────────────────────────────────────────────

def print_section(title, icon="🤖"):
    print(f"\n{'─'*60}")
    print(f"  {icon} {title}")
    print(f"{'─'*60}")


if __name__ == "__main__":
    print("=" * 60)
    backend_label = "MedGemma 1.5 (local GPU)" if BACKEND == "ollama" else "Gemini 2.5 Flash (cloud)"
    print(f"  🤖 MODULE 3 — Healthcare AI Agent ({backend_label})")
    print("  ⭐ THIS IS THE CENTERPIECE OF THE WORKSHOP")
    print("=" * 60)
    print("""
    The agent AUTONOMOUSLY decides:
    • WHICH tools to call    (check beds? analyze X-ray? search guidelines?)
    • In WHAT order          (check beds first, then patient info, then...)
    • With WHAT arguments    (patient_id="P-201", query="STEMI treatment")
    • How to CHAIN them      (if no beds → find step-down candidates)

    KEY: This agent uses the SAME capabilities from Modules 1 & 2:
    🔬 analyze_patient_xray   → Module 1's multimodal vision
    📚 search_medical_knowledge → Module 2's vector RAG pipeline
    """)

    # ─── Show Agent Architecture ───
    print_section("Agent Architecture: LLM + Tools", "🏗️")
    print("""
    ┌───────────────────────────────────────────────────┐
    │           LLM Brain (Gemini or MedGemma)           │
    │                                                    │
    │  "I need to check beds, analyze the X-ray,         │
    │   search treatment guidelines, then assign..."     │
    │                                                    │
    │  ┌──────────────────────────────────────────┐      │
    │  │     Automatic Function Calling            │      │
    │  │     (SDK handles the loop for us)          │      │
    │  └──────────────────────────────────────────┘      │
    └─────────────────────┬─────────────────────────────┘
                          │ calls functions
    ┌─────────────────────▼─────────────────────────────┐
    │  🔧 TOOLS (Python functions)                       │
    │                                                    │
    │  check_bed_availability()   → Hospital DB          │
    │  get_patient_info(id)       → Patient records      │
    │  analyze_patient_xray(id)   → 🔬 MODULE 1 VISION   │
    │  search_medical_knowledge   → 📚 MODULE 2 RAG      │
    │  assess_discharge_readiness → Discharge model      │
    │  assign_patient_to_bed      → Bed management       │
    │  send_alert                 → Staff notification    │
    └───────────────────────────────────────────────────┘
    """)

    # ─── Show Available Tools ───
    print_section("Available Tools (7 total)", "🔧")
    for fn in AGENT_TOOLS:
        doc = fn.__doc__.split("\n")[0] if fn.__doc__ else "No description"
        # Highlight integrated tools
        tag = ""
        if fn.__name__ == "analyze_patient_xray":
            tag = " ← 🔬 Module 1"
        elif fn.__name__ == "search_medical_knowledge":
            tag = " ← 📚 Module 2"
        print(f"    🔧 {fn.__name__:<30} — {doc}{tag}")

    # ─── Show Current ICU State ───
    print_section("Current ICU Status", "🏥")
    for bed_id, info in HOSPITAL_DB["beds"].items():
        if info:
            sev = info["severity"]
            bar = "🟥" * min(sev, 10) + "⬜" * (10 - min(sev, 10))
            print(f"    {bed_id}: {info['name']:<12} Sev:{sev:>2}/10 {bar}  {info['condition']}")
        else:
            print(f"    {bed_id}: 🟩 EMPTY")

    print(f"\n  🚑 Incoming patients:")
    for pid, p in HOSPITAL_DB["incoming"].items():
        xray_tag = " 📷 X-ray available" if p.get("has_xray") else ""
        print(f"    {pid}: {p['name']} ({p['age']}{p['sex'][0]}) — Severity {p['severity']}/10 — {p['condition']}{xray_tag}")

    # ═══════════════════════════════════════════════════════════
    # SCENARIO 1: Emergency STEMI Admission
    # ═══════════════════════════════════════════════════════════
    print_section("SCENARIO 1: Emergency STEMI Admission", "🚨")

    scenario = (
        "INCOMING EMERGENCY: Patient P-201 (Meera T.), 62-year-old female, "
        "presenting with STEMI — ST elevation in leads II, III, aVF. "
        "BP 85/55, HR 120, SpO2 89%. Troponin 0.15 ng/mL. "
        "She has a chest X-ray available. She needs immediate ICU admission. "
        "Check bed availability, review her medical data, analyze her chest X-ray, "
        "search the medical knowledge base for STEMI treatment guidelines, "
        "assign an appropriate bed, and alert the care team."
    )
    print(f"  Patient scenario: {scenario[:80]}...\n")

    if DEMO_MODE:
        print("  ⚠️  Running in DEMO MODE (pre-recorded agent trace)")
        run_demo_mode()
    else:
        try:
            # Pre-build RAG collection so it's ready for the agent
            print("  📦 Building medical knowledge base (vector RAG)...")
            _get_rag_collection()
            if HAS_CHROMA:
                print("  ✅ ChromaDB + sentence-transformers ready")
            else:
                print("  ⚠️  ChromaDB not available — using keyword fallback")

            system_instruction = (
                "You are a healthcare AI agent managing ICU operations at a hospital. "
                "You have access to hospital management tools AND medical analysis capabilities. "
                "Available tools include: checking bed availability, getting patient info, "
                "analyzing chest X-rays with multimodal AI (analyze_patient_xray), "
                "searching a medical knowledge base with vector RAG (search_medical_knowledge), "
                "assessing discharge readiness, assigning beds, and sending alerts. "
                "When handling a patient admission: "
                "1) Check bed availability, 2) Review patient information, "
                "3) Analyze their X-ray if available, "
                "4) Search medical knowledge base for treatment guidelines, "
                "5) Make bed assignments (which require physician approval), "
                "6) Alert the relevant care teams. "
                "Think step by step and explain your clinical reasoning. "
                "NEVER make final medical decisions without flagging for physician approval."
            )

            if BACKEND == "ollama":
                # ─── Ollama: Manual tool-calling loop ───
                print(f"  🤖 Starting agent with Ollama dual-model architecture...")
                print(f"      Brain (tool calling): {OLLAMA_TOOL_MODEL}")
                print(f"      Eyes  (vision/text):  {OLLAMA_MODEL}")
                print("  (Watch the LLM autonomously decide which tools to call!)\n")

                # Build tool schemas and function map
                ollama_tools = [build_ollama_tool_schema(f) for f in AGENT_TOOLS]
                tool_map = {f.__name__: f for f in AGENT_TOOLS}

                final_response = run_ollama_agent(
                    scenario=scenario,
                    system_instruction=system_instruction,
                    tools_schema=ollama_tools,
                    tool_functions=tool_map,
                    max_iterations=10,
                    print_steps=True,
                )

                print("\n" + "═" * 60)
                print("  📊 AGENT EXECUTION COMPLETE (Ollama local)")
                print("═" * 60)
                print("\n  🤖 Agent's Final Response:\n")
                if final_response:
                    for line in final_response.split("\n"):
                        print(f"      {line}")
                else:
                    print("      [No final response — see tool call trace above]")

            else:
                # ─── Gemini: Automatic function calling ───
                print("  🤖 Starting agent with AUTOMATIC function calling...")
                print("  (Watch the LLM autonomously decide which tools to call!)\n")

                config = types.GenerateContentConfig(
                    tools=AGENT_TOOLS,
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(
                        disable=False,
                    ),
                    system_instruction=system_instruction,
                )

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=scenario,
                    config=config,
                )

                print("\n" + "═" * 60)
                print("  📊 AGENT EXECUTION COMPLETE")
                print("═" * 60)
                print("\n  🤖 Agent's Final Response:\n")
                for line in response.text.split("\n"):
                    print(f"      {line}")

        except Exception as e:
            err_msg = str(e).split("\n")[0][:120]
            print(f"\n  ⚠️  Error: {err_msg}")
            print("  Showing pre-recorded trace instead:\n")
            run_demo_mode()

    # ═══════════════════════════════════════════════════════════
    # How Function Calling Works (Teaching Moment)
    # ═══════════════════════════════════════════════════════════
    print_section("How LLM Function Calling Works", "📖")
    print("""
    1. We define Python functions with TYPE HINTS and DOCSTRINGS
       → The LLM reads these to understand what each tool does

    2. We pass the functions to the model as tools
       → The LLM now knows it has these tools available

    3. We send a message: "Handle this STEMI patient..."
       → The LLM AUTONOMOUSLY decides: "I should check beds first"

    4. The tool-calling loop (auto for Gemini, manual for Ollama):
       → Model calls a function → gets result → decides next tool
         → repeat until done

    5. The entire multi-step reasoning happens:
       check_beds → get_vitals → analyze_xray → search_guidelines →
       assign_bed → alert_team

    KEY INSIGHT: The LLM is not following a script.
    It DECIDES which tools to use based on the situation.
    Change the scenario → the agent changes its behavior.

    💡 NOTICE: Two of these tools are the SAME capabilities we
    built earlier! analyze_patient_xray uses Module 1's multimodal
    approach, and search_medical_knowledge uses Module 2's RAG
    pipeline. The agent is the BRAIN that orchestrates everything.
    """)

    # ─── Human-in-the-Loop Safety ───
    print_section("Safety: Human-in-the-Loop", "🛡️")
    print("""
    Notice: assign_patient_to_bed() returns "PENDING_PHYSICIAN_APPROVAL"

    In production agentic AI, CRITICAL decisions are NEVER automated:
    ┌────────────────────────────────────────────────────┐
    │  AI CAN do autonomously:                           │
    │  ✅ Check bed availability                         │
    │  ✅ Look up patient records                        │
    │  ✅ Analyze X-rays (visual interpretation)         │
    │  ✅ Retrieve treatment guidelines                  │
    │  ✅ Send notifications                             │
    │                                                    │
    │  AI MUST get human approval for:                   │
    │  ⚠️ Bed assignments                               │
    │  ⚠️ Treatment decisions                           │
    │  ⚠️ Medication orders                             │
    │  ⚠️ Discharge decisions                           │
    └────────────────────────────────────────────────────┘

    The agent PROPOSES → The physician APPROVES → The system EXECUTES
    """)

    # ─── Ollama Alternative ───
    print_section("Local Alternative: Ollama Dual-Model", "💻")
    if BACKEND == "ollama":
        print(f"""
    ✅ YOU JUST RAN THE AGENT LOCALLY WITH TWO MODELS!

    🧠 Brain (Qwen3): {OLLAMA_TOOL_MODEL}
       → Orchestrated tool calls, decided reasoning chain
    👁️ Eyes (MedGemma): {OLLAMA_MODEL}
       → Analyzed X-rays, generated medical text

    The MANUAL tool-calling loop:
    1. Send prompt + tool schemas → Qwen3 returns tool_calls
    2. Execute the matching Python function
       (if it's analyze_xray → MedGemma sees the image!)
    3. Feed the result back as a 'tool' message
    4. Repeat until Qwen3 returns plain text (done!)

    100% local — no patient data left this machine.
    """)
    else:
        print(f"""
    This agent ran on Gemini (cloud) with AUTOMATIC function calling.
    The SAME agent also runs locally via Ollama + MedGemma 1.5:

        WORKSHOP_BACKEND=ollama   (in .env)

    The local version uses a MANUAL tool-calling loop:
    model returns tool_calls → we execute → feed result back → repeat.

    Same intelligence, same architecture, but no data leaves the machine.
    """)

    # Summary
    print(f"\n{'🎯'*25}")
    print("  MODULE 3 — KEY TAKEAWAYS")
    print(f"{'🎯'*25}")
    print("""
    1. AGENTS = LLMs that USE TOOLS and REASON about what to do next
       Not chatbots. Not if/else rules. REAL autonomous reasoning.

    2. THIS AGENT USES EVERYTHING WE BUILT:
       🔬 Module 1's multimodal vision → analyze_patient_xray()
       📚 Module 2's vector RAG       → search_medical_knowledge()
       🏥 Hospital management tools     → beds, alerts, assignments

    3. FUNCTION CALLING is the core mechanism:
       Define Python functions → Give to LLM → LLM decides when to use them

    4. AUTOMATIC FUNCTION CALLING handles the full loop:
       LLM thinks → calls tool → gets result → thinks again → calls next tool

    5. HUMAN-IN-THE-LOOP is mandatory for healthcare:
       AI proposes → Human approves → System executes

    6. This is PRODUCTION ARCHITECTURE used by:
       • Microsoft Healthcare Agent Orchestrator
       • Amazon Connect Health
       • Google's AMIE diagnostic agent

    🔑 "We built the eyes (multimodal), the memory (RAG), and then
        the BRAIN (this agent) that orchestrates everything. That's
        how real healthcare AI systems work."
    """)
