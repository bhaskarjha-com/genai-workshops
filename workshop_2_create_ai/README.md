# 🛠️ Workshop 2: Create AI — Building GenAI Applications

> **Theme:** *"From consuming AI to building with it"*

**Format:** Google Colab Notebook + optional local Jupyter
**Estimated Time:** ~2 hours (self-paced)

---

## 🎯 Learning Objectives

By the end of this workshop, you will be able to:

- ✅ **Structure** a professional GenAI project with proper file organization, `.env` management, and dependencies
- ✅ **Generate images** using FLUX diffusion models via Gradio API
- ✅ **Run local LLMs** with Ollama — no cloud dependency, full privacy
- ✅ **Build a RAG pipeline** with vector embeddings (FAISS) and semantic retrieval
- ✅ **Understand agent architecture** — brain (LLM), tools, memory, and planning

This workshop also includes a **bonus notebook** — the `Agent_Programming_Guide.ipynb` — a complete hands-on tutorial for building ReAct-style AI agents with Ollama.

---

## 📋 Prerequisites

- ✅ Completed **[Workshop 1](../workshop_1_see_ai/)** (or equivalent GenAI fundamentals knowledge)
- ✅ Python 3.10+ and **Google Account** (for Colab)
- ✅ Basic Python (functions, classes, pip)
- 🔧 **(Optional)** [Ollama](https://ollama.com) installed locally for Sections 3 & Agent Guide

---

## 🚀 Quick Start

### Option A: Google Colab (Recommended)
1. Open [`Workshop_2_Advanced_GenAI.ipynb`](./Workshop_2_Advanced_GenAI.ipynb) in Colab
2. Run cells sequentially with `Shift + Enter`
3. All dependencies install automatically in Colab

### Option B: Local Jupyter
```bash
pip install -r requirements.txt
jupyter notebook Workshop_2_Advanced_GenAI.ipynb
```

### Bonus: Agent Programming Guide
```bash
# Requires Ollama running locally
ollama pull llama3.2
jupyter notebook Agent_Programming_Guide.ipynb
```

---

## 📂 Files

| File | Purpose |
|------|---------|
| `Workshop_2_Advanced_GenAI.ipynb` | 📓 The main workshop notebook — run this |
| `Agent_Programming_Guide.ipynb` | 🤖 **Bonus:** Complete agent tutorial (ReAct, memory, multi-tool) |
| `requirements.txt` | Python dependencies |
| `guides/INSTRUCTOR_GUIDE.md` | 👨‍🏫 Teaching guide with timing and scripts |
| `guides/RESOURCES.md` | 📚 Curated learning resources |

---

## 📖 Workshop Outline

| Section | Topic | Estimated Time |
|---------|-------|---------------|
| 🏗️ Project Structure | Professional GenAI project layout, `.env`, `.gitignore` | 15 min |
| 🎨 Image Generation | How diffusion models work, generate images with FLUX API | 25 min |
| 🖥️ Local Models | Why local matters, Ollama setup, running LLMs privately | 10 min |
| 📚 RAG Pipeline | Embeddings, vector stores (FAISS), semantic retrieval + generation | 25 min |
| 🤖 Agent Architecture | Agent components: brain, tools, memory, planning (theory) | 10 min |
| 🏥 Healthcare AI Preview | Bridge to Workshop 3 — what's coming next | 10 min |

### Bonus Notebook: Agent Programming Guide (~90 min)

| Part | Topic |
|------|-------|
| 📚 Understanding Agents | Agent vs LLM, core components, the agent loop |
| 🔧 Setting Up Ollama | Install, pull models, Python integration |
| 🛠️ Your First Agent | ReAct pattern, tool calling with Ollama |
| 🧠 Adding Memory | Conversation history, context management |
| 🔄 Multi-Tool Agent | Multiple tools working together |
| 🔁 Self-Reflection | Chain-of-thought, self-critique patterns |
| 🎓 Complete Project | Build a Research Assistant Agent |

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| "ModuleNotFoundError" for langchain | Run: `!pip install langchain langchain-community` |
| FLUX API "GPU quota exceeded" | Wait ~20 min or try later — it's a free shared GPU |
| Image generated but not displayed | Check the display cell uses `my_image` (not `image_path`) |
| Ollama connection refused | Make sure Ollama is running: `ollama serve` |
| FAISS install fails on Mac M1 | Use: `pip install faiss-cpu` (not `faiss-gpu`) |
| Agent notebook: "No models found" | Pull a model first: `ollama pull llama3.2` |

---

## ➡️ What's Next?

Continue to **[Workshop 3: Agentic AI](../workshop_3_agentic_ai/)** where you'll build a production-grade autonomous healthcare AI agent with multimodal vision, RAG, function calling, bias detection, and safety guardrails.
