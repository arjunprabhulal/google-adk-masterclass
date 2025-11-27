# 05. Workflow Agents

Sequential, Parallel, and Loop workflow patterns in ADK.

**Blog Post:** [https://arjunprabhulal.com/adk-workflow-sequential-loop-parallel/](https://arjunprabhulal.com/adk-workflow-sequential-loop-parallel/)

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Setup Steps](#setup-steps)
3. [Workflow Patterns](#workflow-patterns)
4. [Running the Examples](#running-the-examples)
5. [Next Steps](#next-steps)

## Prerequisites

- Python 3.10+
- Gemini API key from [AI Studio](https://aistudio.google.com/apikey)

## Setup Steps

1. Navigate to this module:

```bash
cd 05-workflow-agents
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r ../requirements.txt
```

4. Set up environment variables in each agent folder's `.env`:

```
GOOGLE_API_KEY=your-api-key-here
```

> **Advanced Examples**: See the [blog post](https://arjunprabhulal.com/adk-workflow-sequential-loop-parallel/) for production-ready examples with state management (`output_key`) and domain-specific implementations.

## Workflow Patterns

### 1. Sequential Agent

Execute agents one after another, passing output to the next step.

**Folder:** `sequential_agent/`

**Flow:**
```
Research → Write → Edit
```

**Use Case:** Multi-step pipelines where each step depends on the previous one.

**Test Query:** "Write a blog post about AI trends"

---

### 2. Parallel Agent

Execute agents simultaneously for independent tasks.

**Folder:** `parallel_agent/`

**Flow:**
```
┌─ Market Analyst ─┐
│                  │
├─ Tech Analyst   ─┼─→ Combined Results
│                  │
└─ Risk Analyst  ──┘
```

**Use Case:** Batch processing where tasks don't depend on each other.

**Test Query:** "Analyze the electric vehicle industry"

---

### 3. Loop Agent

Repeat agent execution until a condition is met or max iterations reached.

**Folder:** `loop_agent/`

**Flow:**
```
Refine → Check Quality → (repeat until DONE or max 5 iterations)
```

**Use Case:** Iterative refinement tasks.

**Test Query:** "Improve this text: AI is good for business"

## Running the Examples

### Using ADK Web (Recommended)

Start the web interface:

```bash
adk web --port 8001
```

Open http://127.0.0.1:8001 and select from the dropdown:

| Agent | Description |
|-------|-------------|
| `sequential_agent` | Research → Write → Edit pipeline |
| `parallel_agent` | Market + Tech + Risk analysts in parallel |
| `loop_agent` | Iterative content refinement |

### Using ADK CLI

```bash
# Sequential
adk run sequential_agent

# Parallel
adk run parallel_agent

# Loop
adk run loop_agent
```

## Project Structure

```
05-workflow-agents/
├── sequential_agent/
│   ├── __init__.py
│   ├── agent.py
│   └── .env
├── parallel_agent/
│   ├── __init__.py
│   ├── agent.py
│   └── .env
├── loop_agent/
│   ├── __init__.py
│   ├── agent.py
│   └── .env
└── README.md
```

## Next Steps

Continue to [06. Multi-Agent Systems](../06-multi-agent-systems/)
