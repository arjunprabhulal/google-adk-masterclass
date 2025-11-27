from google.adk.agents import Agent

# Specialist agents
researcher = Agent(
    model="gemini-2.5-flash",
    name="researcher",
    instruction="Research topics thoroughly and provide detailed findings.",
)

writer = Agent(
    model="gemini-2.5-flash",
    name="writer",
    instruction="Write clear, engaging content based on research.",
)

reviewer = Agent(
    model="gemini-2.5-flash",
    name="reviewer",
    instruction="Review content for accuracy and quality.",
)

# Coordinator agent
root_agent = Agent(
    model="gemini-2.5-flash",
    name="coordinator",
    instruction="""You are a project coordinator managing a team of specialists.

Your team:
- researcher: For gathering information
- writer: For creating content
- reviewer: For quality checks

Delegate tasks appropriately and synthesize results.""",
    sub_agents=[researcher, writer, reviewer],
)
