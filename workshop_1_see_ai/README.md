# 🔍 Workshop 1: See AI — GenAI Fundamentals

> **Theme:** *"See the magic, understand the mechanism"*

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/bhaskarjha-com/genai-workshops/blob/main/workshop_1_see_ai/Workshop_1_GenAI_Fundamentals.ipynb)

**Format:** Google Colab Notebook (runs in your browser — no local install needed)
**Estimated Time:** ~90 minutes (self-paced)

---

## 🎯 Learning Objectives

By the end of this workshop, you will be able to:

- ✅ **Identify** what Generative AI is and how it differs from traditional AI
- ✅ **Explain** the Transformer architecture at a conceptual level (tokenization, attention, parameters)
- ✅ **Generate text** using GPT-2 with Hugging Face Transformers
- ✅ **Control AI output** by tuning temperature, max tokens, and sampling
- ✅ **Explore** the landscape of GenAI tools (3D, video, music, agents)

---

## 📋 Prerequisites

- ✅ A **Google Account** (for Google Colab)
- ✅ **Basic Python** familiarity (variables, functions, loops)
- ✅ A **web browser** and internet connection
- ❌ No GPU, no local install, no prior AI experience needed

---

## 🚀 Quick Start

### Option A: Google Colab (Recommended)
1. Open the notebook: [`Workshop_1_GenAI_Fundamentals.ipynb`](./Workshop_1_GenAI_Fundamentals.ipynb)
2. Click **"Open in Colab"** (or upload to Colab manually)
3. Run cells sequentially with `Shift + Enter`

### Option B: Local Jupyter
```bash
pip install -r requirements.txt
jupyter notebook Workshop_1_GenAI_Fundamentals.ipynb
```

---

## 📂 Files

| File | Purpose |
|------|---------|
| `Workshop_1_GenAI_Fundamentals.ipynb` | 📓 The main workshop notebook — run this |
| `requirements.txt` | Python dependencies (for local setup) |
| `guides/INSTRUCTOR_GUIDE.md` | 👨‍🏫 Teaching guide with timing, scripts, and troubleshooting |
| `guides/RESOURCES.md` | 📚 Curated learning resources and courses |

---

## 📖 Workshop Outline

| Section | Topic | Estimated Time |
|---------|-------|---------------|
| 👁️ See AI Magic | Explore GenAI tools: 3D models, video, music, agents | 10 min |
| 🧠 The AI Mindset | What is GenAI? How Transformers & attention work | 15 min |
| 🛠️ Environment Setup | Install Hugging Face Transformers, verify GPU | 10 min |
| 📝 Text Generation | Load GPT-2, generate text, experiment with prompts | 25 min |
| 🌡️ Temperature Lab | Compare conservative vs creative AI outputs | 10 min |
| 📖 Story Generation | Generate longer-form content with the model | 10 min |
| 🎓 Wrap-Up | Key concepts review, next steps, resources | 10 min |

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| "ModuleNotFoundError" | Re-run the `!pip install` cell at the top |
| Cell doesn't run | Check Colab shows "Connected" (top right) |
| Very slow generation | Click Runtime → Change runtime type → GPU |
| "CUDA out of memory" | Use `device=-1` (CPU mode) — already set by default |

---

## ➡️ What's Next?

When you're done, continue to **[Workshop 2: Create AI](../workshop_2_create_ai/)** where you'll build image generators, run local LLMs, and create RAG pipelines.
