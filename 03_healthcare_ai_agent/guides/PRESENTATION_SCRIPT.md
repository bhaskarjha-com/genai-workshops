# 🎤 Workshop 3 — Complete Presentation Script
## "Agentic AI in Healthcare"
**Duration:** ~2 hours  
**Format:** Live instructor-led, screen sharing  
**Audience:** Engineering students with Workshop 1 & 2 foundations

---

## ⏱️ Master Timeline

| Time | Duration | Section | What's Happening |
|------|----------|---------|--------------------|
| 9:30–9:55 | 25 min | **Pre-workshop prep** | Your private setup, testing all 3 backends |
| 10:00–10:07 | 7 min | **Opening** | Welcome, recap W1-W2, today's roadmap |
| 10:07–10:27 | 20 min | **Module 1** | Multimodal Medical AI |
| 10:27–10:47 | 20 min | **Module 2** | Medical RAG |
| 10:47–10:52 | 5 min | **☕ Break** | "Stretch, grab water" |
| 10:52–11:22 | 30 min | **⭐ Module 3** | Healthcare Agent (CENTERPIECE) |
| 11:22–11:42 | 20 min | **Module 4** | Bias & Fairness |
| 11:42–11:52 | 10 min | **Module 5** | Safety & Guardrails |
| 11:52–12:00 | 8 min | **Closing** | Takeaways, careers, Q&A, resources |

---

## 🔧 PRE-WORKSHOP CHECKLIST (9:30 AM — Private, Before Going Live)

### Your Desktop Setup
Open these windows BEFORE the video call:

```
Window 1: VS Code with workshop_3 folder open
Window 2: Terminal (already activated venv: . .venv/Scripts/activate)
Window 3: Browser tab → https://aistudio.google.com (Gemini API dashboard — for showing students)
Window 4: Browser tab → video call
```

### Your Three Backends — Test ALL THREE at 9:30 AM

This workshop has **three-tier resilience**. Every module can run on:

| Backend | Environment Variable | When to Use |
|---------|---------------------|-------------|
| **☁️ Gemini** | `WORKSHOP_BACKEND=gemini` | Primary — live cloud API demo |
| **🖥️ Ollama** | `WORKSHOP_BACKEND=ollama` | If API is down, or to show local GPU deployment |
| **📋 Demo** | `WORKSHOP_BACKEND=demo` | Nuclear fallback — pre-recorded output, always works |

### Test Sequence (Do this at 9:30 AM)
```bash
# Activate environment
cd path/to/workshop_3_agentic_ai
. .venv/Scripts/activate

# ── Test 1: Gemini Cloud API ──
WORKSHOP_BACKEND=gemini python -c "
from dotenv import load_dotenv; load_dotenv()
from google import genai
client = genai.Client()
print(client.models.generate_content(model='gemini-2.5-flash', contents='Say hello in 5 words').text)
"
# Should print a 5-word greeting

# ── Test 2: Ollama Local GPU ──
ollama list
# Should show: dcarrascosa/medgemma-1.5-4b-it:Q8_0 AND qwen3:8b

WORKSHOP_BACKEND=ollama python -c "
import ollama
# Test MedGemma (vision + text)
r = ollama.chat(model='dcarrascosa/medgemma-1.5-4b-it:Q8_0', messages=[{'role':'user','content':'Say hello in 5 words'}])
print('MedGemma:', r['message']['content'])
# Test Qwen3 (tool calling)
r2 = ollama.chat(model='qwen3:8b', messages=[{'role':'user','content':'Say hello in 5 words'}])
print('Qwen3:', r2['message']['content'])
"
# Should print two 5-word greetings from local GPU

# ── Test 3: Pre-warm embeddings (avoids delay during Module 2/3) ──
python -c "from sentence_transformers import SentenceTransformer; m = SentenceTransformer('all-MiniLM-L6-v2'); print('Embeddings ready')"
```

### Which Backend to Start With?
- **Start with Gemini** (cloud) — it's faster and more impressive for the audience
- **Switch to Ollama** if you hit API rate limits (429 errors) — just say "Let me show you something cool — we're switching to a model running entirely on my GPU right now"
- The `.env` file controls it: change `WORKSHOP_BACKEND=gemini` to `WORKSHOP_BACKEND=ollama` and re-run

