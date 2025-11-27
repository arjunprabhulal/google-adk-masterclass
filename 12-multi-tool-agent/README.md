# 12. Multi-Tool Agent

Combining multiple tools in a single agent.

**Blog Post:** [https://arjunprabhulal.com/adk-multi-tool-agent/](https://arjunprabhulal.com/adk-multi-tool-agent/)

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Setup Steps](#setup-steps)
4. [Tool Combination Patterns](#tool-combination-patterns)
5. [Running the Agent](#running-the-agent)
6. [Next Steps](#next-steps)

## Overview

Multi-tool agents combine different types of tools:

- Custom function tools
- Built-in tools (Google Search, Code Executor)
- Other agents as tools (AgentTool)

## Prerequisites

- Python 3.10+
- Gemini API key from [AI Studio](https://aistudio.google.com/apikey)

## Setup Steps

1. Navigate to this module:

```bash
cd 12-multi-tool-agent
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r ../requirements.txt
pip install pytz  # For timezone tool
```

4. Set up environment variables in `super_assistant/.env`:

```
GOOGLE_API_KEY=your-api-key-here
```

## Tool Combination Patterns

```python
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool

# Wrap specialist agents as tools
search_tool = AgentTool(agent=search_agent)
code_tool = AgentTool(agent=code_agent)

# Combine with custom functions
agent = Agent(
    tools=[search_tool, code_tool, get_local_time],
)
```

## Running the Agent

### Using ADK Web

```bash
adk web
```

Open http://127.0.0.1:8000 and select `super_assistant`.

**Test Queries:**
- "What time is it in Tokyo?"
- "Search for the latest Python news"
- "Calculate 15% of 250"

### Using ADK CLI

```bash
adk run super_assistant
```

## Next Steps

Continue to [13. Third-Party MCP Tools](../13-third-party-mcp-tools/)
