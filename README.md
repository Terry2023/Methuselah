# Methuselah
**Sovereign AI Dashboard with Autonomous Gatekeeper LLM**

A locally-sovereign AI dashboard running entirely on commodity hardware 
with no cloud dependencies. All inference stays on-device via Ollama.

---

## What It Is

Methuselah is a single-node implementation of the FI-13 sovereignty 
boundary concept — a skeuomorphic browser-based control surface that 
routes user prompts through an autonomous Gatekeeper LLM before 
dispatching to a local model roster.

The Gatekeeper performs four functions automatically:
1. **Prompt scrubbing** — spelling, grammar, intent clarification
2. **Intent classification** — task type detection drives model selection
3. **Model routing** — selects optimal backend from Ollama roster
4. **Weight adjustment** — sets temperature and sampling parameters

---

## Hardware

Developed and tested on:
- AMD Ryzen 9 7950X
- NVIDIA RTX 4070
- 64GB DDR5
- Ubuntu 24.04 LTS (WSL2)

Runs on any machine capable of running Ollama with at least 16GB RAM.

---

## Model Roster

| Model | Use case |
|---|---|
| Qwen2.5 | Math, code, formal reasoning |
| Mistral-NeMo 12B | Analysis, factual queries |
| Llama 3.1 8B | General, summarization |
| Gemma2 9B | Creative, open-ended |

---

## Installation

```bash
# Clone the repo
git clone https://github.com/Terry2023/methuselah.git
cd methuselah/src

# Install dependencies
pip install fastapi uvicorn httpx duckduckgo-search

# Start Ollama and pull models
ollama pull qwen2.5
ollama pull mistral-nemo
ollama pull llama3.1:8b
ollama pull gemma2:9b

# Launch
start_methuselah.bat    # Windows
# or
uvicorn main:app --host 127.0.0.1 --port 8000
```

Then open `index.html` in your browser.

---

## FI-13 Protocol Mapping

| Methuselah component | FI-13 protocol | Notes |
|---|---|---|
| Localhost boundary | P2 SCP | Sovereignty enforced by network interface |
| Model routing | P1 DHP | Capability-based dispatch |
| Category guardrails | P6 OMP | Domain ontology switching |
| SQLite memory | P3 SSP | Cross-session state continuity |
| Gatekeeper LLM | P6/P8 | Automated intent framing and routing |
| Slider weights | P11 CSP | Trust-weighted parameter control |

Methuselah is an empirical single-node precursor to the full FI-13 
federated architecture described in the companion paper.

---

## Related

- [fi13-protocol](https://github.com/Terry2023/fi13-protocol) — 
  The formal FI-13 specification this implements
- [hive-engine](https://github.com/Terry2023/hive-engine) — 
  Multi-model debate engine (P10/P11)

---

*Part of the Paradigm 3D / Cislunar Systems Architect research portfolio.*  
*ORCID: [0009-0004-1981-0916](https://orcid.org/0009-0004-1981-0916)*