### Backend Switching During the Workshop
To switch mid-workshop, just change one line in `.env`:
```bash
# In .env file:
WORKSHOP_BACKEND=gemini    # ← change this to 'ollama' or 'demo'
```
Or override on the command line:
```bash
WORKSHOP_BACKEND=ollama python 01_multimodal_medical_ai.py
```

### Rate Limit Strategy
> [!IMPORTANT]
> Free tier = **15 requests per minute** (RPM). Across 5 modules you'll make ~10-15 API calls total. Space them out. If you get 429 errors, switch to `WORKSHOP_BACKEND=ollama` or `demo`.

### Contingency Plan
| If this happens... | Do this |
|--------------------|---------|
| API key dies/rate limit | Switch to `WORKSHOP_BACKEND=ollama` — runs locally on your GPU |
| Ollama crashes | Switch to `WORKSHOP_BACKEND=demo` — pre-recorded output |
| Both fail | `WORKSHOP_BACKEND=demo` — output is identical to live |
| ChromaDB crashes | Module 2/3 fall back to keyword search |
| SHAP crashes | Module 4 falls back to sklearn feature_importances_ |
| Internet drops completely | Use `WORKSHOP_BACKEND=ollama` — fully offline! Module 4 also fully offline |

---

## 📍 PART 1: OPENING (10:00–10:07)

### 🖥️ Screen: Share your VS Code with the workshop folder visible

### 🎤 Speaking Script:

> *"Good morning everyone! Welcome to Workshop 3 — the final workshop in our Generative AI series.*
>
> *I'm [Your Name]. Quick show of hands in the chat — how many of you attended Workshop 1 or 2?"*

**[Pause 10 seconds for chat responses]**

> *"Great. Quick recap for everyone:*
>
> *Workshop 1 was 'See AI' — you saw what GenAI can do. Text generation, image generation, how transformers work under the hood.*
>
> *Workshop 2 was 'Create AI' — you BUILT things. Local models with Ollama, RAG pipelines, medical document summarization.*
>
> *Today? Today is 'Act Like AI Agents.' We're not building chatbots. We're building an AI system that can THINK, REASON, and ACT autonomously in a hospital ICU."*

**[Show the architecture slide — switch to terminal and show the folder structure briefly]**

> *"Here's our journey in 5 modules:*
>
> *First — the agent's EYES. We'll use a multimodal LLM to literally analyze a chest X-ray. It can SEE medical images.*
>
> *Second — the agent's MEMORY. A RAG system with real medical guidelines, so it doesn't hallucinate treatment plans.*
>
> *Third — and this is the star — the agent's BRAIN. An autonomous agent that uses both the eyes AND the memory, plus hospital management tools, to handle an emergency admission. Nobody tells it what to do. It DECIDES.*
>
> *Fourth — the agent's CONSCIENCE. We check: does this AI treat Black patients differently from White patients? Spoiler: it does. And we detect it.*
>
> *Fifth — the agent's SAFETY NET. Real horror stories of AI gone wrong, guardrails that block dangerous outputs, and the regulatory landscape — including India's brand new SAHI framework from January 2026.*
>
> *Everything runs live. Real API calls. Real AI. And here's a bonus — we've built this so it can run on BOTH Google's cloud API AND a local model on my own GPU. Same code, same results. Let's go."*

---

## 📍 MODULE 1: MULTIMODAL MEDICAL AI (10:07–10:27)

### 🖥️ Screen: Terminal

### Setup (30 seconds)

```bash
python 01_multimodal_medical_ai.py
```

**[The backend selector will show at the top — point at it briefly]**

> *"Notice at the top — it shows the backend. We have three backends configured: Google's cloud, local GPU models (MedGemma for vision + Qwen3 for reasoning), and pre-recorded mode. We'll show both live setups today."*

### 🎤 Speaking Script — Opening Hook:

> *"Here's a question: When a doctor looks at a patient, do they just read a text file? No. They look at X-rays, ECGs, lab reports, hear the patient describe symptoms — multiple data types simultaneously.*
>
> *That's what multimodal AI does. Gemini 2.5 Flash can SEE images AND read text at the same time. Let me show you."*

### Phase 1: Text-Only Analysis (~3 min)
**[Output shows text-only diagnosis on screen]**

