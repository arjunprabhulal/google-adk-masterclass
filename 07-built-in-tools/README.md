# 07. Built-in Tools

Google Search and Code Executor tools in ADK.

**Blog Post:** [https://arjunprabhulal.com/adk-built-in-tools/](https://arjunprabhulal.com/adk-built-in-tools/)

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Setup Steps](#setup-steps)
4. [Available Tools](#available-tools)
5. [Google Search Tool](#google-search-tool)
6. [Code Executor Tool](#code-executor-tool)
7. [Running the Agent](#running-the-agent)
8. [Project Structure](#project-structure)
9. [Next Steps](#next-steps)

## Overview

ADK provides built-in tools that agents can use out of the box:

- **Google Search** - Real-time web search with grounding
- **Code Executor** - Safe Python code execution in a sandbox

## Prerequisites

- Python 3.10+
- Gemini API key from [AI Studio](https://aistudio.google.com/apikey)

## Setup Steps

1. Navigate to this module:

```bash
cd 07-built-in-tools
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

4. Create `.env` file in `google_search_agent/`:

```bash
echo "GOOGLE_GENAI_USE_VERTEXAI=0" > google_search_agent/.env
echo "GOOGLE_API_KEY=your-api-key-here" >> google_search_agent/.env
```

## Available Tools

| Tool | Import | Description |
|------|--------|-------------|
| `google_search` | `from google.adk.tools import google_search` | Web search via Google |
| `BuiltInCodeExecutor` | `from google.adk.code_executors import BuiltInCodeExecutor` | Python code execution |

## Google Search Tool

The Google Search tool enables real-time web searches with grounding:

```python
from google.adk.agents import Agent
from google.adk.tools import google_search

agent = Agent(
    model="gemini-2.5-flash",
    name="search_agent",
    instruction="You are a helpful assistant with web search.",
    tools=[google_search],
)
```

**Features:**
- Real-time search results
- Grounded responses with citations
- Automatic query formulation

## Code Executor Tool

The Code Executor runs Python code in a secure sandbox:

```python
from google.adk.agents import Agent
from google.adk.code_executors import BuiltInCodeExecutor

agent = Agent(
    model="gemini-2.5-flash",
    name="code_agent",
    instruction="You can write and execute Python code.",
    code_executor=BuiltInCodeExecutor(),
)
```

**Features:**
- Sandboxed execution (safe)
- Supports common libraries (math, json, etc.)
- Returns stdout, stderr, and results
- Great for calculations, data processing

**Example queries:**
- "Calculate the factorial of 10"
- "Generate a list of prime numbers up to 50"
- "Parse this JSON and extract the names"

## Running the Agent

### Using ADK Web

```bash
adk web
```

Open http://127.0.0.1:8000 and select `google_search_agent`.

**Test Queries:**
- "What's the latest news on AI?"
- "Search for Python 3.12 new features"

### Using ADK CLI

```bash
adk run google_search_agent
```

## Project Structure

```
07-built-in-tools/
├── README.md
├── google_search_agent/
│   ├── __init__.py
│   ├── agent.py          # Agent with google_search tool
│   └── .env
├── code_agent.py          # Standalone Code Executor example
└── search_agent.py        # Standalone Search example
```

## Next Steps

Continue to [08. Vertex AI RAG](../08-vertex-ai-rag/)
