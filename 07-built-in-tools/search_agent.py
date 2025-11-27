"""
06. Built-in Tools - Google Search

Blog: https://arjunprabhulal.com/adk-built-in-tools/
"""

from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    model="gemini-2.5-flash",
    name="search_agent",
    instruction="""You are a helpful assistant with web search capabilities.
    Use Google Search to find current information and answer questions accurately.""",
    tools=[google_search],
)