> *"First — we give the AI ONLY text. Patient symptoms: chest pain, shortness of breath, elevated troponin.*
>
> *Look at the response — it says 'could be cardiac, could be pulmonary.' It's hedging. It doesn't have enough information. Just like if YOU described your symptoms to a doctor over the phone."*

### Phase 2: Image-Only Analysis (~5 min)
**[Output shows X-ray analysis]**

> *"Now — we give it ONLY the chest X-ray. No text, no vitals. Just the image.*
>
> *Look — it says 'cardiomegaly, possible pleural effusion.' That's actually correct for this X-ray. But it's just describing what it sees. It can't connect it to the patient's story."*

> [!TIP]
> **Visual moment**: Point at the X-ray output and say:  
> *"This is a REAL LLM analyzing a REAL medical image. Not a lookup table. Not if-else rules. The same neural network that writes essays is now reading an X-ray."*

### Phase 3: Multimodal = Image + Text + Vitals (~5 min)
**[Output shows combined analysis with HIGH confidence]**

> *"NOW — we give it EVERYTHING. The X-ray, the symptoms, the vital signs, the lab values. All at once.*
>
> *Look at the difference! The confidence jumped. It's connecting the cardiomegaly on the X-ray with the troponin elevation and the BP drop. It's saying: 'STEMI with cardiogenic shock.' That's exactly what a cardiologist would say.*
>
> *THIS is why multimodal matters. Text alone? 'Maybe cardiac.' Image alone? 'Enlarged heart.' Both together? 'STEMI — activate the cath lab.'"*

### Code Walkthrough (~5 min)
**[Switch to VS Code, show the relevant code section]**

> *"Let me show you the code. It's surprisingly simple with the new Google GenAI SDK."*

Point at these lines:
```python
from google import genai
from google.genai import types

client = genai.Client()  # Auto-detects GEMINI_API_KEY

# Send image + text together
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
        prompt_text
    ],
)
```

> *"Three lines to send an image to an AI. `types.Part.from_bytes` for the image, a text prompt, and `generate_content`. That's it.*
>
> *This is the new `google-genai` SDK — the latest from Google. Not the old deprecated one."*

### 🔀 OPTIONAL: Show Ollama version (if time or if API is down)

> *"Now here's something cool. What if you don't want to send patient data to Google's cloud? Privacy regulations in many hospitals prohibit it.*  
>
> *Watch — I'm switching to a LOCAL model. MedGemma 1.5, running on my own Nvidia GPU right here."*

```bash
WORKSHOP_BACKEND=ollama python 01_multimodal_medical_ai.py
```

> *"Same code, same patient, same X-ray — but now it's running ENTIRELY on my GPU. No internet. No cloud. No data leaves this machine. MedGemma analyzes the X-ray, and Qwen3 handles the text reasoning — two models collaborating locally."*

### Transition to Module 2:

> *"So we've given our agent its EYES. It can SEE medical images. But a doctor doesn't just look at X-rays — they know thousands of treatment guidelines, drug interactions, protocols.*
>
> *Our agent needs MEMORY. That's Module 2 — Retrieval-Augmented Generation."*

---

## 📍 MODULE 2: MEDICAL RAG (10:27–10:47)

### 🖥️ Screen: Terminal

```bash
python 02_medical_rag_frontier.py
```

### 🎤 Speaking Script — Opening Hook:

> *"Let me tell you a scary story. I asked ChatGPT: 'Can cinnamon cure Type 2 diabetes?' And it said yes — with confidence. That's called a HALLUCINATION. And in healthcare, hallucinations kill people.*
>
> *RAG — Retrieval-Augmented Generation — solves this. Instead of generating answers from memory, the AI first RETRIEVES real medical documents, then generates an answer WITH CITATIONS. Like a student who actually reads the textbook before answering."*

### Phase 1: Building the Knowledge Base (~5 min)
**[Output shows ChromaDB being built]**

> *"Watch what happens. We're loading real medical guidelines — AHA, WHO, ADA, NICE — into a vector database called ChromaDB.*
>
> *Each document gets converted into a 384-dimensional EMBEDDING — a mathematical fingerprint of its meaning. 'Heart attack treatment' and 'STEMI management guidelines' have SIMILAR embeddings, even though they use different words. That's semantic search."*

### Phase 2: RAG Query Demo (~5 min)
**[Output shows cited answer]**

