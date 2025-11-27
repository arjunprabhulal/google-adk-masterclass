# 06. Multi-Agent Systems

Agent orchestration and collaboration patterns.

**Blog Post:** [https://arjunprabhulal.com/adk-multi-agent-systems/](https://arjunprabhulal.com/adk-multi-agent-systems/)

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Setup Steps](#setup-steps)
4. [Delegation Patterns](#delegation-patterns)
5. [Running the Agent](#running-the-agent)
6. [Next Steps](#next-steps)

## Overview

Multi-agent systems divide work among specialists, coordinate interactions, and manage shared context. Key benefits:

- **Specialization** - Each agent focuses on specific tasks
- **Scalability** - Add new specialists without changing the coordinator
- **Maintainability** - Easier to update individual components

## Prerequisites

- Python 3.10+
- Gemini API key from [AI Studio](https://aistudio.google.com/apikey)

## Setup Steps

1. Navigate to this module:

```bash
cd 06-multi-agent-systems
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

4. Set up environment variables in `customer_support/.env`:

```
GOOGLE_API_KEY=your-api-key-here
```

## Delegation Patterns

| Pattern | Description | Use Case |
|---------|-------------|----------|
| **Hub-Spoke** | Central coordinator delegates to specialists | Customer support routing |
| **Pipeline** | Chain of agents processing in sequence | Content creation workflow |
| **Swarm** | Agents collaborate dynamically | Complex research tasks |

## Running the Agent

### Using ADK Web

```bash
adk web
```

Open http://127.0.0.1:8000 and select `customer_support`.

**Test Queries:**
- "Research AI trends and write a summary"
- "I need help with a technical issue"

### Using ADK CLI

```bash
adk run customer_support
```

## Next Steps

Continue to [07. Built-in Tools](../07-built-in-tools/)
