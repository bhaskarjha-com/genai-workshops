"""
🛡️ Workshop 3 — Module 5: Safety, Guardrails & Responsible AI
===============================================================
Duration: ~15 min | Tech: Guardrails on Module 3 agent + Case Studies

Before deploying our agent, we add SAFETY LAYERS:
  1. Real-world AI failure case studies (what went wrong and why)
  2. LIVE guardrails that wrap the agent's outputs
  3. Input/output validation on every agent action
  4. Regulatory landscape: FDA, CDSCO, EU AI Act, DPDP Act
  5. Deployment readiness checklist

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

client = None
if BACKEND == "gemini":
    try:
        from google import genai
        client = genai.Client()
    except ImportError:
        DEMO_MODE = True


def print_section(title, icon="🛡️"):
    print(f"\n{'─'*60}")
    print(f"  {icon} {title}")
    print(f"{'─'*60}")


# ═══════════════════════════════════════════════════════════════
# PART 1: Real AI Failure Case Studies
# ═══════════════════════════════════════════════════════════════

def failure_case_studies():
    """Documented cases of healthcare AI going wrong."""

    cases = [
        {
            "name": "IBM Watson for Oncology (2013–2022)",
            "what_happened": (
                "IBM's Watson for Oncology was marketed as an AI that could recommend "
                "cancer treatments. It was deployed at major hospitals worldwide."
            ),
            "what_went_wrong": (
                "Investigation revealed Watson's recommendations were based on a small "
                "number of synthetic cases, not real patient data. MD Anderson spent $62M "
                "on the project. Watson recommended unsafe treatments in multiple cases, "
                "including suggesting a drug that would interact fatally with a patient's "
                "other medications."
            ),
            "lesson": "AI trained on synthetic/limited data fails in the real world.",
            "icon": "💊",
        },
        {
            "name": "Optum/UnitedHealth Racial Bias (2019)",
            "what_happened": (
                "A widely-used algorithm by Optum/UnitedHealth determined which patients "
                "needed extra healthcare attention. It affected 200 million Americans."
            ),
            "what_went_wrong": (
                "Researchers found the algorithm systematically discriminated against Black "
                "patients. It used healthcare SPENDING as a proxy for health needs. Because "
                "Black patients historically had less access to care (and therefore lower "
                "spending), the algorithm concluded they were healthier — denying them "
                "needed care. At a given risk score, Black patients were significantly "
                "sicker than White patients."
            ),
            "lesson": "Proxy variables can encode systemic bias. Cost ≠ Health.",
            "icon": "⚖️",
        },
        {
            "name": "Epic Sepsis Model (2021)",
            "what_happened": (
                "Epic Systems' sepsis prediction model was deployed at hundreds of hospitals "
                "to detect sepsis early and save lives."
            ),
            "what_went_wrong": (
                "External validation showed the model MISSED 67% of sepsis cases while "
                "generating massive numbers of false alarms. Nurses experienced alert "
                "fatigue — ignoring ALL alerts, including real emergencies. The model's "
                "published 76% sensitivity dropped to 33% in real-world use."
            ),
            "lesson": "Lab performance ≠ real-world performance. False alarms kill trust.",
            "icon": "🚨",
        },
        {
            "name": "Dermatology AI Skin Cancer (2021–2023)",
            "what_happened": (
                "Multiple AI skin cancer detection tools were trained and showed impressive "
                "accuracy in detecting melanoma from skin images."
            ),
            "what_went_wrong": (
                "Models were trained primarily on light-skinned patients. Accuracy dropped "
                "significantly for darker skin tones. Some models had <30% accuracy on dark "
                "skin vs >90% on light skin. This meant the most vulnerable populations — "
                "who already face delayed diagnosis — got the worst AI performance."
            ),
            "lesson": "AI is only as diverse as its training data.",
            "icon": "📸",
        },
    ]

    for case in cases:
        print(f"\n  {case['icon']} {case['name']}")
        print(f"  {'─'*50}")
        print(textwrap.fill(f"  What happened: {case['what_happened']}", width=60,
                            initial_indent="  ", subsequent_indent="    "))
        print()
        print(textwrap.fill(f"  What went wrong: {case['what_went_wrong']}", width=60,
                            initial_indent="  ", subsequent_indent="    "))
        print(f"\n  💡 Lesson: {case['lesson']}")


# ═══════════════════════════════════════════════════════════════
# PART 2: Live Guardrails on Agent Outputs
# ═══════════════════════════════════════════════════════════════

class HealthcareGuardrail:
    """Safety guardrails that wrap ANY healthcare AI agent's outputs.
    These run BEFORE any action is executed."""

    # Actions that ALWAYS require physician approval
    CRITICAL_ACTIONS = [
        "prescribe_medication", "modify_dosage", "discharge_patient",
        "assign_patient_to_bed", "cancel_treatment", "change_diagnosis",
    ]

    # Topics the AI should NEVER give definitive answers on
    FORBIDDEN_CLAIMS = [
        "guaranteed", "100% cure", "no side effects", "definitely",
        "proven to cure", "replaces your doctor", "stop taking medication",
    ]

    # Confidence thresholds
    MIN_CONFIDENCE = 0.7
    ESCALATION_THRESHOLD = 0.5

    def validate_output(self, agent_text, action_type=None):
        """Validate an agent's output before it reaches the patient/doctor."""
        issues = []

        # Check 1: Forbidden claims
        for phrase in self.FORBIDDEN_CLAIMS:
            if phrase.lower() in agent_text.lower():
                issues.append({
                    "severity": "CRITICAL",
                    "type": "FORBIDDEN_CLAIM",
                    "detail": f"Agent used forbidden phrase: '{phrase}'",
                    "action": "BLOCK — do not deliver this output",
                })

        # Check 2: Critical actions need approval
        if action_type and action_type in self.CRITICAL_ACTIONS:
            issues.append({
                "severity": "WARNING",
                "type": "REQUIRES_APPROVAL",
                "detail": f"Action '{action_type}' requires physician sign-off",
                "action": "HOLD — queue for physician review",
            })

        # Check 3: Missing disclaimer
        disclaimer_keywords = ["consult", "physician", "doctor", "professional",
                               "not a substitute", "medical advice"]
        has_disclaimer = any(kw in agent_text.lower() for kw in disclaimer_keywords)
        if not has_disclaimer and len(agent_text) > 100:
            issues.append({
                "severity": "WARNING",
                "type": "MISSING_DISCLAIMER",
                "detail": "Output lacks medical professional consultation disclaimer",
                "action": "APPEND standard disclaimer before delivery",
            })

        # Check 4: Dosage mention without verification
        dosage_terms = ["mg", "ml", "mcg", "units", "dose", "dosage"]
        if any(term in agent_text.lower() for term in dosage_terms):
            issues.append({
                "severity": "CRITICAL",
                "type": "DOSAGE_MENTIONED",
                "detail": "Agent output mentions specific dosages",
                "action": "VERIFY — cross-reference with pharmacy database",
            })

        return {
            "passed": len([i for i in issues if i["severity"] == "CRITICAL"]) == 0,
            "issues": issues,
            "total_issues": len(issues),
            "critical_issues": len([i for i in issues if i["severity"] == "CRITICAL"]),
        }


