# 01. Getting Started with Google ADK

Introduction to Google's Agent Development Kit, setting up your environment, and building your first agent.

**Blog Post:** [https://arjunprabhulal.com/adk-getting-started/](https://arjunprabhulal.com/adk-getting-started/)

## Table of Contents

1. [What is ADK?](#what-is-adk)
2. [Prerequisites](#prerequisites)
3. [Setup Steps](#setup-steps)
4. [Running the Agent](#running-the-agent)
5. [Next Steps](#next-steps)

## What is ADK?

The Agent Development Kit (ADK) is an open-source framework from Google for building AI agents. Key features:

- **Multi-model support** - Works with Gemini, GPT, Claude, and more
- **Flexible deployment** - Run locally or in the cloud
- **Rich ecosystem** - Integrates with Python, Java, and Go

## Prerequisites

- Python 3.10+
- Gemini API key from [AI Studio](https://aistudio.google.com/apikey)

## Setup Steps

1. Navigate to this module:

```bash
cd 01-getting-started
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

## Running the Agent

### Option 1: ADK Web Interface (Recommended)

```bash
adk web
```

Open http://127.0.0.1:8000 and chat with your agent.

**Test Query:** "Hello, what can you help me with?"

### Option 2: ADK CLI

```bash
adk run simple_agent
```

## Next Steps

Continue to [02. Setting Up Agents](../02-setting-up-agent/)
