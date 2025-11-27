"""
Programmatic Agent Setup Example

This script demonstrates how to run an ADK agent programmatically using:
- Runner class for agent execution
- InMemorySessionService for session management
- Async event processing for streaming responses

Usage:
    python run_agent.py
"""

import asyncio
import os
from google.genai import types
from google.adk.agents.llm_agent import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

# Load environment variables
from dotenv import load_dotenv
load_dotenv()


async def main():
    # 1. Create session service
    session_service = InMemorySessionService()
    
    # 2. Create a session
    session = await session_service.create_session(
        state={}, 
        app_name='demo_app', 
        user_id='demo_user'
    )
    
    # 3. Create agent
    agent = Agent(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        name='root_agent',
        description='A helpful assistant for user questions.',
        instruction='Answer user questions to the best of your knowledge',
    )
    
    # 4. Create runner
    runner = Runner(
        app_name='demo_app',
        agent=agent,
        session_service=session_service,
    )
    
    # 5. Format user input
    query = "What is the Transformers architecture in AI? Be brief."
    print(f"User: {query}\n")
    print("Agent: ", end="", flush=True)
    
    content = types.Content(
        role='user', 
        parts=[types.Part(text=query)]
    )
    
    # 6. Run agent and process events
    events_async = runner.run_async(
        session_id=session.id,
        user_id=session.user_id,
        new_message=content
    )
    
    # 7. Process events and extract response text (streaming)
    async for event in events_async:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(part.text, end="", flush=True)
    
    print()  # New line after response


if __name__ == "__main__":
    asyncio.run(main())
