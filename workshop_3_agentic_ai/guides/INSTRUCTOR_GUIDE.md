# 🎓 Workshop 3 Instructor Guide v3 — Frontier Agentic AI in Healthcare

## Quick Reference

| Item | Detail |
|------|--------|
| **Title** | "Agentic AI in Healthcare" |
| **Duration** | ~110 min |
| **Cloud LLM** | Gemini 2.5 Flash (free API, `google-genai` SDK) |
| **Local LLM** | MedGemma 1.5 4B via Ollama (multimodal, medical-trained) |
| **Backend Config** | `workshop_config.py` — set `WORKSHOP_BACKEND` in `.env` |
| **API Key** | Free from [aistudio.google.com](https://aistudio.google.com/apikey) |
| **Key Change** | Three-tier backend: Gemini → Ollama → Demo Mode |

---

## ⏱️ Timeline

| Time | Module | File | Tech |
|------|--------|------|------|
| 0:00–0:05 | Opening | — | Recap W1-W2 |
| 0:05–0:25 | Module 1: Multimodal | `01_multimodal_medical_ai.py` | Gemini multimodal API |
| 0:25–0:45 | Module 2: RAG | `02_medical_rag_frontier.py` | ChromaDB + transformers |
| 0:45–0:50 | **Break** | — | 5 min |
| 0:50–1:20 | ⭐ Module 3: Agent | `03_healthcare_agent_frontier.py` | **Gemini function calling** |
| 1:20–1:40 | Module 4: Bias | `04_bias_and_fairness.py` | SHAP + AIF360 |
| 1:40–1:55 | Module 5: Safety | `05_safety_and_guardrails.py` | Guardrails + ethics |
| 1:55–2:00 | Wrap-up | — | Careers + Q&A |

---

## 🔧 Pre-Workshop Setup (15 min)

### 1. Get Gemini API Key (30 seconds)
```
1. Go to https://ai.google.dev
2. Click "Get API Key"
3. Create key → copy it
4. Set it:
   # Linux/Mac/Colab:
   export GEMINI_API_KEY="your_key_here"
   # Windows:
   set GEMINI_API_KEY=your_key_here
```

### 2. Install Dependencies
```bash
pip install google-genai chromadb sentence-transformers shap aif360 python-dotenv
```

### 3. Test Each Module
```bash
python 01_multimodal_medical_ai.py     # needs API key + sample_chest_xray.png
python 02_medical_rag_frontier.py      # needs API key + chromadb
python 03_healthcare_agent_frontier.py # needs API key (STAR module!)
python 04_bias_and_fairness.py         # local only (sklearn, shap, aif360)
python 05_safety_and_guardrails.py     # needs API key for live safe/unsafe demo
```

### 4. Backup: Ollama (if API issues)
```bash
# Install Ollama from https://ollama.com/download
# Then pull the medical model:
ollama pull dcarrascosa/medgemma-1.5-4b-it:Q8_0

# Switch backend:
# Set WORKSHOP_BACKEND=ollama in .env
```

### 5. Verify sample_chest_xray.png exists
Module 1 and Module 3 both use this for multimodal X-ray analysis.

---

## 🎤 Opening Script (0:00–0:05)

> *"Good morning everyone! Welcome to Workshop 3 — Agentic AI in Healthcare.*
>
> *Quick recap: In Workshop 1, you SAW what GenAI can do — text generation, image generation, how transformers work. In Workshop 2, you BUILT things — local models with Ollama, RAG pipelines, medical summarization.*
>
> *Today, we go to the frontier. We're building an AI AGENT — not a chatbot that answers questions, but a system that REASONS, ACTS, and makes autonomous decisions in a hospital ICU setting.*
>
> *Here's the journey: First, we build the agent's EYES — multimodal AI that can literally see X-rays. Then, its MEMORY — a RAG knowledge base of real medical guidelines. Then, the BRAIN — an agent that uses both of those tools plus hospital management functions to handle an emergency admission. And finally, we ask: can we TRUST it? Can we DEPLOY it safely?*
>
> *Everything runs live with Gemini 2.5 Flash — Google's latest. You'll see real AI in action. Let's go."*

---

## 📝 Per-Module Talking Points

### Module 1 — Multimodal (20 min)
**Hook**: "Doctors don't diagnose from a text message. Gemini can literally SEE this X-ray."

**Key moments**:
1. Text-only prompt → "Could be many things"
2. Image-only → "X-ray shows cardiomegaly"
3. Image + text + vitals → "STEMI with cardiogenic shock" (HIGH confidence)
4. "See the gap? Multimodal wins every time."

**Transition to Module 2**: "Great — we gave the agent its EYES. But what about medical knowledge? A doctor knows treatment guidelines by heart. Our agent needs that too."

**Students will be wowed by**: Gemini analyzing a REAL medical image

---

### Module 2 — RAG (20 min)
**Hook**: "AI that makes up medical facts can KILL people. RAG ensures every answer has a source."

**Key moments**:
1. Build ChromaDB knowledge base in < 10 seconds
2. Show semantic search: "heart attack treatment" matches "STEMI management"
3. RAG answer with [1][2] citations vs hallucinated answer
4. "WITHOUT RAG, the LLM said cinnamon cures diabetes. WITH RAG, it cites ADA 2024."

**Transition to Module 3**: "We now have the eyes AND the memory. Time to build the BRAIN — an agent that uses BOTH of these as tools."

**Show the architecture diagram**: students love seeing the full pipeline

---

### Module 3 — Agent (30 min) ⭐ CENTERPIECE
**Hook**: "We just built the eyes (multimodal) and the memory (RAG). Now we build the BRAIN."

**Key moments** (this is where students gasp):
1. Define 7 hospital tools as Python functions — **including** `analyze_patient_xray` (Module 1) and `search_medical_knowledge` (Module 2)
2. Tell students: "Two of these tools are the SAME capabilities we just built!"
3. Give them to Gemini → send an emergency
4. **WATCH the LLM autonomously**: check_beds → get_vitals → **analyze_xray** → **search_guidelines** → assign_bed → alert_staff
5. "Nobody told it to call these tools in this order. The LLM DECIDED."
6. "And look — it used our multimodal vision AND our RAG knowledge base!"
7. Show human-in-the-loop: "PENDING_PHYSICIAN_APPROVAL"

**Transition to Module 4**: "OK, this agent is impressive. But before we ship it — can we TRUST it? Does it treat all patients equally? Let's find out."

**Pause for Q&A here** — students will have many questions about function calling

---

### Module 4 — Bias (20 min)
**Hook**: "Our agent looks smart. But can we TRUST it? Let's find out."

**Key moments**:
1. Overall accuracy 70%+ → "Looks fine, right?"
2. BOOM — per-group breakdown shows 10%+ gap
3. AIF360 metrics: "These are what FDA actually checks"
4. SHAP explanations: "The AI flagged this patient because of comorbidities, not race"

**Transition to Module 5**: "We found bias and we can detect it. But what OTHER things can go wrong? Let me show you some real horror stories."

---

### Module 5 — Safety (15 min)
**Hook**: "Every failure I'm about to show you happened at a MAJOR institution."

**Key moments**:
1. IBM Watson, Optum, Epic — real stories, real consequences
2. **Live guardrails**: feed unsafe output → watch it get BLOCKED
3. Safe vs unsafe: same model, different system prompt → completely different behavior
4. Regulatory update: India's SAHI framework + CDSCO now classifies AI as medical devices

---

## 🎤 Closing Script (1:55–2:00)

> *"Let's step back and see what we built today:*
>
> *We built an AI that can SEE medical images, REMEMBER treatment guidelines from real sources, REASON autonomously about what to do in an emergency, and we learned how to CHECK it for fairness and PROTECT patients with guardrails.*
>
> *This is not science fiction. Companies like Qure.ai right here in India are doing exactly this — their AI reads chest X-rays in rural hospitals where there's no radiologist. Google's AMIE agent can hold diagnostic conversations. And all of them need the bias detection and safety guardrails we covered.*
>
> *If any of this excites you: the field is WIDE OPEN. Companies are hiring — I've shared a resources document with learning paths, datasets, and career information. Build a project, put it on GitHub, write about it on LinkedIn. That's how you get started.*
>
> *Thank you for being part of this workshop series. Now go build something amazing."*

---

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| API key rate limit (15 RPM) | Switch to `WORKSHOP_BACKEND=ollama` in `.env`. Or wait 60 seconds. |
| ChromaDB install fails | Module 2 shows concept (still runs). Module 3 falls back to keyword matching. |
| Module 3 hangs | LLM is thinking — wait 15 seconds (multi-tool chains take time) |
| SHAP crashes | Falls back to feature_importances_ (built-in sklearn) |
| AIF360 can't install | Module 4 shows metrics conceptually without AIF360 |
| ALL modules fail | Every module has Demo Mode with pre-recorded output |
| sample_chest_xray.png missing | Module 1 skips image analysis; Module 3 returns demo output |
| Sentence-transformers slow | First download of all-MiniLM-L6-v2 takes ~1 min, then cached |
| Ollama model not found | Run `ollama pull dcarrascosa/medgemma-1.5-4b-it:Q8_0` |

---

## 💼 Career Discussion (5 min)

| Role | Salary (India) | Companies |
|------|----------------|-----------|
| Healthcare AI Engineer | ₹8–25 LPA | Qure.ai, Niramai, SigTuple |
| ML Engineer (Healthcare) | ₹10–30 LPA | Google Health, Microsoft |
| Agentic AI Developer | ₹12–35 LPA | TCS, Infosys, Wipro AI labs |
| AI Product Manager | ₹15–50 LPA | Practo, 1mg, HealthifyMe |

Share `STUDENT_RESOURCES.md` in the Teams chat after the workshop.

---

## ❓ Common Student Questions

| Question | Answer |
|----------|--------|
| **"Is this replacing doctors?"** | "No! It's augmenting them. AI proposes, doctors decide. Always." |
| **"I didn't attend Workshop 1 & 2?"** | "You'll still learn a lot! We'll recap key concepts." |
| **"Can I run this on my laptop?"** | "Yes! Everything runs locally or free via Google Colab / Gemini API." |
| **"Is this only for CS students?"** | "No! Healthcare/biotech students bring domain expertise that engineers lack." |
| **"What about patient privacy?"** | "Covered in Module 5. We show local Ollama models for hospital-private deployment." |
| **"How do I get a job in this?"** | "Build a project, upload to GitHub, post on LinkedIn. Companies listed in STUDENT_RESOURCES.md." |
| **"Is this how real agents work?"** | "Yes! Google, Microsoft, Amazon all use this exact LLM + function calling pattern for healthcare agents." |

---

## ⚠️ SDK Note

This code uses the **new `google-genai` SDK** (v1.68+), which is the current recommended SDK from Google (March 2026). The old `google-generativeai` package is deprecated.
```python
# Current SDK pattern (what we use):
from google import genai
client = genai.Client()  # Auto-detects GEMINI_API_KEY
response = client.models.generate_content(model="gemini-2.5-flash", contents="...")
```

---

## 📚 Resources to Share After Workshop

→ Share `STUDENT_RESOURCES.md` in the Teams chat. It contains:
- Free learning paths (Fast.ai, DeepLearning.AI, Hugging Face)
- Open datasets (MIMIC-III, ChestX-ray14, PubMed)
- Career information + Indian AI companies
- Regulatory frameworks

---

## 🎓 Workshop Series Progression

```
Workshop 1: "See AI" (Exploration)
├── GenAI fundamentals, text & image generation
└── Understanding transformers

Workshop 2: "Create AI" (Engineering)
├── Local models (Ollama), professional project structure
├── RAG pipelines, medical summarization
└── Synthetic data generation

Workshop 3: "Act Like AI Agents" (Production) ← YOU ARE HERE
├── Gemini multimodal medical analysis  (the eyes)
├── Vector RAG with ChromaDB             (the memory)
├── ⭐ Gemini function calling agents    (the brain)
├── AIF360 fairness metrics              (the conscience)
└── Safety guardrails & regulations      (the safety net)
```

---

## 📁 Files

```
workshop_3/
├── workshop_config.py              # ← Shared backend selector (Gemini/Ollama/Demo)
├── 01_multimodal_medical_ai.py      # Multimodal (image + text)
├── 02_medical_rag_frontier.py       # ChromaDB + sentence-transformers + LLM
├── 03_healthcare_agent_frontier.py  # ⭐ Function calling agent (integrated!)
├── 04_bias_and_fairness.py          # sklearn + SHAP + AIF360
├── 05_safety_and_guardrails.py      # Guardrails + case studies + regs
├── sample_chest_xray.png            # Sample medical image for Modules 1 & 3
├── .env                             # API key + WORKSHOP_BACKEND config
├── requirements.txt                 # All dependencies
├── README.md                        # Quick-start guide
├── STUDENT_RESOURCES.md             # Post-workshop handout
└── INSTRUCTOR_GUIDE_v3.md           # ← This file
```
