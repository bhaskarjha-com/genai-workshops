"""
🧠 Workshop 3 — Module 1: Multimodal Medical AI
=============================================================
Duration: ~20 min | Tech: Gemini 2.5 Flash or MedGemma 1.5 (via Ollama)

THIS IS NOT RULE-BASED. This uses a real multimodal LLM to:
  1. Analyze a chest X-ray IMAGE
  2. Process text symptoms
  3. Combine image + text + vitals for comprehensive diagnosis

Backends: Gemini (cloud) | Ollama/MedGemma (local GPU) | Demo (pre-recorded)
Setup:   pip install -r requirements.txt
         Set GEMINI_API_KEY in .env (or use WORKSHOP_BACKEND=ollama)
"""

import os
import sys
import textwrap
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

from workshop_config import BACKEND, get_ollama_vision_response, get_ollama_response

# ─── API Setup ─────────────────────────────────────────────────
DEMO_MODE = (BACKEND == "demo")
client = None
if BACKEND == "gemini":
    from google import genai
    from google.genai import types
    client = genai.Client()


# ─── Pre-recorded outputs for demo mode ──────────────────────
DEMO_OUTPUTS = {
    "text_only": textwrap.dedent("""\
        Based on the symptoms described (crushing chest pain radiating to the left arm,
        profuse sweating, nausea, and shortness of breath), this presentation is highly
        concerning for an **Acute Myocardial Infarction (Heart Attack)**, specifically
        a possible **ST-Elevation Myocardial Infarction (STEMI)**.

        **Urgency: CRITICAL — Seek emergency care immediately (call 108/112).**

        Key concerns:
        - Crushing chest pain with radiation = classic cardiac presentation
        - Diaphoresis (sweating) = sympathetic activation
        - Associated nausea and dyspnea = common MI accompaniments

        However, without vital signs, labs, or imaging, I cannot confirm this diagnosis.
        Differential diagnoses include unstable angina, pulmonary embolism, or aortic
        dissection. **Immediate ECG and troponin levels are essential.**"""),

    "image_only": textwrap.dedent("""\
        **Chest X-ray Analysis:**

        Findings:
        1. **Cardiomegaly** — The cardiac silhouette appears enlarged (cardiothoracic
           ratio > 0.5), suggesting possible cardiac hypertrophy or pericardial effusion.
        2. **Right lower lobe opacity** — There is an area of increased density in the
           right lower lung zone, which could represent consolidation (pneumonia),
           atelectasis, or pleural effusion.
        3. **Costophrenic angles** — The right costophrenic angle appears blunted,
           suggesting a small right-sided pleural effusion.
        4. **No pneumothorax** — Lung markings extend to the periphery bilaterally.
        5. **Bony structures** — No acute fractures identified.

        **Impression:** Cardiomegaly with right lower lobe consolidation and possible
        small right pleural effusion. Clinical correlation recommended."""),

    "multimodal": textwrap.dedent("""\
        **Comprehensive Multimodal Assessment:**

        Integrating the chest X-ray findings with the clinical presentation:

        **Primary Diagnosis: Acute ST-Elevation Myocardial Infarction (STEMI)**
        Confidence: HIGH (92%)

        Evidence Fusion:
        1. 🔴 **Symptoms** (text): Crushing chest pain + left arm radiation + diaphoresis
           = Classic acute coronary syndrome presentation
        2. 🔴 **X-ray** (image): Cardiomegaly confirms pre-existing cardiac disease,
           increasing MI probability. Right lower lobe opacity may represent
           pulmonary congestion from acute heart failure.
        3. 🔴 **Vitals**: BP 85/55 (cardiogenic shock), HR 120 (compensatory tachycardia),
           SpO2 89% (hypoxemia from pulmonary congestion)
        4. 🔴 **Labs**: Troponin 0.15 ng/mL (ELEVATED — confirms myocardial injury)

        **Urgency: CRITICAL — Activate Cardiac Catheterization Lab**

        Immediate Actions:
        → Aspirin 325mg + dual antiplatelet therapy
        → IV heparin
        → Primary PCI within 90 minutes (door-to-balloon time)
        → Continuous cardiac monitoring
        → Prepare for possible cardiogenic shock management (IABP/Impella)

        The integration of imaging (cardiomegaly, pulmonary congestion), clinical symptoms,
        hemodynamic compromise (BP 85/55), and biomarker elevation (troponin 0.15) provides
        **high-confidence multimodal diagnosis** compared to any single data source alone.

        ⚠️ DISCLAIMER: This is an AI-assisted analysis. Final diagnosis and treatment
        decisions must be made by a qualified physician."""),
}


# ─── Helper ───────────────────────────────────────────────────
def print_section(title, icon="🔬"):
    print(f"\n{'─'*60}")
    print(f"  {icon} {title}")
    print(f"{'─'*60}")


