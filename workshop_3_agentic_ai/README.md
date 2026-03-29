# 🤖 Workshop 3: Agentic AI — Autonomous Healthcare Agents

> **Theme:** *"Build an autonomous AI agent that sees, remembers, thinks, and acts"*

**Format:** Python scripts (terminal-based, each module is self-contained)
**Estimated Time:** ~2 hours (self-paced)

---

## 🎯 Learning Objectives

By the end of this workshop, you will be able to:

- ✅ **Build multimodal AI** that analyzes medical images + text simultaneously
- ✅ **Construct a RAG pipeline** with ChromaDB for semantic medical knowledge retrieval
- ✅ **Create an autonomous agent** that uses function calling to chain tools without human intervention
- ✅ **Detect bias** in ML models using SHAP explainability and IBM AIF360 fairness metrics
- ✅ **Implement guardrails** on AI output for safe, responsible medical AI deployment
- ✅ **Understand three-tier resilience**: graceful degradation from cloud → local GPU → demo mode

---

## 📋 Prerequisites

- ✅ Completed **[Workshop 1](../workshop_1_see_ai/)** and **[Workshop 2](../workshop_2_create_ai/)** (or equivalent)
- ✅ Python 3.10+ installed locally
- ✅ Basic understanding of LLMs, embeddings, and RAG
- 🔧 **(Optional)** [Gemini API key](https://aistudio.google.com/apikey) (free) for cloud backend
- 🔧 **(Optional)** [Ollama](https://ollama.com) + GPU for local backend

> **No API key? No GPU?** Every module runs in **Demo Mode** with pre-recorded outputs — always works.

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Choose Your Backend

| Backend | Setup | Best For |
|---------|-------|----------|
| **☁️ Gemini** (cloud) | Set `GEMINI_API_KEY` in `.env` ([get free key](https://aistudio.google.com/apikey)) | Best quality, live demo |
| **🖥️ Ollama** (local GPU) | `ollama pull dcarrascosa/medgemma-1.5-4b-it:Q8_0` | Offline, privacy-first |
| **📋 Demo** (pre-recorded) | No setup needed | Fallback, works anywhere |

Create your `.env` file from the template:
```bash
cp .env.example .env
# Edit .env with your settings
```

### 3. Run All Modules
```bash
python 01_multimodal_medical_ai.py     # 👁️ "The Eyes" — vision + text
python 02_medical_rag_frontier.py      # 🧠 "The Memory" — vector RAG
python 03_healthcare_agent_frontier.py # ⭐ "The Brain" — autonomous agent
python 04_bias_and_fairness.py         # ⚖️ "The Conscience" — bias detection
python 05_safety_and_guardrails.py     # 🛡️ "The Safety Net" — guardrails
```

---

## 📂 Files

| File | Purpose | Duration |
|------|---------|----------|
| `workshop_config.py` | Shared backend selector — all modules import this | — |
| `01_multimodal_medical_ai.py` | LLM analyzes X-ray images + text symptoms → diagnosis | 20 min |
| `02_medical_rag_frontier.py` | RAG: embed articles, semantic retrieval, cited answers | 20 min |
| `03_healthcare_agent_frontier.py` | ⭐ LLM autonomously calls hospital tools (function calling) | 30 min |
| `04_bias_and_fairness.py` | Bias detection, AIF360 fairness metrics, SHAP explainability | 20 min |
| `05_safety_and_guardrails.py` | Guardrails on AI output, case studies, regulatory landscape | 15 min |
| `sample_chest_xray.png` | Sample medical image for Module 1 & 3 multimodal demos | — |
| `.env.example` | Environment config template (API key, backend selection) | — |

### Instructor Materials (in `guides/`)

| File | Purpose |
|------|---------|
| `guides/INSTRUCTOR_GUIDE.md` | Complete teaching guide with timing, scripts, and Q&A prep |
| `guides/PRESENTATION_SCRIPT.md` | Minute-by-minute delivery script (~30 pages) |
| `guides/STUDENT_RESOURCES.md` | Post-workshop: courses, datasets, career paths |

---

## 🧠 Workshop Narrative

```
Module 1: "The Eyes"       → Multimodal vision (X-ray + text + vitals)
Module 2: "The Memory"     → RAG knowledge base (vector retrieval + citations)
Module 3: "The Brain"  ⭐  → Agent that USES both as tools + hospital management
Module 4: "The Conscience" → Can we trust it? Bias detection + fairness
Module 5: "The Safety Net" → Guardrails, case studies, regulations
```

The agent in Module 3 genuinely calls `analyze_patient_xray()` (Module 1's approach) and `search_medical_knowledge()` (Module 2's RAG pipeline) as tools — demonstrating how Modules 1 & 2 become building blocks for the autonomous agent.

---

## 🔧 Tech Stack

| Component | Technology |
|-----------|-----------|
| Cloud LLM | Gemini 2.5 Flash (`google-genai` SDK) |
| Local LLM (vision/text) | MedGemma 1.5 4B via Ollama |
| Local LLM (tool calling) | Qwen3 8B via Ollama |
| Backend config | `workshop_config.py` (auto-selects Gemini/Ollama/Demo) |
| Multimodal | Gemini Vision API or MedGemma vision |
| Vector DB | ChromaDB (in-memory) |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Fairness | IBM AIF360 + SHAP |
| Function calling | Gemini auto-calling / Ollama manual tool-call loop |

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| "No module named google.genai" | `pip install google-genai` |
| Gemini API key invalid | Get a free key from [aistudio.google.com](https://aistudio.google.com/apikey) |
| Ollama connection refused | Start Ollama: `ollama serve` |
| Module 3 agent loops forever | Set `WORKSHOP_BACKEND=demo` in `.env` |
| Module 4 AIF360 install error | `pip install aif360 --no-deps` then install deps manually |
| SHAP slow on large datasets | Expected — runs on synthetic data, takes 1-2 min |
| "PIL not found" error | `pip install Pillow` |

---

## 📝 Notes

- **Three-tier resilience**: Gemini → Ollama → Demo Mode. If one fails, fall to the next.
- **Backend selection**: Set `WORKSHOP_BACKEND` in `.env` or get an interactive prompt.
- **Ollama local**: MedGemma 1.5 4B needs ~5 GB VRAM for vision. Qwen3 8B needs ~6 GB for tool calling.
- **Module 4**: Fully offline (sklearn/SHAP/AIF360) — no LLM needed.
- **Google Colab**: All code runs on Colab — install requirements and set API key in Colab secrets.

---

## ⚠️ Disclaimer

This workshop uses **simulated medical scenarios** for educational purposes. The AI models, diagnoses, and patient data are synthetic demonstrations. **This is not a medical device and must not be used for clinical decision-making.**

---

## ⬅️ Previous Workshops

- **[Workshop 1: See AI](../workshop_1_see_ai/)** — GenAI fundamentals, Transformers, text generation
- **[Workshop 2: Create AI](../workshop_2_create_ai/)** — Image generation, local models, RAG pipelines
