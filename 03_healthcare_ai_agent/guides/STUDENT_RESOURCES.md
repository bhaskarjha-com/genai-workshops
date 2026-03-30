# 📚 Workshop 3 — Post-Workshop Resources

**Agentic AI in Healthcare**  
*Share this with students after the workshop.*

---

## 🎯 What You Learned Today

| Module | Concept | Industry Equivalent |
|--------|---------|-------------------|
| **Multimodal AI** | LLMs that see images + read text | Google Med-PaLM M, BiomedCLIP |
| **Vector RAG** | Semantic retrieval + cited answers | Every production LLM app |
| **Agentic AI** | LLM autonomously calls tools | Microsoft Healthcare Agent, AMIE |
| **Bias Detection** | AIF360 fairness metrics | FDA regulatory requirement |
| **Guardrails** | Safety layers on AI output | Required for any medical AI deployment |

---

## 📖 Free Learning Paths

### Beginner → Intermediate
1. **[Fast.ai Practical Deep Learning](https://fast.ai)** — Best free ML course (code-first)
2. **[DeepLearning.AI — AI for Medicine](https://www.coursera.org/specializations/ai-for-medicine)** — 3-course specialization (free to audit)
3. **[Hugging Face NLP Course](https://huggingface.co/learn/nlp-course)** — Transformers + embeddings
4. **[LangChain RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/)** — Build production RAG systems

### Healthcare AI Specific
5. **[Google Cloud Healthcare AI](https://cloud.google.com/healthcare-api)** — Production healthcare APIs
6. **[MIMIC-III Tutorials](https://mimic.mit.edu/)** — Work with real ICU patient data
7. **[Papers with Code — Medical AI](https://paperswithcode.com/area/medical)** — Latest research + code

### Agentic AI
8. **[Google Gemini Function Calling Docs](https://ai.google.dev/gemini-api/docs/function-calling)** — What we used in Module 3
9. **[Anthropic Tool Use Guide](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)** — Same pattern, different provider
10. **[LangGraph Agents](https://langchain-ai.github.io/langgraph/)** — Multi-agent frameworks

---

## 📊 Open Datasets to Practice With

| Dataset | What It Contains | Access |
|---------|-----------------|--------|
| **MIMIC-III** | 40K+ ICU patient records | [PhysioNet](https://physionet.org/content/mimiciii/) (free, requires training) |
| **ChestX-ray14** | 112K chest X-rays with labels | [NIH](https://nihcc.app.box.com/v/ChestXray-NIHCC) |
| **PubMed** | 35M+ medical abstracts | [pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/) |
| **UK Biobank** | 500K participants, health data | [ukbiobank.ac.uk](https://www.ukbiobank.ac.uk/) |
| **PhysioNet** | ECG, EEG, physiological signals | [physionet.org](https://physionet.org/) |

---

## 💼 Career Paths in Healthcare AI (India, 2026)

| Role | Salary Range | Who's Hiring |
|------|-------------|-------------|
| Healthcare AI Engineer | ₹8–25 LPA | Qure.ai, Niramai, SigTuple, Predible |
| ML Engineer (Healthcare) | ₹10–30 LPA | Google Health, Microsoft, Amazon |
| Agentic AI Developer | ₹12–35 LPA | TCS, Infosys, Wipro AI Labs, startups |
| AI Product Manager (Health) | ₹15–50 LPA | Practo, 1mg, PharmEasy, HealthifyMe |
| Clinical AI Researcher | ₹8–20 LPA | AIIMS, IITs, research labs |
| AI Ethics & Governance | ₹10–25 LPA | NASSCOM, consulting firms, govt |

### How to Break In
1. **Build a project** — Use today's code as a starting point, extend it
2. **Pick a dataset** — MIMIC-III or ChestX-ray14, build something real
3. **Write about it** — Blog post on Medium or LinkedIn
4. **Upload to GitHub** — Public repo with good README
5. **Apply broadly** — AI startups are hiring across India

---

## 🏥 Indian Healthcare AI Companies

| Company | What They Do | Location |
|---------|-------------|----------|
| **Qure.ai** | AI for radiology (X-ray, CT analysis) | Mumbai |
| **Niramai** | AI breast cancer screening (thermal imaging) | Bangalore |
| **SigTuple** | AI for pathology (blood, urine analysis) | Bangalore |
| **Predible** | AI radiology (cardiac CT, liver) | Bangalore |
| **Tricog** | AI ECG analysis for heart attacks | Bangalore |
| **Wysa** | AI mental health chatbot | Bangalore |

---

## 🔗 Communities to Join

- **Healthcare AI India** — LinkedIn group (~10K members)
- **r/MachineLearning** — Reddit (800K+ members)
- **Kaggle Healthcare Competitions** — Practice with real problems
- **Papers with Code** — See latest medical AI papers with implementation
- **Hugging Face** — Medical model hub (BiomedCLIP, MedGemma, etc.)

---

## 📋 Regulatory Frameworks to Know

| Framework | What It Covers |
|-----------|---------------|
| **FDA AI/ML SaMD** | US medical AI device approval |
| **EU AI Act 2025** | Healthcare AI = "high-risk" → mandatory audit |
| **DPDP Act 2023** | India's data protection law (₹250 Cr penalties) |
| **CDSCO + SAHI 2026** | AI diagnostic software = Class C medical device |
| **ABDM/ABHA** | India's digital health infrastructure |

---

## 🛠️ Tools & Frameworks from Today's Workshop

```bash
# Install everything we used
pip install google-genai chromadb sentence-transformers shap aif360 python-dotenv ollama

# For local deployment (no cloud needed)
# Install Ollama: https://ollama.com/download
ollama pull dcarrascosa/medgemma-1.5-4b-it:Q8_0    # Medical multimodal model (vision + text)
ollama pull qwen3:8b                                 # Tool-calling model for agent orchestration

# Switch between cloud and local:
# Set WORKSHOP_BACKEND=gemini (or ollama, or demo) in .env
```

---

*Created by Bhaskar Jha | Originally delivered at VIT University*
