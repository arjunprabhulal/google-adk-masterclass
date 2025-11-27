# 10. Custom Function Tools

Building custom Python function tools for ADK agents.

**Blog Post:** [https://arjunprabhulal.com/adk-custom-tools-function/](https://arjunprabhulal.com/adk-custom-tools-function/)

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Setup Steps](#setup-steps)
4. [Creating a Function Tool](#creating-a-function-tool)
5. [Running the Agent](#running-the-agent)
6. [Next Steps](#next-steps)

## Overview

Custom function tools are Python functions that agents can call. ADK automatically wraps them - no need for `FunctionTool()`.

## Prerequisites

- Python 3.10+
- Gemini API key from [AI Studio](https://aistudio.google.com/apikey)

## Setup Steps

1. Navigate to this module:

```bash
cd 10-custom-function-tools
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

4. Set up environment variables in `custom_tool_agent/.env`:

```
GOOGLE_API_KEY=your-api-key-here
```

## Creating a Function Tool

1. Define a Python function with **type hints**
2. Add a **docstring** describing the function
3. Return a **dictionary** with the result
4. Pass the function directly to the agent's `tools` list

```python
def get_order_status(order_id: str) -> dict:
    """Retrieves the status of an order by order ID."""
    return {"order_id": order_id, "status": "Shipped"}

agent = Agent(
    model="gemini-2.5-flash",
    tools=[get_order_status],  # ADK auto-wraps it
)
```

## Running the Agent

### Using ADK Web

```bash
adk web
```

Open http://127.0.0.1:8000 and select `custom_tool_agent`.

**Test Queries:**
- "What is the status of order 12345?"
- "Check order ABC123"

### Using ADK CLI

```bash
adk run custom_tool_agent
```

## Next Steps

Continue to [11. OpenAPI Tools](../11-openapi-tools/)
