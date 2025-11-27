# 04. LLM Agents

Building intelligent LLM-powered agents with Google ADK.

**Blog Post:** [https://arjunprabhulal.com/adk-llm-agents/](https://arjunprabhulal.com/adk-llm-agents/)

## Table of Contents

1. [What is an LLM Agent?](#what-is-an-llm-agent)
2. [Prerequisites](#prerequisites)
3. [Setup Steps](#setup-steps)
4. [Agent Configuration](#agent-configuration)
5. [Running the Agent](#running-the-agent)
6. [Next Steps](#next-steps)

## What is an LLM Agent?

An LLM Agent uses a Large Language Model as its reasoning engine to:

- Understand user intent
- Plan and execute actions
- Generate contextual responses
- Maintain conversation state

## Prerequisites

- Python 3.10+
- Gemini API key from [AI Studio](https://aistudio.google.com/apikey)

## Setup Steps

1. Navigate to this module:

```bash
cd 04-llm-agents
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

4. Set up environment variables in `financial_analyst/.env`:

```
GOOGLE_API_KEY=your-api-key-here
```

## Agent Configuration

Key parameters when defining an LLM Agent:

| Parameter | Description | Example |
|-----------|-------------|---------|
| `model` | The LLM model to use | `gemini-2.5-flash` |
| `name` | Unique agent identifier | `fin_analyst` |
| `instruction` | System prompt defining behavior | Role, expertise, guidelines |
| `description` | What the agent does | Used for routing in multi-agent systems |

## Running the Agent

### Using ADK Web

```bash
adk web
```

Open http://127.0.0.1:8000 and select `financial_analyst`.

**Test Queries:**
- "What is a PE ratio?"
- "Explain the difference between growth and value stocks"
- "What are the key metrics in a 10-K filing?"

### Using ADK CLI

```bash
adk run financial_analyst
```

## Next Steps

Continue to [05. Workflow Agents](../05-workflow-agents/)
