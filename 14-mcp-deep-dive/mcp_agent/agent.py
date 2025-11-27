"""
14. MCP Deep Dive - Advanced Patterns and Multi-MCP

This module goes deeper into MCP, showing how to:
- Use multiple MCP servers together
- Handle different connection types
- Build production-ready MCP agents

Blog: https://arjunprabhulal.com/adk-mcp-deep-dive/

Multi-MCP Architecture:
┌─────────────────────────────────────────────────────────────┐
│                    RESEARCH AGENT                            │
│                                                              │
│   "Analyze the google/adk-python repo and find related      │
│    tutorials on the web"                                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┴───────────────┐
            │                               │
            ▼                               ▼
┌───────────────────────┐     ┌───────────────────────┐
│     GITHUB MCP        │     │    FIRECRAWL MCP      │
│                       │     │                       │
│  - Get repo info      │     │  - Scrape web pages   │
│  - Read files         │     │  - Extract content    │
│  - List issues        │     │  - Search the web     │
│                       │     │                       │
│  (HTTP Connection)    │     │  (Stdio Connection)   │
└───────────────────────┘     └───────────────────────┘
            │                               │
            └───────────────┬───────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   COMBINED RESPONSE                          │
│                                                              │
│   Agent synthesizes data from both sources into a           │
│   comprehensive answer                                       │
└─────────────────────────────────────────────────────────────┘

Connection Types Comparison:
┌────────────────────────────────────────────────────────────┐
│  HTTP (StreamableHTTPServerParams)                         │
│  ──────────────────────────────────                        │
│  - Cloud-hosted MCP servers                                │
│  - Production deployments                                  │
│  - Auth via headers                                        │
│  - Example: GitHub Copilot MCP                             │
├────────────────────────────────────────────────────────────┤
│  Stdio (StdioConnectionParams)                             │
│  ──────────────────────────────                            │
│  - Local MCP servers (npm packages)                        │
│  - Development and testing                                 │
│  - Runs as child process                                   │
│  - Example: npx firecrawl-mcp                              │
└────────────────────────────────────────────────────────────┘
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
# SINGLE MCP AGENT (GitHub)
# ============================================================

root_agent = Agent(
    model="gemini-2.5-flash",
    name="mcp_agent",
    instruction="""You are a code analysis assistant with GitHub access.

When analyzing repositories:
1. Fetch the repo's README and key files
2. Understand the project structure
3. Identify main features and technologies
4. Provide insights and recommendations

Be thorough and cite specific files when relevant.""",
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
    Demo: Advanced MCP usage with GitHub.
    
    For multi-MCP (GitHub + Firecrawl), you would add:
    
    from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
    from mcp import StdioServerParameters
    
    firecrawl_mcp = MCPToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="npx",
                args=["-y", "firecrawl-mcp"],
                env={"FIRECRAWL_API_KEY": os.environ.get("FIRECRAWL_API_KEY")}
            ),
        ),
    )
    
    Then pass both to the agent:
    tools=[github_mcp, firecrawl_mcp]
    """
    
    if not GITHUB_TOKEN:
        print("=" * 60)
        print("MCP DEEP DIVE DEMO")
        print("=" * 60)
        print("""
ERROR: GITHUB_TOKEN not set!

To run this demo:
1. Get a GitHub token: https://github.com/settings/tokens
2. Set it: export GITHUB_TOKEN="your_token"
3. Run: python agent.py
        """)
        return
    
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name="mcp_app",
        session_service=session_service,
    )
    
    print("=" * 60)
    print("MCP DEEP DIVE DEMO")
    print("=" * 60)
    
    user_id = "user_demo"
    session = await session_service.create_session(
        app_name="mcp_app",
        user_id=user_id,
    )
    
    print(f"\nSession: {session.id[:8]}...")
    print("-" * 40)
    
    # Code analysis query
    query = "Analyze the google/adk-python repository. What are its main features?"
    print(f"\nUser: {query}")
    print("\n(Fetching from GitHub via MCP...)\n")
    
    response = await chat(runner, user_id, session.id, query)
    print(f"Agent: {response}")
    
    print("\n" + "=" * 60)
    print("ADVANCED MCP PATTERNS")
    print("=" * 60)
    print("""
1. MULTI-MCP AGENTS
   Combine multiple MCP servers in one agent:
   
   tools=[
       MCPToolset(github_params),   # Code analysis
       MCPToolset(firecrawl_params), # Web scraping
       MCPToolset(slack_params),     # Notifications
   ]

2. DYNAMIC TOOL DISCOVERY
   MCP tools are discovered at runtime. The agent
   automatically learns what's available.

3. ERROR HANDLING
   MCPToolset handles connection errors, timeouts,
   and retries automatically.

4. AUTHENTICATION PATTERNS
   - HTTP: Pass tokens in headers
   - Stdio: Pass via env variables

5. BEST PRACTICES
   - Use readonly mode when possible
   - Limit toolsets to what you need
   - Handle token expiration gracefully
   - Log MCP calls for debugging
    """)


if __name__ == "__main__":
    asyncio.run(main())
