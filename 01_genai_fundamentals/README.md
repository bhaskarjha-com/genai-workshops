# 🧬 Workshop 1: GenAI Fundamentals

> **Theme:** *"Understand the magic behind Generative AI"*

[![Open In Colab](https://img.shields.io/badge/Workshop_1-Open_in_Colab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/bhaskarjha-com/genai-workshops/blob/main/01_genai_fundamentals/Workshop_1_GenAI_Fundamentals.ipynb)
[![Watch Recording](https://img.shields.io/badge/Watch_Recording-YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://youtu.be/fHLQ0h8192w)

**Format:** Google Colab Notebook (runs in your browser — no local install needed)
**Estimated Time:** ~90 minutes (self-paced)
**Recording:** [▶️ Full session on YouTube](https://youtu.be/fHLQ0h8192w) — watch the instructor walk through every cell

---

## 🎯 Learning Objectives

By the end of this workshop, you will be able to:

- ✅ **Identify** what Generative AI is and how it differs from traditional AI
- ✅ **Explain** the Transformer architecture at a conceptual level (tokenization, attention, parameters)
- ✅ **Tokenize text** and see how AI reads language as number sequences
- ✅ **Generate text** using GPT-2 with Hugging Face Transformers
- ✅ **Control AI output** by tuning temperature, max tokens, and sampling
- ✅ **Apply prompt engineering** — vague vs specific vs role-based prompts
- ✅ **Compare local vs cloud AI** — GPT-2 vs Gemini side-by-side

---

## 📋 Prerequisites

- ✅ A **Google Account** (for Google Colab)
- ✅ **Basic Python** familiarity (variables, functions, loops)
- ✅ A **web browser** and internet connection
- ❌ No GPU, no local install, no prior AI experience needed

---

## 🚀 Quick Start

### Option A: Google Colab (Recommended)
1. Click the **"Open in Colab"** badge above
2. Run cells sequentially with `Shift + Enter`

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
| `guides/RESOURCES.md` | 📚 Curated learning resources, AI tools, and courses |

---

## 📖 Workshop Outline

| # | Section | What You'll Do | Time |
|:-:|---------|---------------|:----:|
| 1 | The AI Landscape | Explore 3 mind-blowing GenAI tools | 5 min |
| 2 | How GenAI Works | Understand Transformers & attention | 10 min |
| 3 | See Inside the Machine | **Tokenize text** — see how AI reads | 10 min |
| 4 | Environment Setup | Install Hugging Face, verify GPU | 5 min |
| 5 | Text Generation | Load GPT-2, generate text, experiment | 20 min |
| 6 | Temperature & Creativity | Compare conservative vs wild AI | 10 min |
| 7 | Prompt Engineering | Vague vs specific vs expert prompts | 15 min |
| 8 | Local vs Cloud AI | Compare GPT-2 with Gemini | 10 min |
| — | Wrap-Up | Key concepts review, next steps | 5 min |

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

When you're done, continue to **[Workshop 2: Building with GenAI](../02_building_with_genai/)** where you'll generate images, build RAG pipelines, and create your first AI agent.