def call_gemini(prompt, image_bytes=None, label="Response"):
    """Call LLM (Gemini or Ollama) or show demo output."""
    if DEMO_MODE:
        key = label.lower().replace(" ", "_")
        output = DEMO_OUTPUTS.get(key, f"[Demo output for: {label}]")
        print(f"\n  📝 {label} (DEMO MODE — pre-recorded):\n")
        for line in output.split("\n"):
            print(f"    {line}")
        return output

    try:
        if BACKEND == "ollama":
            # ─── Ollama path ───
            if image_bytes is not None:
                text = get_ollama_vision_response(prompt, image_bytes)
            else:
                text = get_ollama_response(prompt)
            source = "Ollama (MedGemma local)"
        else:
            # ─── Gemini path ───
            contents = []
            if image_bytes is not None:
                contents.append(types.Part.from_bytes(data=image_bytes, mime_type="image/png"))
            contents.append(prompt)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents,
            )
            text = response.text
            source = "Gemini"

        print(f"\n  📝 {label} (LIVE from {source}):\n")
        for line in text.split("\n"):
            print(f"    {line}")
        return text
    except Exception as e:
        err_msg = str(e).split("\n")[0][:120]
        print(f"\n  ⚠️  API Error: {err_msg}")
        print(f"  Showing pre-recorded output instead.\n")
        key = label.lower().replace(" ", "_")
        output = DEMO_OUTPUTS.get(key, f"[Fallback for: {label}]")
        for line in output.split("\n"):
            print(f"    {line}")
        return output


def load_image(path=None):
    """Try to load a medical image as bytes."""
    if DEMO_MODE:
        return None

    search_paths = [
        path,
        "sample_chest_xray.png",
        Path(__file__).parent / "sample_chest_xray.png",
    ]
    for p in search_paths:
        if p and Path(str(p)).exists():
            with open(str(p), "rb") as f:
                img_bytes = f.read()
            print(f"  ✅ Loaded medical image: {p}")
            return img_bytes
    print("  ⚠️  No medical image found. Using text-only analysis.")
    print("  Place 'sample_chest_xray.png' in this directory for full demo.")
    return None


# ─── Patient Case ─────────────────────────────────────────────
PATIENT = {
    "name": "Ramesh K.", "age": 58, "sex": "Male",
    "symptoms": (
        "Crushing chest pain radiating to the left arm for the past 45 minutes. "
        "Profuse sweating, nausea, shortness of breath. "
        "Patient is anxious and clutching his chest."
    ),
    "vitals": "BP 85/55 mmHg, HR 120 bpm, SpO2 89%, RR 26/min, Temp 36.8°C",
    "labs": "Troponin: 0.15 ng/mL (ELEVATED), WBC: 11,000, Glucose: 145 mg/dL",
    "history": "Hypertension (10 years), Smoker (30 pack-years), Family h/o CAD",
}