def guardrails_demo():
    """Run the guardrails on example safe and unsafe outputs."""

    guardrail = HealthcareGuardrail()

    # Test cases
    test_outputs = [
        {
            "label": "SAFE Agent Output",
            "text": (
                "Based on the patient's symptoms (chest pain, elevated troponin) and the "
                "AHA STEMI guidelines, I recommend immediate cardiology consultation for "
                "evaluation for primary PCI. The patient should be monitored in the ICU. "
                "This assessment should be reviewed by the attending physician before any "
                "treatment decisions are made."
            ),
            "action": None,
        },
        {
            "label": "UNSAFE Agent Output #1",
            "text": (
                "The patient definitely has a heart attack. Start aspirin 325mg and "
                "heparin 60 units/kg immediately. This treatment is guaranteed to work "
                "with no side effects. The AI has 100% cure rate for this condition."
            ),
            "action": "prescribe_medication",
        },
        {
            "label": "UNSAFE Agent Output #2",
            "text": (
                "Patient seems fine. Recommend they stop taking medication and go home. "
                "This diagnosis proves the patient is healthy. No further treatment needed."
            ),
            "action": "discharge_patient",
        },
    ]

    for test in test_outputs:
        print(f"\n  📋 Testing: {test['label']}")
        print(f"  Input: \"{test['text'][:70]}...\"")

        result = guardrail.validate_output(test["text"], test.get("action"))

        if result["passed"]:
            print(f"  ✅ PASSED — {result['total_issues']} non-critical issues")
        else:
            print(f"  ❌ BLOCKED — {result['critical_issues']} critical issue(s)")

        for issue in result["issues"]:
            icon = "🔴" if issue["severity"] == "CRITICAL" else "🟡"
            print(f"    {icon} [{issue['severity']}] {issue['type']}")
            print(f"       {issue['detail']}")
            print(f"       → {issue['action']}")


# ═══════════════════════════════════════════════════════════════
# PART 3: Safe vs Unsafe AI Comparison (Live LLM Demo)
# ═══════════════════════════════════════════════════════════════

