# 20. Events

Understanding the event system in ADK agent execution.

**Blog Post:** [https://arjunprabhulal.com/adk-events/](https://arjunprabhulal.com/adk-events/)

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Setup Steps](#setup-steps)
4. [Event Structure](#event-structure)
5. [Identifying Events](#identifying-events)
6. [Event Actions](#event-actions)
7. [Running the Demo](#running-the-demo)

## Overview

Events are immutable records that capture every significant occurrence during an agent's interaction lifecycle. They enable:

- **Real-time streaming** - Show responses as they're generated (check `event.partial`)
- **Debugging** - Trace agent execution with `event.author`, `event.id`
- **Monitoring** - Track tool calls via `get_function_calls()` and `get_function_responses()`
- **State tracking** - Monitor changes via `event.actions.state_delta`

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

## Event Structure

Events build upon `LlmResponse` and include these key properties:

| Property | Description |
|----------|-------------|
| `event.author` | Who sent it (`'user'` or agent name) |
| `event.id` | Unique event identifier |
| `event.invocation_id` | Tracks the interaction cycle |
| `event.timestamp` | Event creation time |
| `event.content` | Message payload (text, parts) |
| `event.partial` | `True` if streaming incomplete |
| `event.actions` | Control signals (state changes, etc.) |

Import from:

```python
from google.adk.events import Event, EventActions
```

> **Note:** The `Event` class import is optional for basic usage due to Python's duck typing, but recommended for type hints and IDE support.

## Identifying Events

ADK uses a single `Event` class. Identify event types using helper methods:

| Event Type | How to Identify | Access Data |
|------------|-----------------|-------------|
| **Text Content** | Check `event.content.parts` | `event.content.parts[0].text` |
| **Tool Call** | `event.get_function_calls()` | `call.name`, `call.args` |
| **Tool Result** | `event.get_function_responses()` | `response.name`, `response.response` |
| **Streaming** | `event.partial == True` | Incomplete chunks |
| **Final Response** | `event.is_final_response()` | Displayable content |

### Example: Processing Events

```python
async for event in runner.run_async(
    user_id=user_id,
    session_id=session_id,
    new_message=content
):
    # Check for tool calls
    function_calls = event.get_function_calls()
    if function_calls:
        for call in function_calls:
            print(f"Calling: {call.name}({call.args})")

    # Check for tool results
    function_responses = event.get_function_responses()
    if function_responses:
        for resp in function_responses:
            print(f"Result: {resp.name} -> {resp.response}")

    # Check for displayable content
    if event.is_final_response():
        if event.content and event.content.parts:
            print(event.content.parts[0].text)
```

## Event Actions

The `event.actions` field carries control signals:

| Action | Description |
|--------|-------------|
| `state_delta` | Key-value pairs of modified session state |
| `artifact_delta` | Updated artifact versions |
| `transfer_to_agent` | Routes control to named agent |
| `escalate` | Terminates agent loops |
| `skip_summarization` | Prevents LLM processing of tool results |

### Example: Tracking State Changes

```python
if event.actions and event.actions.state_delta:
    for key, value in event.actions.state_delta.items():
        print(f"State changed: {key} = {value}")
```

## Running the Demo

```bash
cd event_agent
python agent.py
```

The demo shows:
- Real-time event streaming with `event.partial`
- Tool calls via `get_function_calls()`
- Tool results via `get_function_responses()`
- Final response detection with `is_final_response()`
- Event metadata: `author`, `id`, `timestamp`