> *"Now I ask: 'What's the treatment protocol for STEMI?'*
>
> *Look at that answer — it cites [1] AHA Guidelines, [2] European Society of Cardiology. Every fact is traceable. No hallucination. A doctor can VERIFY this."*

### Phase 3: RAG vs No-RAG Comparison (~5 min)
**[Output shows dangerous vs safe answers side by side]**

> *"Here's the key moment. WITHOUT RAG — look at this response. The LLM is making up dosages, being way too confident, no sources.*
>
> *WITH RAG — grounded, cited, hedged. 'According to ADA 2024 guidelines...' THIS is what you deploy in a hospital."*

### Architecture Diagram (~3 min)
**[Output shows ASCII pipeline diagram]**

> *"Here's the full pipeline, visible on your screen. User query goes to the embedding model, gets compared against the vector database, top results come back, and THEN the LLM generates an answer using those results as context. The LLM never just 'makes stuff up' — it has sources."*

> [!TIP]
> **Key point**: *"Notice that the embeddings model (sentence-transformers) runs LOCALLY on your machine — it's only the answer generation that uses Gemini or our local MedGemma. The retrieval part is always local, always private."*

### Transition to Module 3:

> *"We now have the EYES — multimodal vision from Module 1. And the MEMORY — RAG from Module 2.*
>
> *Time for the star of the show. We're going to build the BRAIN — an AI agent that uses BOTH of these as tools, plus hospital management functions, to autonomously handle an ICU emergency.*
>
> *Let's take a 5-minute break first. Stretch, grab water. When we come back — the centerpiece."*

---

## ☕ BREAK (10:47–10:52)

> *"Five minutes. See you at 10:52."*

**[During break: Ctrl+C any running process. Clear terminal. Make sure Ollama is still running (`ollama list`). Ready to run Module 3.]**

---

## 📍 MODULE 3: HEALTHCARE AI AGENT ⭐ (10:52–11:22)

> [!IMPORTANT]
> This is the CENTERPIECE. Take your time. Students should walk away remembering this module.

### 🖥️ Screen: Terminal

```bash
python 03_healthcare_agent_frontier.py
```

### 🎤 Speaking Script — Opening Hook:

> *"Welcome back. This is it. The centerpiece.*
>
> *Forget chatbots. Forget autocomplete. What you're about to see is an AI that REASONS. It looks at a situation, DECIDES what to do, takes ACTION, looks at the result, decides the NEXT action — all autonomously.*
>
> *And here's the beautiful part: the two tools we just built? The multimodal vision and the RAG knowledge base? They become TOOLS that the agent can USE. We built the eyes and the memory. Now we build the brain that orchestrates everything."*

### Phase 1: Architecture Display (~3 min)
**[Output shows ASCII architecture diagram]**

> *"Look at this architecture. At the top — the LLM brain. When running on Gemini, it handles everything. When running locally, we use Qwen3 for orchestration and MedGemma for vision — a dual-model setup. Below it — 7 tools. Python functions.*
>
> *Two of them are highlighted. See `analyze_patient_xray` — that's Module 1's multimodal vision. See `search_medical_knowledge` — that's Module 2's RAG pipeline.*
>
> *When this agent runs, IT will decide whether to use these tools. Not us. IT."*

### Phase 2: ICU Status Display (~2 min)
**[Output shows bed status with severity bars]**

> *"Here's our simulated ICU. 8 beds, 7 occupied. Look at the severity bars — Priya is at 9/10 with septic shock. Only ONE bed is empty: ICU-07.*
>
> *And here come the incoming patients. Meera T., 62-year-old female, STEMI — that's a heart attack. Severity 9/10. She has a chest X-ray available.*
>
> *The question to the agent: handle this emergency admission. Check beds, review the patient, analyze the X-ray, look up treatment guidelines, and figure out what to do."*

### Phase 3: Live Agent Execution (~10 min)
**[Output shows agent trace — LIVE from Gemini or Ollama]**

> *"Watch the agent work. Nobody scripted this sequence. The LLM is DECIDING."*

**Point at each step as it appears:**