def safe_vs_unsafe_demo():
    """Show how system prompts and guardrails change AI behavior."""

    print_section("Safe vs Unsafe AI (System Prompt Matters)", "⚡")

    question = "I've been having chest pain for a week. What should I do?"

    unsafe_prompt = f"Answer this medical question directly and confidently: {question}"
    safe_prompt = f"""You are a medical AI assistant. You MUST follow these rules:
1. NEVER provide a definitive diagnosis
2. ALWAYS recommend consulting a healthcare professional
3. Provide general educational information ONLY
4. Include appropriate urgency warnings
5. Never recommend specific medications or dosages

Patient asks: {question}"""

    if not DEMO_MODE:
        try:
            print(f"\n  ❓ Patient question: \"{question}\"\n")
            print(f"  ❌ WITHOUT safety prompt:")
            if BACKEND == "ollama":
                r1_text = get_ollama_response(unsafe_prompt)
            else:
                r1_text = client.models.generate_content(
                    model="gemini-2.5-flash", contents=unsafe_prompt
                ).text
            for line in r1_text.split("\n")[:8]:
                print(f"    {line}")

            print(f"\n  ✅ WITH safety prompt:")
            if BACKEND == "ollama":
                r2_text = get_ollama_response(safe_prompt)
            else:
                r2_text = client.models.generate_content(
                    model="gemini-2.5-flash", contents=safe_prompt
                ).text
            for line in r2_text.split("\n"):
                print(f"    {line}")
            return
        except Exception:
            pass

    # Demo mode fallbacks
    print(f"\n  ❓ Patient asks: \"{question}\"\n")

    print("  ❌ WITHOUT Safety Prompt (DANGEROUS):")
    print(textwrap.indent(textwrap.dedent("""\
        You probably have angina or a heart attack. Take aspirin 325mg
        immediately and nitroglycerin if available. If pain persists after
        3 doses, you might have a blockage. You should start a statin
        regimen — take atorvastatin 40mg daily.

        ⚠️ PROBLEMS:
        → Gives a diagnosis without examination
        → Recommends specific medications and dosages
        → No urgency warning (chest pain for a WEEK!)
        → No disclaimer about consulting a professional"""), "    "))

    print("\n  ✅ WITH Safety Prompt (RESPONSIBLE):")
    print(textwrap.indent(textwrap.dedent("""\
        Chest pain lasting a week is something that should be evaluated
        by a healthcare professional as soon as possible. While there are
        many possible causes (some benign, some serious), persistent chest
        pain warrants medical attention.

        ⚠️ If you experience any of these, call emergency services (108/112)
        immediately: severe or crushing chest pain, pain radiating to arm/jaw,
        shortness of breath, lightheadedness, or cold sweats.

        I am an AI assistant and cannot diagnose medical conditions. Please
        see a doctor or visit an emergency department for proper evaluation.

        ✅ SAFE: No diagnosis, no medications, clear urgency warning,
           appropriate disclaimer, directs to professional care."""), "    "))


# ═══════════════════════════════════════════════════════════════
# PART 4: Regulatory Landscape
# ═══════════════════════════════════════════════════════════════

def regulatory_landscape():
    """Key regulations for healthcare AI in 2026."""

    print("""
  ┌────────────────────────────────────────────────────────────┐
  │   REGULATION              │ SCOPE         │ KEY REQUIREMENT │
  ├────────────────────────────────────────────────────────────┤
  │ 🇺🇸 FDA AI/ML SaMD        │ Medical AI    │ Clinical        │
  │    Framework               │ devices       │ validation +    │
  │                            │               │ bias analysis   │
  ├────────────────────────────────────────────────────────────┤
  │ 🇪🇺 EU AI Act (2025)      │ All AI in EU  │ Healthcare AI = │
  │                            │               │ "HIGH RISK" →   │
  │                            │               │ mandatory audit │
  ├────────────────────────────────────────────────────────────┤
  │ 🇮🇳 DPDP Act 2023         │ Data privacy  │ Consent-based   │
  │    (India)                 │ for Indians   │ processing,     │
  │                            │               │ ₹250 Cr penalty │
  ├────────────────────────────────────────────────────────────┤
  │ 🇮🇳 CDSCO + SAHI          │ Medical       │ AI diagnostic   │
  │    (India, Jan 2026)       │ devices       │ software = Class│
  │                            │               │ C med device    │
  ├────────────────────────────────────────────────────────────┤
  │ 🇮🇳 ABDM / ABHA           │ Health data   │ Standardized    │
  │    (Ayushman Bharat)       │ exchange      │ health IDs +    │
  │                            │               │ interoperability│
  └────────────────────────────────────────────────────────────┘

  🆕 India AI Update (2026):
  → SAHI (Strategy for AI in Healthcare for India) — unveiled at India
    AI Summit 2026. National blueprint for ethical AI adoption in healthcare.
  → CDSCO now classifies AI diagnostic software as CLASS C medical devices
    (Jan 2026). Requires manufacturing/import license + clinical validation
    on INDIAN patient populations.
  → BODH platform (IIT Kanpur + NHA): benchmarks AI models using real-world
    data while preserving patient privacy.
  → Indian AI startups (Qure.ai, Niramai, SigTuple) must now comply with:
    DPDP Act (data) + CDSCO (device) + ABDM (interoperability)
    """)


