"""
05. Workflow Agents - Loop Pattern

Repeat agent execution until a condition is met or max iterations reached.
Best for iterative refinement tasks.

Blog: https://arjunprabhulal.com/adk-workflow-sequential-loop-parallel/
"""

from google.adk.agents import Agent, LoopAgent

# Refiner agent - runs repeatedly until satisfied
refiner = Agent(
    model="gemini-2.5-flash",
    name="refiner",
    instruction="""Review and improve the content.
    If the quality is satisfactory, respond with 'DONE'.
    Otherwise, provide an improved version.""",
)

# Loop until done or max iterations reached
root_agent = LoopAgent(
    name="refinement_loop",
    sub_agents=[refiner],
    max_iterations=5,
)

