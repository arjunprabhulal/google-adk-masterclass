"""
05. Workflow Agents - Sequential Pattern

Execute agents one after another, passing output to the next step.
Best for multi-step pipelines where each step depends on the previous one.

Blog: https://arjunprabhulal.com/adk-workflow-sequential-loop-parallel/
"""

from google.adk.agents import Agent, SequentialAgent

# Step 1: Research
researcher = Agent(
    model="gemini-2.5-flash",
    name="researcher",
    instruction="Research the given topic and provide key findings.",
)

# Step 2: Write
writer = Agent(
    model="gemini-2.5-flash",
    name="writer",
    instruction="Take the research findings and write a clear summary.",
)

# Step 3: Edit
editor = Agent(
    model="gemini-2.5-flash",
    name="editor",
    instruction="Review and polish the summary for clarity and grammar.",
)

# Sequential Pipeline: Research → Write → Edit
root_agent = SequentialAgent(
    name="content_pipeline",
    sub_agents=[researcher, writer, editor],
)

