# 15. Session, State & Memory

Conversation history, state management, and long-term memory.

**Blog Post:** [https://arjunprabhulal.com/adk-sessions-state/](https://arjunprabhulal.com/adk-sessions-state/)

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Setup Steps](#setup-steps)
4. [Core Concepts](#core-concepts)
5. [Running the Demo](#running-the-demo)
6. [Next Steps](#next-steps)

## Overview

ADK provides three levels of data persistence:

| Concept | Scope | Purpose |
|---------|-------|---------|
| **Session** | Single conversation | Track message history |
| **State** | Within a session | Store temporary data |
| **Memory** | Across sessions | Long-term knowledge |

## Prerequisites

- Python 3.10+
- Gemini API key from [AI Studio](https://aistudio.google.com/apikey)

## Setup Steps

1. Navigate to this module:

```bash
cd 15-sessions-state-memory
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

4. Set up environment variables in `memory_agent/.env`:

```
GOOGLE_API_KEY=your-api-key-here
```

## Core Concepts

### Sessions

Track conversation history within a single interaction:

```python
session_service = InMemorySessionService()
session = await session_service.create_session(
    app_name="my_app",
    user_id="user_123"
)
```

### State

Store temporary data within a session:

```python
# In a tool function
tool_context.state["cart"] = ["item1", "item2"]
```

### Memory

Long-term knowledge across sessions:

```python
# Development
memory_service = InMemoryMemoryService()

# Production
memory_service = VertexAiMemoryBankService()
```

## Running the Demo

```bash
cd memory_agent
python agent.py
```

The demo shows:
- Creating sessions with user IDs
- Storing and retrieving state
- Multi-turn conversations

## Next Steps

Continue to [16. Context Management](../16-context-management/)
