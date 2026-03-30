# 🧬 GenAI Workshops

> **Hands-on Generative AI workshops — from fundamentals to autonomous agents.**
> Tokenization, prompt engineering, image generation, RAG, AI agents, bias detection, and safety guardrails.
> Fully self-paced. Runs anywhere: cloud, local GPU, or fully offline.

[![Workshop 1 - Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/bhaskarjha-com/genai-workshops/blob/main/01_genai_fundamentals/Workshop_1_GenAI_Fundamentals.ipynb)
[![Workshop 2 - Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/bhaskarjha-com/genai-workshops/blob/main/02_building_with_genai/Workshop_2_Advanced_GenAI.ipynb)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

---

## 🎯 What You'll Learn

By completing this workshop series, you will be able to:

- ✅ Explain how **LLMs, Transformers, and diffusion models** work
- ✅ **Tokenize text** and understand how AI reads language
- ✅ **Generate text and images** using open-source AI models
- ✅ Apply **prompt engineering** techniques for better AI output
- ✅ Build **RAG pipelines** with vector embeddings and semantic retrieval
- ✅ Build **AI agents** with tool-calling (ReAct pattern)
- ✅ Run **local LLMs** with Ollama (zero cloud dependency)
- ✅ Detect and mitigate **bias in ML models** using AIF360
- ✅ Implement **safety guardrails** on AI outputs

---

## 🗺️ Workshop Series

| # | Workshop | What You'll Build | Format | Time |
|:-:|---------|-------------------|--------|:----:|
| 1 | **[GenAI Fundamentals](./01_genai_fundamentals/)** | Tokenizer, text generator, prompt lab, local-vs-cloud comparison | Colab Notebook | ~90 min |
| 2 | **[Building with GenAI](./02_building_with_genai/)** | Image generator, RAG pipeline, mini AI agent with tools | Colab Notebook | ~2 hrs |
| 3 | **[Healthcare AI Agent](./03_healthcare_ai_agent/)** | Autonomous healthcare agent with vision, RAG, bias detection, safety | Python Scripts | ~2 hrs |

---

## 🚀 Quick Start

Each workshop is **self-contained**. Clone the repo and pick any workshop:

```bash
git clone https://github.com/bhaskarjha-com/genai-workshops.git
cd genai-workshops

# Workshop 1 or 2: Open notebook in Google Colab or Jupyter
cd 01_genai_fundamentals
# Open Workshop_1_GenAI_Fundamentals.ipynb in Colab

# Workshop 3: Run Python scripts directly
cd 03_healthcare_ai_agent
pip install -r requirements.txt
python 01_multimodal_medical_ai.py
```

> **No GPU? No API key?** Workshops 1 & 2 run on free Colab GPUs. Workshop 3 has a **Demo Mode** that works fully offline with pre-recorded outputs.

---

## 🏗️ Learning Path

```
┌────────────────────────┐    ┌────────────────────────┐    ┌──────────────────────────┐
│  01  FUNDAMENTALS       │    │  02  BUILDING           │    │  03  HEALTHCARE AGENT     │
│                        │    │                        │    │                          │
│  • Transformers        │    │  • Image generation    │    │  • Multimodal vision     │
│  • Tokenization  ★     │───▶│  • RAG pipelines  ★    │───▶│  • Autonomous agents  ⭐  │
│  • Text generation     │    │  • Mini AI agent  ★    │    │  • Bias & fairness       │
│  • Prompt engineering  │    │  • Local vs cloud      │    │  • Safety guardrails     │
│  • Local vs cloud      │    │                        │    │                          │
└────────────────────────┘    └────────────────────────┘    └──────────────────────────┘
     Foundations                   Applications                 Production-Grade
```

**Recommended order:** 1 → 2 → 3 (each builds on the previous).
**Can I skip?** Yes — each workshop has its own README with prerequisites.

---

## 📋 Prerequisites

| Requirement | Workshop 1 | Workshop 2 | Workshop 3 |
|-------------|:----------:|:----------:|:----------:|
| Python 3.10+ | ✅ (via Colab) | ✅ (via Colab) | ✅ (local) |
| Google Account | ✅ | ✅ | Optional |
| GPU | ❌ Free Colab GPU | ❌ Free Colab GPU | Optional (demo mode) |
| Ollama | ❌ | Optional | Optional |
| API Key | ❌ | ❌ | Optional (free Gemini) |
| Prior AI knowledge | ❌ None | Workshop 1 | Workshops 1 & 2 |

---

## 👨‍🏫 For Instructors

Each workshop includes a `guides/` folder with ready-to-use teaching materials:

| File | What It Contains |
|------|-----------------|
| `INSTRUCTOR_GUIDE.md` | Timeline, teaching hooks, Q&A prep, emergency procedures |
| `PRESENTATION_SCRIPT.md` | Minute-by-minute delivery script (Workshop 3) |
| `RESOURCES.md` / `STUDENT_RESOURCES.md` | Curated post-workshop learning paths |

**Delivery modes:**
- 🎓 **Live workshop:** Follow the instructor guide, share screen, run code together
- 📖 **Self-paced:** Students follow the README and run cells/scripts independently
- 📋 **Demo mode (W3):** Pre-recorded outputs, works without any API keys or GPU

---

## 🏗️ Repository Structure

```
genai-workshops/
├── README.md                    ← You are here
├── LICENSE                      (MIT)
├── CONTRIBUTING.md
├── CHANGELOG.md
├── .gitignore
│
├── 01_genai_fundamentals/
│   ├── README.md                Student guide
│   ├── requirements.txt
│   ├── Workshop_1_GenAI_Fundamentals.ipynb
│   └── guides/
│       ├── INSTRUCTOR_GUIDE.md
│       └── RESOURCES.md
│
├── 02_building_with_genai/
│   ├── README.md                Student guide
│   ├── requirements.txt
│   ├── Workshop_2_Advanced_GenAI.ipynb
│   ├── Running_Local_Models_Deep_Dive.ipynb
│   ├── Agent_Programming_Guide.ipynb
│   └── guides/
│       ├── INSTRUCTOR_GUIDE.md
│       └── RESOURCES.md
│
└── 03_healthcare_ai_agent/
    ├── README.md                Student guide
    ├── requirements.txt
    ├── .env.example
    ├── workshop_config.py
    ├── 01_multimodal_medical_ai.py
    ├── 02_medical_rag_frontier.py
    ├── 03_healthcare_agent_frontier.py
    ├── 04_bias_and_fairness.py
    ├── 05_safety_and_guardrails.py
    ├── sample_chest_xray.png
    └── guides/
        ├── INSTRUCTOR_GUIDE.md
        ├── PRESENTATION_SCRIPT.md
        └── STUDENT_RESOURCES.md
```

---

## ⚠️ Disclaimer

This is educational material. Healthcare scenarios in Workshop 3 use **simulated data** for teaching purposes. **Not a medical device. Not for clinical use.**

---

## 🤝 Contributing

Found a bug? Have a suggestion? See [CONTRIBUTING.md](./CONTRIBUTING.md).

---

## 📄 License

[MIT License](./LICENSE) — free to use, modify, and distribute.

---

## 🙏 Acknowledgements

Created by **Bhaskar Jha** for the VIT University (BMESI & BMSA × IIIC) workshop series on Generative AI, 2026.

Built with: [Hugging Face](https://huggingface.co) · [Google Gemini](https://ai.google.dev) · [Ollama](https://ollama.com) · [ChromaDB](https://www.trychroma.com) · [IBM AIF360](https://aif360.res.ibm.com)