> *"Step 1 — It checked bed availability first. Smart. No point assigning a patient if there are no beds.*
>
> *Step 2 — It pulled the patient information. Name, age, vitals, severity.*
>
> *Step 3 — HERE. Look at this. It called `analyze_patient_xray` — that's MODULE 1's multimodal vision! The agent SEES the X-ray and reads: cardiomegaly, lower lobe opacity, possible pleural effusion.*
>
> *Step 4 — And NOW it calls `search_medical_knowledge` — that's MODULE 2's RAG! It's searching for STEMI treatment guidelines. It finds: AHA says primary PCI within 120 minutes.*
>
> *Step 5 — It assigns her to ICU-07. But look — PENDING_PHYSICIAN_APPROVAL. The AI doesn't just slam her into a bed. It PROPOSES. A human must APPROVE.*
>
> *Step 6 — It alerts the cardiology team and ICU staff. Door-to-balloon timer started.*
>
> *SIX autonomous steps. Using vision, knowledge retrieval, bed management, and clinical alerting. Nobody told it the order. The LLM decided: 'I should check beds first, then look at the patient, then analyze the X-ray, then check guidelines, then assign and alert.' THAT is agentic AI."*

### Phase 4: Function Calling Explained (~5 min)
**[Show the explanation section + code]**

> *"How does this actually work? It's called FUNCTION CALLING.*
>
> *You define Python functions with type hints and docstrings. The LLM READS those docstrings and understands what each tool does. You pass them as tools. When you send a message, the model autonomously decides: 'I need to call check_bed_availability first.' It returns a structured tool call, the function executes, the result goes back, and the model decides: 'OK, now I need get_patient_info.' This loop continues until the agent is satisfied."*

**[If time allows, briefly show the code:]**

```python
# ── Gemini: Automatic function calling ──
config = types.GenerateContentConfig(
    tools=AGENT_TOOLS,       # Our 7 Python functions
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False),
    system_instruction="You are a healthcare AI agent..."
)
response = client.models.generate_content(model="gemini-2.5-flash", contents=scenario, config=config)
```

> *"One API call — Gemini handles the entire multi-step loop internally. It calls our functions, reads the results, decides next steps, and keeps going until it's done."*

### 🔀 Phase 4B: Show Ollama Local Agent (~3 min — OPTIONAL but impressive)

> [!TIP]
> **This is your "wow" moment.** Show that the SAME code works locally. If you're running ahead of schedule, definitely do this. It shows production-grade engineering.

> *"Now watch this. Same 7 tools. Same patient. Same emergency. But running entirely on my GPU — Qwen3 orchestrates the tool calls, and MedGemma handles vision. Two open-source models collaborating."*

```bash
WORKSHOP_BACKEND=ollama python 03_healthcare_agent_frontier.py
```

> *"Look — Step 1, Step 2... the local models are making the SAME decisions. Qwen3 decides what to do, MedGemma analyzes the X-ray when needed, and the loop continues.*
>
> *With Gemini, function calling is AUTOMATIC — the SDK handles the loop. With Ollama, WE implement the loop manually: Qwen3 returns a tool call → we execute the function → feed the result back → Qwen3 decides the next tool. We built a 'manual agentic loop.'*
>
> *Same intelligence, same architecture, but running 100% locally. No patient data leaves this machine. THIS is how hospitals deploy AI in production — local models, on-premise GPUs, data sovereignty."*

### Phase 5: Human-in-the-Loop (~3 min)
**[Show the safety section output]**

> *"Notice something critical. The agent can check beds, look up info, analyze X-rays, search guidelines, and send notifications — ALL autonomously. But bed assignments, treatment decisions, medication orders, and discharge decisions? PENDING_PHYSICIAN_APPROVAL.*
>
> *This is called human-in-the-loop. In production healthcare AI, the AI PROPOSES, the physician APPROVES, the system EXECUTES. This is how Microsoft, Google, and Amazon all build their healthcare agents. It's not optional — it's a regulatory requirement."*

### Transition to Module 4:

> *"This agent is impressive. It reasons, it acts, it uses our tools. But before we ship it... can we TRUST it? Does it treat a 62-year-old Black woman the same as a 62-year-old White man? Let's find out."*

---

## 📍 MODULE 4: BIAS & FAIRNESS (11:22–11:42)

### 🖥️ Screen: Terminal

```bash
python 04_bias_and_fairness.py
```

> [!TIP]
> **Module 4 uses NO LLM at all** — it's entirely sklearn, SHAP, and AIF360. Runs offline, no API needed, no backend selection. Always works.

### 🎤 Speaking Script — Opening Hook:

