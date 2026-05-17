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
