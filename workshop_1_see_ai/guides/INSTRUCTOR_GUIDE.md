# 🎤 Workshop 1 — Instructor Guide

> **Title:** "See AI — GenAI Fundamentals"
> **Duration:** ~90 minutes
> **Format:** Google Colab Notebook, delivered via screen share

---

## Quick Reference

| Time | Section | Key Action |
|------|---------|------------|
| 0:00–0:10 | Welcome & Hook | Live demo of text generation |
| 0:10–0:25 | AI Mindset | Concept explanation: GenAI, Transformers, Attention |
| 0:25–0:40 | Setup | Everyone runs install cells together |
| 0:40–1:05 | Text Generation | Hands-on: load GPT-2, generate, experiment |
| 1:05–1:10 | Break | 5-minute buffer |
| 1:10–1:20 | Temperature Lab | Compare creative vs conservative outputs |
| 1:20–1:30 | Wrap-Up & Q&A | Review, resources, tease Workshop 2 |

---

## 🎯 Opening Hook (0:00–0:10)

**Before students do anything, demo on YOUR screen:**
1. Open the notebook
2. Run the text generation cell with prompt: "VIT students are"
3. Show the AI-generated text
4. Say: *"This took 3 lines of code. By the end of today, YOU will build this."*

**Key messages:**
- "No prior AI experience needed"
- "Everything runs in your browser — no installation required"
- "If you get stuck, type HELP in chat"

---

## 🧠 Concepts (0:10–0:25)

### Key talking points:

1. **What is GenAI?** (3 min)
   > "Traditional AI analyzes. Generative AI CREATES. ChatGPT, Midjourney, DALL-E — all Generative AI."

2. **The Autocomplete Analogy** (5 min)
   > "Think of your phone's autocomplete. It predicts the next word. GenAI is like that, but trained on the ENTIRE internet."

3. **Transformers & Attention** (5 min)
   > "The magic is called 'Attention'. The AI looks at ALL words and decides which ones matter for the next word."

4. **Parameters = Knowledge** (2 min)
   > "GPT-2 has 124 million parameters. GPT-4 has 1.8 TRILLION. More parameters = more knowledge."

**Check understanding:** "Type 1 in chat if you understand that GenAI works by predicting 'what comes next'"

---

## 🛠️ Setup (0:25–0:40)

⚠️ **CRITICAL: Everyone must complete this together**

1. Share the Colab notebook link in chat
2. Students click: File → Open in Colab
3. Run installation cell → wait for "Installation Complete"
4. Run verification cell → wait for "✅" checkmarks

### Common issues:

| Problem | Solution |
|---------|----------|
| "ModuleNotFoundError" | Re-run the install cell |
| Cell doesn't run | Check if connected (top right shows "Connected") |
| Slow/stuck | Click Runtime → Restart and run all |

---

## ✏️ Hands-On (0:40–1:05)

**Text Generation with GPT-2:**
1. Load model (5 min) — first time takes 2-3 min to download
2. First generation (5 min) — 🎯 WOW MOMENT: "Look at what the AI wrote!"
3. Explain parameters (5 min) — temperature, max_tokens
4. Students experiment (10 min) — "YOUR TURN" cell

**Checkpoint:** "If you generated your own text, type GEN in chat!"

---

## 🎓 Wrap-Up (1:20–1:30)

### Tease Workshop 2:
> "Next time we'll go deeper — image generation, local models, and building a RAG pipeline!"

### Call to action:
> "Before next time, try different prompts and explore Hugging Face!"

---

## 🚨 Emergency Procedures

| Scenario | Action |
|----------|--------|
| Colab goes down | Share screen, demo from your computer |
| API rate limited | Show pre-saved outputs as examples |
| Running over time | Cut: temperature comparison → prompt comparison → bonus |
| **Never cut** | First text generation, first image generation, Q&A |

---

## 📋 Pre-Workshop Checklist

### Day Before:
- [ ] Test notebook end-to-end in Colab
- [ ] Prepare backup demo recordings
- [ ] Have notebook link ready to share

### 30 Minutes Before:
- [ ] Open Colab, run all cells to cache models
- [ ] Join meeting, test screen share
- [ ] Have this guide open on a separate screen
