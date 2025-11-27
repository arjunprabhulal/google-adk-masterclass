from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool
from google.adk.code_executors import BuiltInCodeExecutor


def get_local_time(timezone: str) -> dict:
    """
    Returns current time for a given timezone.
    
    Args:
        timezone (str): The timezone name (e.g., 'America/New_York', 'Asia/Tokyo').
    
    Returns:
        dict: Current time in the specified timezone.
    """
    from datetime import datetime
    import pytz
    try:
        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return {"status": "success", "timezone": timezone, "current_time": current_time}
    except Exception as e:
        return {"status": "error", "message": f"Invalid timezone: {timezone}"}


# Create separate agents for built-in tools
search_agent = Agent(
    model='gemini-2.5-flash',
    name='SearchAgent',
    instruction="You are a specialist in web search. Use Google Search to find information.",
    tools=[google_search],
)

code_agent = Agent(
    model='gemini-2.5-flash',
    name='CodeAgent',
    instruction="You are a specialist in code execution. Write and run Python code for calculations.",
    code_executor=BuiltInCodeExecutor(),
)

# Create the Multi-Tool Agent using AgentTool
root_agent = Agent(
    model='gemini-2.5-flash',
    name='SuperAssistant',
    instruction="""You are a versatile assistant with access to multiple capabilities:
- Use SearchAgent for real-time web information (news, weather, facts).
- Use CodeAgent for complex math, data analysis, or code execution.
- Use get_local_time for timezone queries.

Analyze the user's request and choose the appropriate tool(s).""",
    tools=[AgentTool(agent=search_agent), AgentTool(agent=code_agent), get_local_time],
)

