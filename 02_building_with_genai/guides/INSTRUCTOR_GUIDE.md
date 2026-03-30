# 🎤 Workshop 2 — Instructor Guide

> **Title:** "Building with GenAI"
> **Duration:** ~2 hours
> **Format:** Google Colab Notebook + optional local Jupyter for Ollama sections

---

## Quick Reference

| Time | Section | Key Action |
|------|---------|------------|
| 0:00–0:05 | Welcome | Recap Workshop 1, today's agenda |
| 0:05–0:20 | Project Structure | Professional GenAI project layout |
| 0:20–0:45 | Image Generation | FLUX API, prompt engineering for images |
| 0:45–0:55 | Local Models | Ollama demo, why local matters |
| 0:55–1:00 | Break | 5-minute buffer |
| 1:00–1:25 | RAG Pipeline | Embeddings, FAISS, retrieval + generation |
| 1:25–1:45 | Mini AI Agent | Build agent with 3 tools + exercise |
| 1:45–1:55 | Wrap-Up & Q&A | Resources, next steps, bridge to Workshop 3 |

---

## 🎯 Opening (0:00–0:05)

### Recap Workshop 1:
> "Last time you SAW what GenAI can do — text generation, how Transformers work. Today you're going to BUILD things. By the end, you'll have generated images with AI, built a semantic search engine, and understood how AI agents work."

---

## 🏗️ Project Structure (0:05–0:20)

**Key message:** "As you move from notebooks to real projects, structure matters."

Walk through the folder structure diagram in the notebook:
- `src/` for code, `config/` for settings, `data/` for files
- `.env` for secrets (NEVER commit!)
- `requirements.txt` for reproducibility

**Interactive:** Ask students to type in chat what `.gitignore` should exclude.

---

## 🎨 Image Generation (0:20–0:45)

**This is the WOW section.**

1. Explain diffusion: "Start with noise → subtract noise step by step → get image"
2. Run the FLUX API connection cell
3. 🎯 **WOW MOMENT:** Run first image generation and display it
4. Explain prompt engineering: subject + style + details + lighting
5. Let students create their own images (10 min)

### ⚠️ Common issue:
FLUX free tier has GPU quotas. If rate-limited:
> "The free API is busy — lots of people using it! The code is correct. Try again after a few minutes."

---

## 🖥️ Local Models (0:45–0:55)

**Key message:** "Cloud is convenient, but local gives you privacy, speed, and no cost."

- Show the Cloud vs Local comparison table
- If Ollama is installed on your machine, do a live demo: `ollama run llama3.2 "Explain AI in one sentence"`
- Mention the Agent Programming Guide notebook for deeper hands-on

---

## 📚 RAG Pipeline (1:00–1:25)

**This is the technical core of this workshop.**

1. Explain the problem: "LLMs don't know YOUR data"
2. Show the RAG diagram: Documents → Embeddings → Vector Store → Retrieve → Augment → Generate
3. Walk through each code cell — this is where students need guidance
4. 🎯 **Aha moment:** When the retrieval returns relevant documents for a query

---

## 🤖 Mini AI Agent (1:25–1:45)

**Hands-on: build a working agent with 3 tools.**

> "An LLM alone is like a brain in a jar. An Agent is a brain with eyes, hands, and a notebook."

1. Walk through the agent diagram: Brain (LLM) + Tools + Memory + Planning
2. Build a mini agent with 3 tools: calculator, weather lookup, and RAG search
3. Let students see the agent autonomously decide which tool to call
4. **Exercise:** Students add their own custom tool to the agent

**Bridge to Workshop 3:**
> "In Workshop 3, you'll build a REAL agent that autonomously calls 7 hospital management tools — including the multimodal vision and RAG pipeline we just built."

---

## 🚨 Emergency Procedures

| Scenario | Action |
|----------|--------|
| FLUX API down | Show pre-saved images, explain the code is correct |
| Colab GPU unavailable | Switch to CPU — text gen still works, skip image gen |
| RAG section too slow | Use fewer documents, skip the GPT-2 generation step |
| Running over time | Cut: Agent architecture (theory) → Healthcare preview |
| **Never cut** | First image generation, RAG retrieval demo |

---

## 📋 Pre-Workshop Checklist

### Day Before:
- [ ] Test both notebooks end-to-end
- [ ] Verify FLUX API is responding
- [ ] If demoing Ollama: pull `llama3.2` model
- [ ] Have pre-generated images as backup

### 30 Minutes Before:
- [ ] Open Colab, run all cells to cache models
- [ ] Test screen share
- [ ] Have this guide open separately
