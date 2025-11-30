# 🧠 ECHOFORM

> A self-reflecting multi-agent cognitive architecture powered by Google Gemini ADK that observes, evaluates, remembers, and evolves its own intelligence.

---

## 🚀 Overview

ECHOFORM is an **experimental AI system**, not a chatbot.

It models intelligence as a *system* rather than a single model call by combining:

* Google Gemini ADK (as the thinking engine)
* Multi-agent orchestration
* SQL-based long-term memory
* Evaluation and scoring
* Personality mutation
* Observability and logging

Each interaction modifies the system’s future behavior.

**Cognitive Loop:**

```
User Input
   ↓
Generator (Gemini ADK)
   ↓
Observer (Meta-Cognition)
   ↓
Compressor (Abstraction)
   ↓
Memory (SQLite)
   ↓
Evaluator (Scoring)
   ↓
Mutator (Behavior Change)
   ↓
Response
```

---

## 🎯 Purpose

ECHOFORM explores whether an AI system can:

* Reflect on its own reasoning
* Persist cognition across time
* Evaluate its own output
* Evolve personality traits
* Expose internal reasoning pathways

The project focuses on **cognitive architecture**, not prompt engineering.

---

## 👥 Target Audience

| Group                      | Usage                       |
| -------------------------- | --------------------------- |
| Kaggle / Course Evaluators | Review system behavior      |
| AI Researchers             | Cognitive experiments       |
| Developers                 | Agent architecture          |
| Students                   | Production-style AI systems |

---

## 🧬 Agent Architecture

ECHOFORM is built from specialized agents that collaborate:

| Agent      | Function                                          |
| ---------- | ------------------------------------------------- |
| Generator  | Uses Gemini ADK to generate responses + reasoning |
| Observer   | Analyzes reasoning (tone, bias, depth)            |
| Compressor | Abstracts cognition into a fingerprint            |
| Memory     | Persist data in SQLite                            |
| Evaluator  | Scores responses                                  |
| Mutator    | Evolves personality                               |

Each agent is isolated, testable, and interchangeable.

---

## 🧠 Google Gemini ADK Integration

ECHOFORM uses **Google Gemini ADK** as its language model backend.

### How Gemini is used:

* Prompted with system-level personality traits
* Receives SQL memory context
* Asked to produce explicit reasoning blocks
* Returns responses that are evaluated and evolved

### Fallback Mode

If no API key is present, ECHOFORM runs in **simulation mode** and still:

* Generates reasoning
* Evolves traits
* Writes to memory

This makes the system runnable for any judge without configuration.

---

## 🔑 Setup Gemini

1. Install SDK:

```bash
pip install google-generativeai
```

2. Set environment variable:

### Windows

```cmd
setx GEMINI_API_KEY "your_key_here"
```

### Linux / macOS

```bash
export GEMINI_API_KEY="your_key_here"
```

Restart terminal after setting the key.

---

## 🗃 SQL Cognitive Memory

All cognition is persisted via SQLite.

### Tables

| Table               | Purpose                    |
| ------------------- | -------------------------- |
| sessions            | Session metadata           |
| messages            | Dialogue history           |
| reasoning_snapshots | Raw + compressed reasoning |
| evaluations         | Scoring history            |
| session_traits      | Personality profile        |

This supports:

* Replay
* Analysis
* Drift study
* Debugging

---

## 🖥 Interfaces

### CLI

```bash
python app.py
```

### Web UI

```bash
streamlit run ui/web_app.py
```

The UI displays:

* Scores
* Traits
* Reasoning
* Cognition fingerprint
* SQL memory viewer

---

## 🔍 Observability

Every system event is logged:

```
[AGENT] Generator invoked
[OBSERVE] Reasoning analyzed
[COMPRESS] Memory fingerprint stored
[EVAL] Response scored
[MUTATION] Traits updated
```

Judges can inspect:

* Logs
* Database rows
* Trait evolution

---

## 📊 Evaluation Metrics

| Metric      | Description         |
| ----------- | ------------------- |
| Accuracy    | Logical soundness   |
| Clarity     | Readability         |
| Depth       | Abstraction         |
| Originality | Novelty             |
| Overall     | Weighted evaluation |

---

## 🧪 Testing

Run all tests:

```bash
pytest
```

Tests validate:

* Agents
* SQL memory
* Gemini fallback
* Mutation logic

---

## 🏫 Course Alignment (5-Day AI Agents Intensive)

The project explicitly matches course pillars:

| Topic         | ECHOFORM             |
| ------------- | -------------------- |
| Models        | Gemini ADK           |
| Tools         | SQLite, logging      |
| Orchestration | Engine-based routing |
| Memory        | SQL persistence      |
| Evaluation    | Scoring agent        |
| Production    | Config + UI + tests  |

---

## 🌟 Why It’s Different

Typical projects:

> Prompt → Response

ECHOFORM:

> Prompt → Cognition System

It models AI as:

* Stateful
* Observable
* Evolvable
* Experimental

---

## 🏁 One-Line Pitch

> A cognitive AI system that analyzes, remembers, evaluates, and evolves with every interaction.

---

## 📜 License

MIT — free to experiment and extend.

---

## ✨ Final Note

ECHOFORM does not claim intelligence.

It **studies** it.
