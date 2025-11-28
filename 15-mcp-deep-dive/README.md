# 15. Model Context Protocol (MCP) Deep Dive

MCP architecture, connection types, and production patterns.

**Blog Post:** [https://arjunprabhulal.com/adk-mcp-deep-dive/](https://arjunprabhulal.com/adk-mcp-deep-dive/)

## Table of Contents

1. [What is MCP?](#what-is-mcp)
2. [Prerequisites](#prerequisites)
3. [Setup Steps](#setup-steps)
4. [Connection Types](#connection-types)
5. [Running the Agent](#running-the-agent)
6. [Next Steps](#next-steps)

## What is MCP?

Model Context Protocol is a standardized way for AI agents to connect to external services and data sources. Key benefits:

- **Standardized interface** - One protocol for many services
- **Dynamic tool discovery** - Agents learn available tools at runtime
- **Secure connections** - Built-in authentication support

## Prerequisites

- Python 3.10+
- Gemini API key from [AI Studio](https://aistudio.google.com/apikey)
- GitHub Personal Access Token
- Node.js (for Firecrawl MCP - optional)

## Setup Steps

1. Navigate to this module:

```bash
cd 15-mcp-deep-dive
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

4. Set up environment variables in `mcp_agent/.env`:

```
GOOGLE_API_KEY=your-api-key-here
GITHUB_TOKEN=your-github-token
FIRECRAWL_API_KEY=your-firecrawl-api-key  # Optional
```

## Connection Types

| Type | Class | Use Case |
|------|-------|----------|
| **HTTP** | `StreamableHTTPServerParams` | Cloud-hosted MCP servers (GitHub Copilot MCP) |
| **Stdio** | `StdioConnectionParams` | Local process-based servers (npx tools) |

### HTTP Connection Example

```python
StreamableHTTPServerParams(
    url="https://api.githubcopilot.com/mcp/",
    headers={"Authorization": f"Bearer {token}"},
)
```

### Stdio Connection Example

```python
StdioConnectionParams(
    server_params=StdioServerParameters(
        command="npx",
        args=["-y", "firecrawl-mcp"],
    ),
)
```

## Running the Agent

### Using Programmatic Runner

```bash
cd mcp_agent
python agent.py
```

**Test Queries:**
- "Explain MCP and its use in ADK"
- "Find ADK repositories on GitHub"

## Next Steps

Continue to [16. Session, State & Memory](../16-sessions-state-memory/)
