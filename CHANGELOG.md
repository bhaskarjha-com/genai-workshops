# Changelog

All notable changes to this workshop series will be documented in this file.

## [2.0.0] — 2026-03-30

### 🔄 Deep Content Overhaul

**Renamed workshops** for clarity:
- `workshop_1_see_ai/` → `01_genai_fundamentals/`
- `workshop_2_create_ai/` → `02_building_with_genai/`
- `workshop_3_agentic_ai/` → `03_healthcare_ai_agent/`

**Workshop 1 — GenAI Fundamentals:**
- NEW: Tokenization demo (see how AI reads text as sub-word tokens)
- NEW: Prompt engineering lab (vague vs specific vs role-based prompts)
- NEW: Local vs Cloud comparison (GPT-2 vs Gemini side-by-side)
- Trimmed "See AI Magic" link list to 3 curated tools
- Updated section numbering to 8 proper sections

**Workshop 2 — Building with GenAI:**
- NEW: Project structure cell now creates real directories in Colab
- NEW: Local model Python demo (Ollama pattern + Colab AI)
- NEW: Mini AI agent with 3 working tools (calculator, weather, RAG search)
- NEW: Agent exercise — add your own tool
- Upgraded RAG to use Gemini (via google.colab.ai) with GPT-2 fallback
- Removed phantom "Section 6: Healthcare AI" from table of contents

**Workshop 3 — Healthcare AI Agent:**
- Added "Quick Recap" bridge section for students resuming after a break
- Updated all cross-references to new folder names

**All workshops:**
- Updated root README with new names, learning path, and descriptions
- Updated all cross-workshop links

---

## [1.0.0] — 2026-03-30

### 🎉 Initial Public Release

**Workshop 1: GenAI Fundamentals**
- GenAI landscape exploration (3D, video, music, agent tools)
- Transformer architecture explained (tokenization, attention, parameters)
- Hands-on GPT-2 text generation with Hugging Face
- Temperature experiments and story generation

**Workshop 2: Building with GenAI**
- Professional project structure for GenAI apps
- Image generation with FLUX API via Gradio
- Local LLM deployment with Ollama
- RAG pipeline: embeddings → FAISS → retrieval → generation
- Agent architecture theory (Brain, Tools, Memory, Planning)
- Bonus: Agent Programming Guide notebook

**Workshop 3: Healthcare AI Agent**
- Multimodal medical analysis (Gemini / MedGemma)
- Healthcare RAG with ChromaDB + sentence-transformers
- Autonomous agent with 7 hospital tools (function calling)
- Bias detection with AIF360 + SHAP explanations
- Safety guardrails and regulatory frameworks
- 3-tier backend: Gemini Cloud → Ollama Local → Demo Mode

### Repository
- Standardized structure: README + requirements + guides/ per workshop
- Open in Colab badges for Workshops 1 & 2
- Instructor guides with minute-by-minute scripts
- MIT License, Contributing guidelines
