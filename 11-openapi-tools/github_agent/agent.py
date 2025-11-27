import os
import json
import logging
from google.adk.agents import Agent
from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset
from google.adk.tools.openapi_tool.auth.auth_helpers import token_to_scheme_credential

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("github_agent")

# 1. Define a minimal GitHub OpenAPI spec for user endpoint
GITHUB_SPEC = {
    "openapi": "3.0.0",
    "info": {"title": "GitHub API", "version": "1.0.0"},
    "servers": [{"url": "https://api.github.com"}],
    "paths": {
        "/user": {
            "get": {
                "operationId": "get_authenticated_user",
                "summary": "Get the authenticated user",
                "responses": {"200": {"description": "Success"}}
            }
        }
    }
}

# 2. Get GitHub token from environment
token = os.environ.get("GITHUB_TOKEN", "")

# 3. Create auth credentials
auth_scheme, auth_credential = token_to_scheme_credential(
    "apikey", "header", "Authorization", f"token {token}"
)

# 4. Initialize Toolset
toolset = OpenAPIToolset(
    spec_str=json.dumps(GITHUB_SPEC),
    spec_str_type="json",
    auth_scheme=auth_scheme,
    auth_credential=auth_credential
)

# 5. Create agent with toolset (ADK handles async internally)
root_agent = Agent(
    model="gemini-2.5-flash",
    name="github_agent",
    instruction="You are a GitHub assistant. Use the available tools to interact with GitHub.",
    tools=[toolset],  # Pass the toolset directly
)
