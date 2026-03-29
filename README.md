# 🧬 GenAI Workshops

> **Hands-on Generative AI workshops — from fundamentals to autonomous agents.**
> Multimodal vision, RAG, AI agents, bias detection, and safety guardrails.
> Fully self-paced. Runs anywhere: cloud, local GPU, or fully offline.

[![Workshop 1 - Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/bhaskarjha-com/genai-workshops/blob/main/workshop_1_see_ai/Workshop_1_GenAI_Fundamentals.ipynb)
[![Workshop 2 - Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/bhaskarjha-com/genai-workshops/blob/main/workshop_2_create_ai/Workshop_2_Advanced_GenAI.ipynb)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

---

## 🎯 What You'll Learn

By completing this workshop series, you will be able to:

- ✅ Explain how **LLMs, Transformers, and diffusion models** work
- ✅ **Generate text and images** using open-source AI models
- ✅ Build **RAG pipelines** with vector embeddings and semantic retrieval
- ✅ Run **local LLMs** with Ollama (zero cloud dependency)
- ✅ Build **autonomous AI agents** with tool-calling and memory
- ✅ Detect and mitigate **bias in ML models** using AIF360
- ✅ Implement **safety guardrails** on AI outputs

---

## 🗺️ Workshop Series

| # | Workshop | Theme | Format | Time | Key Topics |
|:-:|---------|-------|--------|:----:|------------|
| 1 | **[See AI](./workshop_1_see_ai/)** | See the magic, understand the mechanism | Colab Notebook | ~90 min | GenAI landscape, Transformers, GPT-2 text generation |
| 2 | **[Create AI](./workshop_2_create_ai/)** | From consuming AI to building with it | Colab Notebook | ~2 hrs | FLUX images, Ollama, RAG pipelines, agent architecture |
| 3 | **[Agentic AI](./workshop_3_agentic_ai/)** | Build an autonomous healthcare AI agent | Python Scripts | ~2 hrs | Multimodal AI, RAG, function-calling agents, bias, safety |

---

## 🚀 Quick Start

Each workshop is **self-contained**. Clone the repo and pick any workshop:

```bash
git clone https://github.com/bhaskarjha-com/genai-workshops.git
cd genai-workshops

# Workshop 1 or 2: Open notebook in Google Colab or Jupyter
cd workshop_1_see_ai
# Open Workshop_1_GenAI_Fundamentals.ipynb in Colab

# Workshop 3: Run Python scripts directly
cd workshop_3_agentic_ai
pip install -r requirements.txt
python 01_multimodal_medical_ai.py
```

> **No GPU? No API key?** Workshops 1 & 2 run on free Colab GPUs. Workshop 3 has a **Demo Mode** that works fully offline with pre-recorded outputs.

---

## 🏗️ Learning Path

```
┌─────────────────────┐     ┌─────────────────────┐     ┌──────────────────────────┐
│  Workshop 1          │     │  Workshop 2          │     │  Workshop 3               │
│  👁️  SEE AI          │────▶│  🛠️  CREATE AI       │────▶│  🤖  AGENTIC AI           │
│                     │     │                     │     │                          │
│  • GenAI landscape  │     │  • Image generation │     │  • Multimodal vision     │
│  • Transformers     │     │  • Local LLMs       │     │  • Healthcare RAG        │
│  • GPT-2 hands-on   │     │  • RAG pipelines    │     │  • Autonomous agents  ⭐  │
│  • Prompt basics    │     │  • Agent concepts   │     │  • Bias & fairness       │
│                     │     │                     │     │  • Safety guardrails     │
└─────────────────────┘     └─────────────────────┘     └──────────────────────────┘
     Foundations                 Applications                Production-Grade
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
├── .gitignore
│
├── workshop_1_see_ai/
│   ├── README.md                Student guide
│   ├── requirements.txt
│   ├── Workshop_1_GenAI_Fundamentals.ipynb
│   └── guides/
│       ├── INSTRUCTOR_GUIDE.md
│       └── RESOURCES.md
│
├── workshop_2_create_ai/
│   ├── README.md                Student guide
│   ├── requirements.txt
│   ├── Workshop_2_Advanced_GenAI.ipynb
│   ├── Agent_Programming_Guide.ipynb
│   └── guides/
│       ├── INSTRUCTOR_GUIDE.md
│       └── RESOURCES.md
│
└── workshop_3_agentic_ai/
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
