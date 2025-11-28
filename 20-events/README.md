# 20. Events

Event streaming and debugging in ADK.

**Blog Post:** [https://arjunprabhulal.com/adk-events/](https://arjunprabhulal.com/adk-events/)

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Setup Steps](#setup-steps)
4. [Event Types](#event-types)
5. [Running the Demo](#running-the-demo)

## Overview

Events are the fundamental building blocks of ADK's execution model. They enable:

- **Real-time streaming** - Show responses as they're generated
- **Debugging** - Trace agent execution step by step
- **Monitoring** - Track tool calls and errors

## Prerequisites

- Python 3.10+
- Gemini API key from [AI Studio](https://aistudio.google.com/apikey)

## Setup Steps

1. Navigate to this module:

```bash
cd 20-events
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

4. Set up environment variables in `event_agent/.env`:

```
GOOGLE_API_KEY=your-api-key-here
```

## Event Types

| Event | Description | Contains |
|-------|-------------|----------|
| `ContentEvent` | Text content from agent | `content.parts[].text` |
| `ToolCallEvent` | Tool execution request | `tool_calls[]` |
| `ToolResultEvent` | Tool execution result | `tool_results[]` |
| `ErrorEvent` | Error information | `error` |
| `EndEvent` | Conversation end | Final state |

### Streaming Events

```python
async for event in runner.run_async(
    user_id=user_id,
    session_id=session_id,
    new_message=content
):
    if event.content and event.content.parts:
        for part in event.content.parts:
            if part.text:
                print(part.text, end="", flush=True)
```

## Running the Demo

```bash
cd event_agent
python agent.py
```

The demo shows:
- Real-time event streaming
- Tool call events
- Event inspection for debugging
