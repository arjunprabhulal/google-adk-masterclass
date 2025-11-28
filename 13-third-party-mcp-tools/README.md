# 13. Third-Party MCP Tools

GitHub and Firecrawl integration via Model Context Protocol.

**Blog Post:** [https://arjunprabhulal.com/adk-third-party-tools-github/](https://arjunprabhulal.com/adk-third-party-tools-github/)

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Setup Steps](#setup-steps)
4. [GitHub MCP Setup](#github-mcp-setup)
5. [Running the Agent](#running-the-agent)
6. [Next Steps](#next-steps)

## Overview

Model Context Protocol (MCP) enables agents to connect to external services through a standardized interface. This module demonstrates GitHub integration.

## Prerequisites

- Python 3.10+
- Gemini API key from [AI Studio](https://aistudio.google.com/apikey)
- GitHub Personal Access Token

## Setup Steps

1. Navigate to this module:

```bash
cd 13-third-party-mcp-tools
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

## GitHub MCP Setup

1. **Create a GitHub token:**
   - Go to github.com/settings/tokens
   - Generate a new token with `repo` scope

2. **Configure MCPToolset:**

```python
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams

github_mcp = MCPToolset(
    connection_params=StreamableHTTPServerParams(
        url="https://api.githubcopilot.com/mcp/",
        headers={"Authorization": f"Bearer {GITHUB_TOKEN}"},
    ),
)
```

## Running the Agent

### Using Programmatic Runner

```bash
cd github_agent
python agent.py
```

### Using ADK Web

```bash
adk web
```

**Test Queries:**
- "List trending Python repositories"
- "Get the README from google/adk-python"

## Next Steps

Continue to [14. MCP Toolbox for Databases](../14-mcp-toolbox/)
