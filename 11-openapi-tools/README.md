# 11. OpenAPI Tools

REST API integration using OpenAPI specifications.

**Blog Post:** [https://arjunprabhulal.com/adk-custom-tools-openapi/](https://arjunprabhulal.com/adk-custom-tools-openapi/)

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Setup Steps](#setup-steps)
4. [How It Works](#how-it-works)
5. [Running the Agent](#running-the-agent)
6. [Next Steps](#next-steps)

## Overview

OpenAPI tools allow agents to call REST APIs defined by OpenAPI/Swagger specifications. ADK automatically generates tools from the spec.

## Prerequisites

- Python 3.10+
- Gemini API key from [AI Studio](https://aistudio.google.com/apikey)
- GitHub Personal Access Token (for the example)

## Setup Steps

1. Navigate to this module:

```bash
cd 11-openapi-tools
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

4. Set up environment variables in `github_agent/.env`:

```
GOOGLE_API_KEY=your-api-key-here
GITHUB_TOKEN=your-github-token
```

## How It Works

1. **Define the OpenAPI spec** - JSON or YAML format
2. **Create OpenAPIToolset** - Pass the spec and auth credentials
3. **Add to agent** - Pass the toolset to the agent's `tools` list

```python
from google.adk.tools.openapi_tool.openapi_toolset import OpenAPIToolset

toolset = OpenAPIToolset(
    spec_str=json.dumps(GITHUB_SPEC),
    spec_str_type="json",
    auth_scheme=auth_scheme,
    auth_credential=auth_credential
)

agent = Agent(tools=[toolset])
```

## Running the Agent

### Using ADK Web

```bash
adk web
```

Open http://127.0.0.1:8000 and select `github_agent`.

**Test Queries:**
- "Get my GitHub user info"
- "Who am I on GitHub?"

### Using ADK CLI

```bash
adk run github_agent
```

## Next Steps

Continue to [12. Multi-Tool Agent](../12-multi-tool-agent/)