# ─── Main Demo ────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    backend_label = "MedGemma 1.5 (local GPU)" if BACKEND == "ollama" else "Gemini 2.5 Flash (cloud)"
    print(f"  🧠 MODULE 1 — Multimodal Medical AI ({backend_label})")
    print("=" * 60)
    print(f"""
    We're going to show that combining MULTIPLE data types gives
    better diagnoses than any single source alone.

    Using {backend_label} — a real multimodal LLM that
    can SEE images AND read text simultaneously.
    """)

    # Load medical image
    print_section("Loading Medical Image", "📷")
    medical_image = load_image()

    # Show patient info
    print_section("Patient Presentation", "🏥")
    print(f"  Patient: {PATIENT['name']}, {PATIENT['age']}y {PATIENT['sex']}")
    print(f"  Symptoms: {PATIENT['symptoms'][:80]}...")
    print(f"  Vitals: {PATIENT['vitals']}")
    print(f"  Labs: {PATIENT['labs']}")
    print(f"  History: {PATIENT['history']}")

    # ═══════════════════════════════════════════════════════════
    # APPROACH 1: Text Only (symptoms alone)
    # ═══════════════════════════════════════════════════════════
    print_section("APPROACH 1: Text-Only Diagnosis", "📝")
    print("  Sending ONLY text symptoms to the LLM (no image, no vitals)...")

    text_prompt = f"""You are a medical AI assistant. Based ONLY on these symptoms,
provide your assessment. Be specific about your confidence level and what
additional information you would need.

Patient: {PATIENT['age']}-year-old {PATIENT['sex']}
Symptoms: {PATIENT['symptoms']}

Provide: 1) Most likely diagnosis 2) Urgency level 3) What else you need to know"""

    call_gemini(text_prompt, label="text_only")

    # ═══════════════════════════════════════════════════════════
    # APPROACH 2: Image Only (chest X-ray alone)
    # ═══════════════════════════════════════════════════════════
    print_section("APPROACH 2: Image-Only Analysis", "📷")
    if medical_image:
        print("  Sending ONLY the chest X-ray to the LLM (no clinical info)...")
        image_prompt = """You are a radiologist AI. Analyze this chest X-ray image.
Describe ALL findings systematically:
1) Heart size and silhouette
2) Lung fields (both sides)
3) Costophrenic angles
4) Bony structures
5) Overall impression"""
        call_gemini(image_prompt, image_bytes=medical_image, label="image_only")
    else:
        print("  [Skipping — no image available. See text-only and multimodal demos.]")
        call_gemini("", label="image_only")

    # ═══════════════════════════════════════════════════════════
    # APPROACH 3: Full Multimodal (image + text + vitals + labs)
    # ═══════════════════════════════════════════════════════════
    print_section("APPROACH 3: MULTIMODAL Diagnosis (Image + Text + Vitals)", "🔬")
    print("  Sending EVERYTHING to the LLM: X-ray + symptoms + vitals + labs...")
    print("  This is how modern medical AI actually works!")

    multimodal_prompt = f"""You are a senior emergency physician AI assistant performing
a comprehensive multimodal assessment. You have access to:

1. CHEST X-RAY: [attached image]
2. CLINICAL PRESENTATION:
   Patient: {PATIENT['age']}-year-old {PATIENT['sex']}
   Symptoms: {PATIENT['symptoms']}
3. VITAL SIGNS: {PATIENT['vitals']}
4. LAB RESULTS: {PATIENT['labs']}
5. MEDICAL HISTORY: {PATIENT['history']}

Provide a COMPREHENSIVE multimodal assessment:
- Integrate X-ray findings WITH clinical data
- Primary diagnosis with confidence level
- Explain how EACH data modality contributes to the diagnosis
- Urgency classification
- Immediate recommended actions
- Note how combining modalities gives higher confidence than any single source"""

    call_gemini(multimodal_prompt, image_bytes=medical_image, label="multimodal")

    # ═══════════════════════════════════════════════════════════
    # Comparison Summary
    # ═══════════════════════════════════════════════════════════
    print_section("WHY MULTIMODAL IS BETTER", "📊")
    print("""
    ┌─────────────────────────────────────────────────────────┐
    │  APPROACH           │ WHAT IT SEES    │ CONFIDENCE       │
    ├─────────────────────┼─────────────────┼──────────────────┤
    │  Text-only          │ Symptoms only   │ Moderate (~60%)  │
    │  Image-only         │ X-ray only      │ Moderate (~65%)  │
    │  MULTIMODAL         │ ALL data        │ HIGH (~90%)      │
    └─────────────────────────────────────────────────────────┘

    The multimodal approach is EXACTLY how these real systems work:
    • Med-PaLM M (Google) — text + imaging + EHR data
    • AMIE (Google DeepMind) — dialogue + images + lab results
    • BiomedCLIP (Microsoft) — 15M medical image-text pairs
    • MedGemma (Google) — open-source medical multimodal model
    """)

    print_section("LOCAL ALTERNATIVE: Ollama + MedGemma", "💻")
    if BACKEND == "ollama":
        print("""
    ✅ YOU'RE ALREADY RUNNING LOCALLY!

    This module is using MedGemma 1.5 on your own GPU via Ollama.
    No patient data left this machine. No cloud API needed.

    This is exactly how hospitals deploy AI in production:
    • Patient data NEVER leaves the hospital network
    • HIPAA/DPDP Act compliance — no third-party data processing
    • Works offline — critical for rural hospitals
    • You control the model version — no surprise updates
    """)
    else:
        print(f"""
    This module ran on Gemini (cloud). But the SAME code supports
    local deployment via Ollama + MedGemma 1.5 — just change one line:

        WORKSHOP_BACKEND=ollama   (in .env)

    Why local matters in healthcare:
    • Patient data NEVER leaves the hospital network
    • HIPAA/DPDP Act compliance — no third-party data processing
    • Works offline — critical for rural hospitals
    • You control the model version — no surprise updates
    """)

    # Summary
    print(f"\n{'🎯'*25}")
    print("  MODULE 1 — KEY TAKEAWAYS")
    print(f"{'🎯'*25}")
    print("""
    1. MULTIMODAL AI combines images + text + structured data
       using a SINGLE model — not separate pipelines

    2. The LLM can LITERALLY SEE medical images and reason about
       them alongside clinical context

    3. This is a TOOL our agent will use in Module 3 —
       the agent will call "analyze_patient_xray" as one
       of its available functions

    4. For production: use LOCAL models (Ollama/MedGemma) to keep
       patient data private

    🔑 "The AI doesn't just read symptoms — it SEES the X-ray,
        READS the labs, and REASONS about all of it together."
    """)