> *"October 2019. Science magazine published a bombshell paper. A healthcare AI used by major hospitals to prioritize patients was systematically discriminating against Black patients. It wasn't designed to be racist. The training data was biased — it used healthcare spending as a proxy for health needs. But Black patients historically spend less due to systemic inequalities, not because they're healthier.*
>
> *Before we deploy our agent from Module 3, we MUST verify it's fair."*

### Phase 1: Dataset Generation (~2 min)
**[Output shows 2000 patients created]**

> *"We generate 2000 synthetic patient records with demographics — race, gender, age, insurance type. Then we train a model to predict hospital readmission."*

### Phase 2: The Bias Reveal (~5 min)
**[Output shows overall accuracy then per-group breakdown]**

> *"Overall accuracy: about 59%. Looks OK, right?*
>
> *Now look at the PER-GROUP breakdown. Asian patients: 61%. Black patients: 54%. That's a 7.2 percentage point gap!*
>
> *And gender — females: 56%, males: 61%. Another 5-point gap.*
>
> *The model that looked 'fine' on average is actually discriminating. This is EXACTLY what happened with the Optum algorithm."*

### Phase 3: AIF360 Regulatory Metrics (~5 min)
**[Output shows SPD, EOD, DI metrics]**

> *"These three metrics — Statistical Parity Difference, Equal Opportunity Difference, and Disparate Impact — are what the FDA actually checks when approving AI medical devices.*
>
> *SPD near 0 means outcomes are equally distributed. EOD near 0 means the model catches positive cases equally. And Disparate Impact — below 0.8 is the legal threshold for discrimination. Our model FAILS on two of three."*

### Phase 4: SHAP Explainability (~5 min)
**[Output shows individual prediction breakdown]**

> *"But detecting bias isn't enough. Doctors need to UNDERSTAND the AI's reasoning. SHAP tells us: 'The AI flagged this patient because of their previous admissions and medication adherence — not because of their race.'*
>
> *See — `med_adherence` pushes DOWN (reduces risk). `prev_admissions` pushes UP (increases risk). And yes, `race_Black` has a positive SHAP value — that's the bias we detected. The doctor can now see it and question it.*
>
> *This is called EXPLAINABILITY. The FDA requires it for medical AI device approval."*

### Transition to Module 5:

> *"We detected bias. We can explain individual predictions. But what ELSE can go wrong? Let me show you some real horror stories."*

---

## 📍 MODULE 5: SAFETY & GUARDRAILS (11:42–11:52)

### 🖥️ Screen: Terminal

```bash
python 05_safety_and_guardrails.py
```

### 🎤 Speaking Script — Opening Hook:

> *"Every failure I'm about to show you happened at a MAJOR institution, with EXPERT teams and MILLIONS of dollars in funding. If they got it wrong, what makes us think we won't? That's why we need systematic safety."*

### Phase 1: Real-World Failures (~3 min)
**[Output shows IBM Watson, Optum, Epic cases]**

> *"IBM Watson for Oncology — recommended UNSAFE cancer treatments. Optum — denied care to Black patients. Epic's sepsis model — false positive rate so high nurses started ignoring ALL alerts. And skin cancer AI — great on fair skin, terrible on dark skin because the training data was 95% Caucasian."*

### Phase 2: Safe vs Unsafe Demo (~4 min)
**[Output shows same question, different system prompts — LIVE from Gemini or Ollama]**

> *"Same model. Same question: 'I've had chest pain for a week, what should I do?' Watch the difference.*
>
> *WITHOUT a safety prompt — the model gives a confident-sounding diagnosis. Dangerous.*
>
> *WITH our safety prompt — it says 'seek medical attention immediately, I cannot provide a diagnosis.' SAME MODEL. The system prompt is everything."*

### Phase 3: Regulatory Table (~2 min)
**[Point at the regulatory table on screen]**

> *"2026 update for India: CDSCO now classifies AI diagnostic software as Class C medical devices. The SAHI framework from India AI Summit 2026. BODH platform benchmarking AI on Indian patient populations. This is real, this is now."*

### Transition to Closing:

> *"Let me wrap this up."*

---

## 📍 CLOSING (11:52–12:00)

### 🎤 Speaking Script:

