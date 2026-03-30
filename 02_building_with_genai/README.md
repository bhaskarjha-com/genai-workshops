# 🛠️ Workshop 2: Building with GenAI

> **Theme:** *"From consuming AI to building real applications"*

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/bhaskarjha-com/genai-workshops/blob/main/02_building_with_genai/Workshop_2_Advanced_GenAI.ipynb)

**Format:** Google Colab Notebook + optional Agent Programming Guide
**Estimated Time:** ~2 hours (self-paced)

---

## 🎯 Learning Objectives

By the end of this workshop, you will be able to:

- ✅ **Set up** a professional GenAI project structure
- ✅ **Generate images** from text using FLUX diffusion models
- ✅ **Compare** cloud vs local AI and understand when to use each
- ✅ **Build a RAG pipeline** — embeddings, vector store, semantic retrieval
- ✅ **Build a mini AI agent** with tool-calling (ReAct pattern)
- ✅ **Add custom tools** to extend your agent's capabilities

---

## 📋 Prerequisites

- ✅ Completed **[Workshop 1](../01_genai_fundamentals/)** (or equivalent knowledge)
- ✅ A **Google Account** (for Google Colab)
- ✅ **Basic Python** familiarity
- ❌ No GPU required, no API keys needed

---

## 🚀 Quick Start

### Option A: Google Colab (Recommended)
1. Click the **"Open in Colab"** badge above
2. Run cells sequentially with `Shift + Enter`

### Option B: Local Jupyter
```bash
pip install -r requirements.txt
jupyter notebook Workshop_2_Advanced_GenAI.ipynb
```

---

## 📂 Files

| File | Purpose |
|------|---------|
| `Workshop_2_Advanced_GenAI.ipynb` | 📓 The main workshop notebook — run this |
| `Agent_Programming_Guide.ipynb` | 🤖 Deep-dive: build a complete ReAct agent with Ollama |
| `requirements.txt` | Python dependencies (for local setup) |
| `guides/INSTRUCTOR_GUIDE.md` | 👨‍🏫 Teaching guide with timing and troubleshooting |
| `guides/RESOURCES.md` | 📚 Curated learning resources |

---

## 📖 Workshop Outline

| # | Section | What You'll Build | Time |
|:-:|---------|-------------------|:----:|
| 1 | Project Structure | Professional GenAI project scaffold (live in Colab) | 10 min |
| 2 | Image Generation | AI images from text using FLUX API | 25 min |
| 3 | Local vs Cloud | Compare model deployment approaches | 10 min |
| 4 | RAG Pipeline | Semantic search + answer engine with FAISS | 25 min |
| 5 | Mini AI Agent | Agent with calculator, weather, and knowledge tools | 15 min |
| — | Wrap-Up | Review + bridge to Workshop 3 | 5 min |

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| FLUX API "GPU quota exceeded" | Free tier is busy — wait a few minutes and retry. Code is correct. |
| "ModuleNotFoundError" | Re-run the `!pip install` cells |
| RAG gives poor answers | Expected with GPT-2 fallback. Run in Colab for Gemini-powered answers. |
| Image won't display | Try `display(IPImage(filename=path))` after generating |

---

## ➡️ What's Next?

### Immediate: Agent Programming Guide
Open `Agent_Programming_Guide.ipynb` for a deep-dive into building complete ReAct agents with Ollama.

### Next Workshop
Continue to **[Workshop 3: Healthcare AI Agent](../03_healthcare_ai_agent/)** where you'll build an autonomous agent that analyzes X-rays, searches medical guidelines, and manages hospital resources.