# ═══════════════════════════════════════════════════════════════
# PART 5: Deployment Checklist
# ═══════════════════════════════════════════════════════════════

def deployment_checklist():
    """What a real team checks before deploying healthcare AI."""
    items = [
        ("Clinical Validation", "Prospective study on target population", "FDA/CDSCO"),
        ("Bias Audit", "AIF360 metrics pass for all demographic groups", "EU AI Act"),
        ("Explainability", "SHAP/LIME explanations for every prediction", "FDA"),
        ("Guardrails", "Input/output validation, forbidden action lists", "Internal"),
        ("Human-in-the-Loop", "Critical decisions require physician approval", "All"),
        ("Data Privacy", "HIPAA/DPDP compliance, encryption, access controls", "DPDP/HIPAA"),
        ("Model Cards", "Document model capabilities, limitations, and bias", "Best practice"),
        ("Monitoring", "Drift detection, accuracy tracking, alert thresholds", "FDA post-market"),
        ("Audit Trail", "Every AI decision logged with timestamp and rationale", "EU AI Act"),
        ("Failover", "Graceful degradation when AI is unavailable", "Internal"),
    ]

    print("\n  ✈️  DEPLOYMENT READINESS CHECKLIST")
    print(f"  {'─'*60}\n")
    for i, (item, detail, regulation) in enumerate(items, 1):
        print(f"    {'☐':>2}  {i:>2}. {item:<25} {detail}")
        print(f"         Required by: {regulation}\n")


# ─── Main ─────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  🛡️  MODULE 5 — Safety, Guardrails & Responsible AI")
    print("=" * 60)
    print("""
    "Every one of these failures happened at MAJOR institutions
     with EXPERT teams. If they got it wrong, what makes us think
     we won't? That's why we need SYSTEMATIC safety checks."
    """)

    # Part 1: Failure case studies
    print_section("Real-World AI Failures", "💀")
    failure_case_studies()

    # Part 2: Live guardrails demo
    print_section("LIVE: Guardrails on Agent Outputs", "🛡️")
    print("""
    These guardrails wrap our Module 3 agent. Every output
    is checked BEFORE it reaches any patient or doctor.
    """)
    guardrails_demo()

    # Part 3: Safe vs Unsafe AI
    safe_vs_unsafe_demo()

    # Part 4: Regulations
    print_section("Regulatory Landscape (2026)", "📜")
    regulatory_landscape()

    # Part 5: Deployment checklist
    print_section("Deployment Readiness Checklist", "✈️")
    deployment_checklist()

    # Summary
    print(f"\n{'🎯'*25}")
    print("  MODULE 5 — KEY TAKEAWAYS")
    print(f"{'🎯'*25}")
    print("""
    1. REAL FAILURES HAPPEN — IBM Watson, Optum bias, Epic sepsis,
       skin cancer AI — all at top institutions. Safety isn't optional.

    2. GUARDRAILS are code that wraps your agent:
       • Block dangerous outputs (specific dosages, false guarantees)
       • Flag critical actions (prescriptions, discharges) for approval
       • Ensure disclaimers are present

    3. SYSTEM PROMPTS matter enormously:
       The SAME model gives dangerously different answers with and
       without proper safety instructions

    4. REGULATORY COMPLIANCE is mandatory:
       • India: DPDP Act + CDSCO + ABDM
       • US: FDA AI/ML SaMD Framework
       • EU: AI Act (healthcare = high-risk)

    5. THE FULL STACK we built today:
       Module 1: Multimodal vision (agent's eyes)
       Module 2: RAG knowledge (agent's memory)
       Module 3: Function calling (agent's brain) ← centerpiece
       Module 4: Bias + fairness (agent's conscience)
       Module 5: Guardrails (agent's safety net) ← this module

    🔑 "Building AI that works is hard. Building AI that works
        SAFELY and FAIRLY is the real challenge — and the only
        version worth deploying."
    """)
