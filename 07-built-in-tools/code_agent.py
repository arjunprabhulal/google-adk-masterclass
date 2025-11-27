"""
06. Built-in Tools - Code Executor

Blog: https://arjunprabhulal.com/adk-built-in-tools/
"""

from google.adk.agents import Agent
from google.adk.code_executors import BuiltInCodeExecutor

root_agent = Agent(
    model="gemini-2.5-flash",
    name="code_agent",
    instruction="""You are a Python coding assistant.
    Write and execute Python code to solve problems.
    Show your code and explain the results.""",
    code_executor=BuiltInCodeExecutor(),
)