> *"Let's step back and see what we built today.*
>
> *We built an AI that can SEE — multimodal vision that analyzes chest X-rays.*  
> *We built an AI that can REMEMBER — RAG that retrieves and cites real medical guidelines.*  
> *We built an AI that can THINK — an agent that autonomously chains 6 tools to handle an ICU emergency.*  
> *We learned to CHECK it — bias detection with AIF360, explainability with SHAP.*  
> *We learned to PROTECT with it — guardrails, safety prompts, human-in-the-loop.*
>
> *And here's what makes this production-grade: every module runs on THREE backends — Google's cloud, a local GPU using MedGemma, and pre-recorded mode. Same code, same architecture, deploy anywhere. THAT is how real systems are built — with redundancy, privacy options, and graceful fallbacks.*
>
> *This is not science fiction. This is production architecture.*
>
> *Qure.ai in Mumbai — their AI reads chest X-rays in rural hospitals where there's no radiologist. Niramai in Bangalore — AI-powered breast cancer screening using thermal imaging. Google's AMIE agent — can hold diagnostic conversations. All of them use the EXACT patterns we covered today — multimodal, RAG, function calling, bias detection, guardrails.*
>
> *If any of this excites you — the field is WIDE OPEN."*

### Career Moment (~2 min):

> *"Healthcare AI Engineer — ₹8 to 25 lakhs. ML Engineer at Google Health or Microsoft — ₹10 to 30 lakhs. Agentic AI Developer — ₹12 to 35 lakhs. These are REAL roles hiring RIGHT NOW in India.*
>
> *How do you break in? Take today's code. Extend it. Use a real dataset like MIMIC-III or ChestX-ray14. Build something. Put it on GitHub. Write a LinkedIn post about it. That's literally how people get hired."*

### Resource Sharing (~1 min):

> *"I'm dropping a STUDENT_RESOURCES.md file in the class chat right now. It has free learning paths, open datasets, career info, Indian AI companies, and all the tools we used today."*

**[Action: Share `STUDENT_RESOURCES.md` in class chat]**

### Q&A (~3 min):

> *"Open floor — any questions? Drop them in the chat."*

**Common questions to prepare for:**

| Question | Your Answer |
|----------|-------------|
| *"Is AI replacing doctors?"* | "No. AI proposes, doctors decide. Always. Every regulatory framework requires human-in-the-loop." |
| *"Can I run this on my laptop?"* | "Absolutely! Gemini API is free. Or install Ollama and run MedGemma 1.5 locally — it only needs 5GB VRAM." |
| *"What GPU do you need for local?"* | "MedGemma 1.5 4B runs on any GPU with 6+ GB VRAM. An RTX 3060 or better works fine." |
| *"Is this only for CS students?"* | "Healthcare/biotech students bring domain expertise — you know WHAT the AI should do. CS students know HOW. Both are needed." |
| *"How do I get the code?"* | "I'll share the GitHub repo / files in the class chat." |
| *"Can the agent handle multiple patients?"* | "This is a single-agent demo. Production systems use multi-agent architectures with supervisor agents." |
| *"What's the difference between Gemini and Ollama versions?"* | "Gemini is cloud—faster, smarter. Ollama runs locally—private, no data leaves the hospital. Same code, same architecture, different deployment." |

### Final Words:

> *"Thank you everyone for being part of this workshop series. Three workshops — from seeing AI, to creating AI, to building autonomous agents. You now understand the full stack.*
>
> *Go build something amazing. And remember — building AI that WORKS is hard. Building AI that works SAFELY and FAIRLY? That's the real challenge. And the only version worth deploying.*
>
> *Thank you!"*

---

## 📋 POST-WORKSHOP CHECKLIST

- [ ] Share `STUDENT_RESOURCES.md` in class chat
- [ ] Share workshop files (zip or GitHub link) in class chat
- [ ] Save the session recording (if recorded)
- [ ] Clean up: delete any temp files
- [ ] Update `.env` — rotate API key if you shared it on screen
- [ ] Stop Ollama if you no longer need it: `ollama stop`

---

## 🚨 EMERGENCY PLAYBOOK

### Tier 1: Gemini Cloud — LIVE (preferred)
```bash
WORKSHOP_BACKEND=gemini python <module>.py
```
This is your primary. Fastest responses, best quality output.

