"""
05. Workflow Agents - Parallel Pattern

Execute agents simultaneously for independent tasks.
Best for batch processing where tasks don't depend on each other.

Blog: https://arjunprabhulal.com/adk-workflow-sequential-loop-parallel/
"""

from google.adk.agents import Agent, ParallelAgent

# Parallel analysts - all run at the same time
market_analyst = Agent(
    model="gemini-2.5-flash",
    name="market_analyst",
    instruction="Analyze market trends and opportunities.",
)

tech_analyst = Agent(
    model="gemini-2.5-flash",
    name="tech_analyst",
    instruction="Analyze technology landscape and innovations.",
)

risk_analyst = Agent(
    model="gemini-2.5-flash",
    name="risk_analyst",
    instruction="Identify potential risks and mitigation strategies.",
)

# Parallel Execution: All analysts run simultaneously
root_agent = ParallelAgent(
    name="analysis_team",
    sub_agents=[market_analyst, tech_analyst, risk_analyst],
)

