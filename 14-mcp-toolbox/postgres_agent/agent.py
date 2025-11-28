"""
14. MCP Toolbox for Databases - PostgreSQL

Connect ADK agents to PostgreSQL databases using MCP Toolbox.

Blog: https://arjunprabhulal.com/adk-mcp-toolbox/

Prerequisites:
1. Start MCP Toolbox server: toolbox --tools-file ../tools.yaml --port 5050
2. Ensure PostgreSQL is running with sample data
3. Set GOOGLE_API_KEY in .env
"""

import os
from google.adk.agents import Agent
from toolbox_core import ToolboxSyncClient
from dotenv import load_dotenv

load_dotenv()

# Connect to the MCP Toolbox server
TOOLBOX_URL = os.getenv("TOOLBOX_URL", "http://localhost:5050")

try:
    toolbox_client = ToolboxSyncClient(TOOLBOX_URL)
    db_tools = toolbox_client.load_toolset("ecommerce")
    print(f"Loaded {len(db_tools)} tools from MCP Toolbox")
except Exception as e:
    print(f"WARNING: Could not connect to MCP Toolbox at {TOOLBOX_URL}")
    print(f"Error: {e}")
    print("Make sure the Toolbox server is running: toolbox --tools-file ../tools.yaml")
    db_tools = []


root_agent = Agent(
    model="gemini-2.5-flash",
    name="postgres_data_agent",
    description="A data analysis agent for PostgreSQL e-commerce database",
    instruction="""You are a database analyst assistant with access to an e-commerce PostgreSQL database.

You can help users:
- Query product information and inventory
- Look up customer data
- Calculate inventory metrics and values
- Search products by category

Use the database tools to fetch real data. Present results clearly.""",
    tools=db_tools,
)
