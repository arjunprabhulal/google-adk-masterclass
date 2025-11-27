# 17. Callbacks

Intercepting and customizing agent behavior.

**Blog Post:** [https://arjunprabhulal.com/adk-callbacks/](https://arjunprabhulal.com/adk-callbacks/)

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Setup Steps](#setup-steps)
4. [Callback Types](#callback-types)
5. [Running the Demo](#running-the-demo)
6. [Next Steps](#next-steps)

## Overview

Callbacks let you intercept and customize agent behavior at various points in the execution lifecycle:

- **Logging** - Track agent activity
- **Filtering** - Block unwanted content
- **Validation** - Ensure data quality
- **Rate Limiting** - Control API usage

## Prerequisites

- Python 3.10+
- Gemini API key from [AI Studio](https://aistudio.google.com/apikey)

## Setup Steps

1. Navigate to this module:

```bash
cd 17-callbacks
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

4. Set up environment variables in `logged_agent/.env`:

```
GOOGLE_API_KEY=your-api-key-here
```

## Callback Types

| Callback | When It Runs | Use Case |
|----------|--------------|----------|
| `before_agent_callback` | Before agent starts | Setup, validation |
| `after_agent_callback` | After agent completes | Cleanup, logging |
| `before_model_callback` | Before LLM call | Prompt modification |
| `after_model_callback` | After LLM response | Response filtering |
| `before_tool_callback` | Before tool execution | Input validation |
| `after_tool_callback` | After tool result | Output processing |

### Example

```python
def before_model_logging(callback_context, llm_request):
    print(f"Sending request to model...")
    return None  # Continue normally

agent = Agent(
    before_model_callback=before_model_logging,
)
```

## Running the Demo

```bash
cd logged_agent
python agent.py
```

The demo shows:
- Logging callbacks for all lifecycle events
- Request/response inspection
- Execution timing

## Next Steps

Continue to [18. Artifacts](../18-artifacts/)