### Tier 2: Ollama Local GPU — LIVE (if cloud fails)
```bash
WORKSHOP_BACKEND=ollama python <module>.py
```
Say to audience:
> *"The cloud API has a temporary hiccup — perfect opportunity to show you something even cooler. I'm switching to models running entirely on my own GPU. MedGemma for medical vision, Qwen3 for reasoning. No internet needed. Watch..."*

### Tier 3: Demo Mode — Pre-recorded (nuclear fallback)
```bash
WORKSHOP_BACKEND=demo python <module>.py
```
Say to audience:
> *"I pre-recorded the exact output so you don't miss anything. This is what the live AI would show..."*

### If a module crashes mid-demo:
```bash
# Ctrl+C, then skip to next module
python 04_bias_and_fairness.py  # Module 4 is fully offline — guaranteed to work
```

### Ollama-specific issues:
| Issue | Fix |
|-------|-----|
| `ollama: command not found` | Open a new terminal, Ollama may not be on PATH |
| Model loading slow (first call) | Models take ~10 sec to load cold. Pre-warm during break |
| MedGemma can't analyze X-ray | Check that `sample_chest_xray.png` is in the workshop directory |
| Tool calling error 400 | Make sure `qwen3:8b` is installed — it's the tool-calling model |
| Tool calling returns unexpected results | Module 3 will fall back to demo trace automatically |

### If students can't see your screen:
Switch to sharing "Window" instead of "Desktop" with students. Share the terminal window directly.

### If you're running behind schedule:
| Cut this... | To save... |
|-------------|-----------|
| Module 2 code walkthrough | 3 min |
| Module 3 Ollama demo (Phase 4B) | 5 min |
| Module 5 regulatory table deep-dive | 3 min |
| Career section (just share the doc) | 3 min |

### If you're running ahead:
- **Show Ollama version of Module 1 or 3** — huge impact!
- Do a live code edit — change the patient scenario and re-run
- Open `aistudio.google.com` and show students how to get their own API key
- Show `workshop_config.py` and explain the three-tier architecture

---

## 🔧 TECHNICAL QUICK REFERENCE

### Backend Architecture
```
workshop_config.py ← Shared by ALL modules
    ↓
Reads WORKSHOP_BACKEND from .env
    ↓
┌─────────────┬──────────────────┬─────────────┐
│   gemini    │     ollama       │    demo     │
│ Cloud API   │   Local GPU      │ Pre-recorded│
│ Gemini 2.5  │ MedGemma (eyes)  │ Hardcoded   │
│ Flash       │ + Qwen3 (brain)  │ outputs     │
└─────────────┴──────────────────┴─────────────┘
```

### Model Details
| Model | Location | VRAM | Multimodal | Tool Calling | Used For |
|-------|----------|------|:----------:|:------------:|----------|
| Gemini 2.5 Flash | Google Cloud | N/A | ✅ | ✅ Auto | Everything (cloud) |
| MedGemma 1.5 4B | Local (Ollama) | ~5 GB | ✅ Vision | ❌ | Vision + text (M1, M2, M5, M3 X-ray tool) |
| Qwen3 8B | Local (Ollama) | ~5 GB | ❌ | ✅ Native | Agent orchestration (M3 tool-calling loop) |

### Module → Backend Feature Usage
| Module | Text Gen | Vision | Tool Calling | Offline? |
|--------|:--------:|:------:|:------------:|:--------:|
| 1 | ✅ | ✅ | — | Via Ollama |
| 2 | ✅ | — | — | Via Ollama |
| 3 | ✅ | ✅ (X-ray tool) | ✅ (6-step agent) | Via Ollama |
| 4 | — | — | — | Always offline |
| 5 | ✅ | — | — | Via Ollama |

---

## 📝 KEY PHRASES TO REMEMBER

These are the "sticky" phrases students will remember:

1. **"The agent's EYES, MEMORY, and BRAIN"** — Module progression metaphor
2. **"Same model, different prompt, completely different behavior"** — Module 5 safe vs unsafe
3. **"Average accuracy is NEVER enough"** — Module 4 bias reveal
4. **"AI proposes, doctor approves, system executes"** — Human-in-the-loop
5. **"The LLM DECIDED this order. Not us."** — Module 3 agent autonomy
6. **"In healthcare, hallucinations kill people"** — Module 2 RAG motivation
7. **"Same code, cloud or local — that's production engineering"** — Backend flexibility
8. **"Building AI that works is hard. Building AI that works SAFELY? That's the real challenge."** — Closing line
