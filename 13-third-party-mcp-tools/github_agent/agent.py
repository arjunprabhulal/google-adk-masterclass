"""
13. Third-Party MCP Tools - Connecting to External Services

MCP (Model Context Protocol) is an open standard that lets agents
connect to external services through a unified interface.

Think of it as a universal adapter - one protocol works with
GitHub, Slack, databases, web scrapers, and hundreds more.

Blog: https://arjunprabhulal.com/adk-third-party-tools-github/

How MCP Works:
┌─────────────────────────────────────────────────────────────┐
│                     YOUR AGENT                               │
│                                                              │
│   ┌─────────────────────────────────────────────────────┐   │
│   │                  MCPToolset                          │   │
│   │                                                      │   │
│   │   Handles:                                           │   │
│   │   - Connection management                            │   │
│   │   - Tool discovery (automatic!)                      │   │
│   │   - Request/response serialization                   │   │
│   │   - Error handling                                   │   │
│   └─────────────────────────────────────────────────────┘   │
│                            │                                 │
└────────────────────────────│─────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    MCP SERVERS                               │
│                                                              │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│   │  GitHub  │  │  Slack   │  │ Firecrawl│  │ Database │   │
│   │   MCP    │  │   MCP    │  │   MCP    │  │   MCP    │   │
│   └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                              │
│   Each server exposes:                                       │
│   - Tools (functions to call)                                │
│   - Resources (data to read)                                 │
│   - Prompts (templates)                                      │
└─────────────────────────────────────────────────────────────┘

Connection Types:
- HTTP (StreamableHTTPServerParams): Cloud-hosted MCP servers
- Stdio (StdioConnectionParams): Local MCP servers (npm packages)
"""

import asyncio
import os
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")


# ============================================================
# AGENT WITH GITHUB MCP
# ============================================================

root_agent = Agent(
    model="gemini-2.5-flash",
    name="github_agent",
    instruction="""You are a helpful assistant with access to GitHub via MCP.

You can:
- Search repositories
- Get file contents
- List issues and pull requests
- View repository information

When asked about a repo, use your GitHub tools to fetch real data.""",
    tools=[
        MCPToolset(
            connection_params=StreamableHTTPServerParams(
                url="https://api.githubcopilot.com/mcp/",
                headers={
                    "Authorization": f"Bearer {GITHUB_TOKEN}",
                    "X-MCP-Toolsets": "all",
                    "X-MCP-Readonly": "true"
                },
            ),
        )
    ],
)


# ============================================================
# CHAT HELPER
# ============================================================

async def chat(runner: Runner, user_id: str, session_id: str, message: str) -> str:
    """Send a message and collect the response."""
    content = types.Content(role="user", parts=[types.Part(text=message)])
    
    response_text = ""
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    ):
        if hasattr(event, 'content') and event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, 'text') and part.text:
                    response_text += part.text
    
    return response_text


# ============================================================
# DEMO
# ============================================================

async def main():
    """
    Demo: Query GitHub using MCP tools.
    
    Note: Requires GITHUB_TOKEN environment variable.
    Get one at: https://github.com/settings/tokens
    """
    
    if not GITHUB_TOKEN:
        print("=" * 60)
        print("GITHUB MCP DEMO")
        print("=" * 60)
        print("""
ERROR: GITHUB_TOKEN not set!

To run this demo:
1. Create a GitHub Personal Access Token:
   https://github.com/settings/tokens
   
2. Set the environment variable:
   export GITHUB_TOKEN="your_token_here"
   
3. Run again:
   python agent.py
        """)
        return
    
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name="github_app",
        session_service=session_service,
    )
    
    print("=" * 60)
    print("GITHUB MCP DEMO")
    print("=" * 60)
    print("\nConnecting to GitHub via MCP...")
    print("(Tools are discovered automatically!)\n")
    
    user_id = "user_demo"
    session = await session_service.create_session(
        app_name="github_app",
        user_id=user_id,
    )
    
    # Example queries
    queries = [
        "What is the google/adk-python repository about?",
        "How many stars does it have?",
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"[Query {i}]")
        print(f"User: {query}")
        response = await chat(runner, user_id, session.id, query)
        print(f"Agent: {response}\n")
    
    print("=" * 60)
    print("MCP CONCEPTS")
    print("=" * 60)
    print("""
WHY MCP?
- One protocol for many services (GitHub, Slack, DBs, etc.)
- Tools discovered automatically at runtime
- Standardized auth and error handling
- Switch services without changing agent code

CONNECTION TYPES:
┌────────────────────────────────────────────────────────────┐
│ StreamableHTTPServerParams (HTTP)                          │
│   - For cloud-hosted MCP servers                           │
│   - Example: GitHub Copilot MCP, hosted APIs               │
│   - Pass auth via headers                                  │
├────────────────────────────────────────────────────────────┤
│ StdioConnectionParams (Local)                              │
│   - For npm-based MCP servers                              │
│   - Runs as a child process                                │
│   - Example: npx firecrawl-mcp                             │
└────────────────────────────────────────────────────────────┘

MCP PRIMITIVES:
- Tools: Functions the agent can call
- Resources: Read-only data (files, schemas)
- Prompts: Pre-defined templates
    """)


if __name__ == "__main__":
    asyncio.run(main())
