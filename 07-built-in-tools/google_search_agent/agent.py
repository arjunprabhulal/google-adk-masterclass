from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    model="gemini-2.5-flash",
    name="google_search_agent",
    instruction="You are a helpful google search assistant.",
    tools=[google_search],
)

