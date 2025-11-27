# 02. Setting Up ADK Agents

Learn three different ways to set up and run ADK agents: CLI, Web Interface, and Programmatic.

**Blog Post:** [https://arjunprabhulal.com/adk-setting-up-agent/](https://arjunprabhulal.com/adk-setting-up-agent/)

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Setup Steps](#setup-steps)
3. [Running Methods](#running-methods)
   - [Method 1: CLI](#method-1-cli)
   - [Method 2: Web Interface](#method-2-web-interface)
   - [Method 3: Programmatic](#method-3-programmatic)
4. [Next Steps](#next-steps)

## Prerequisites

- Python 3.10+
- Gemini API key from [AI Studio](https://aistudio.google.com/apikey)

## Setup Steps

1. Navigate to this module:

```bash
cd 02-setting-up-agent
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

4. Set up environment variables in `simple_agent/.env`:

```
GOOGLE_API_KEY=your-api-key-here
```

## Running Methods

### Method 1: CLI

The fastest way to interact with agents from the terminal.

```bash
# Basic run
adk run simple_agent

# Save session when exiting
adk run simple_agent --save_session

# Resume a saved session
adk run simple_agent --resume demo.session.json
```

### Method 2: Web Interface

Visual browser-based interface for chatting with agents.

```bash
# Start web UI (opens at http://127.0.0.1:8000)
adk web

# Custom port
adk web --port 8080

# With auto-reload for development
adk web --reload
```

### Method 3: Programmatic

Full control over agent behavior in Python code.

```bash
python run_agent.py
```

This demonstrates:
- `Runner` class for agent execution
- `InMemorySessionService` for session management
- Async event processing for streaming responses

**Test Query:** "What is the Transformers architecture in AI?"

## Next Steps

Continue to [03. Visual Builder](../03-visual-builder/)
