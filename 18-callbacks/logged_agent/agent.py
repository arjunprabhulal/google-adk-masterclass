"""
17. Callbacks - Intercepting Agent Behavior

Callbacks let you hook into the agent execution pipeline.
You can log, modify, or block requests and responses at key points.

Blog: https://arjunprabhulal.com/adk-callbacks/

Callback Execution Flow:
┌─────────────────────────────────────────────────────────────┐
│                     USER MESSAGE                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│               before_agent_callback                          │
│   (Runs once at the start of request handling)               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│               before_model_callback                          │
│   (Runs before each LLM call - may happen multiple times)    │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      LLM CALL                                │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│               after_model_callback                           │
│   (Runs after each LLM response)                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ Tool needed?  │
                    └───────────────┘
                      │           │
                     Yes          No
                      │           │
                      ▼           │
┌─────────────────────────────────────────────────────────────┐
│               before_tool_callback                           │
│   (Validate args, add auth, block tools)                     │
└─────────────────────────────────────────────────────────────┘
                      │           │
                      ▼           │
┌─────────────────────────────────────────────────────────────┐
│                    TOOL EXECUTION                            │
└─────────────────────────────────────────────────────────────┘
                      │           │
                      ▼           │
┌─────────────────────────────────────────────────────────────┐
│               after_tool_callback                            │
│   (Log results, transform, cache)                            │
└─────────────────────────────────────────────────────────────┘
                      │           │
                      └─────┬─────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│               after_agent_callback                           │
│   (Runs once at the end - cleanup, metrics)                  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   FINAL RESPONSE                             │
└─────────────────────────────────────────────────────────────┘

Return Value Rule:
- Return None  → Continue normally
- Return value → Skip the step, use your value instead
"""

import asyncio
import logging
from datetime import datetime
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Setup logging to see callbacks in action
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("callbacks")


# ============================================================
# CALLBACK FUNCTIONS
# ============================================================

def logging_before_model(
    callback_context: CallbackContext,
    llm_request
) -> None:
    """
    Runs BEFORE each LLM call.
    Use for: logging, prompt modification, request blocking.
    """
    logger.info(f"[BEFORE MODEL] Agent: {callback_context.agent_name}")
    
    # Log message count
    if hasattr(llm_request, 'contents') and llm_request.contents:
        logger.info(f"[BEFORE MODEL] Messages: {len(llm_request.contents)}")
    
    return None  # Continue with original request


def logging_after_model(
    callback_context: CallbackContext,
    llm_response
) -> None:
    """
    Runs AFTER each LLM response.
    Use for: logging, content filtering, response modification.
    """
    logger.info(f"[AFTER MODEL] Agent: {callback_context.agent_name}")
    logger.info(f"[AFTER MODEL] Response received")
    
    return None  # Continue with original response


# ============================================================
# TOOL FOR DEMO
# ============================================================

def get_time() -> dict:
    """Returns the current time."""
    now = datetime.now()
    return {
        "time": now.strftime("%H:%M:%S"),
        "date": now.strftime("%Y-%m-%d"),
        "day": now.strftime("%A")
    }


# ============================================================
# AGENT WITH CALLBACKS
# ============================================================

root_agent = Agent(
    model="gemini-2.5-flash",
    name="callback_agent",
    instruction="""You are a helpful assistant.
You can tell the current time using the get_time tool.
Be concise.""",
    tools=[get_time],
    before_model_callback=logging_before_model,
    after_model_callback=logging_after_model,
)


# ============================================================
# CHAT HELPER
# ============================================================

async def chat(runner: Runner, user_id: str, session_id: str, message: str) -> str:
    """Send a message and collect the response."""
    content = types.Content(role="user", parts=[types.Part(text=message)])
    
    response_text = ""
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    ):
        if hasattr(event, 'content') and event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, 'text') and part.text:
                    response_text += part.text
    
    return response_text


# ============================================================
# DEMO
# ============================================================

async def main():
    """
    Watch the logs to see callbacks firing at each stage!
    """
    
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name="callback_app",
        session_service=session_service,
    )
    
    print("=" * 60)
    print("CALLBACKS DEMO")
    print("=" * 60)
    print("\nWatch the logs to see callbacks in action!\n")
    
    user_id = "user_demo"
    session = await session_service.create_session(
        app_name="callback_app",
        user_id=user_id,
    )
    
    print(f"Session: {session.id[:8]}...")
    print("-" * 40)
    
    # Test conversations
    turns = [
        ("Simple question", "Hello! What's your name?"),
        ("Tool call", "What time is it?"),
    ]
    
    for label, msg in turns:
        print(f"\n[{label}]")
        print(f"User: {msg}")
        print("--- Callbacks firing ---")
        response = await chat(runner, user_id, session.id, msg)
        print(f"Agent: {response}")
    
    # Summary
    print("\n" + "=" * 60)
    print("CALLBACK REFERENCE")
    print("=" * 60)
    print("""
┌────────────────────────────────────────────────────────────┐
│                   ALL 6 CALLBACKS                           │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  AGENT-LEVEL (wrap entire request):                         │
│  ─────────────────────────────────                          │
│  before_agent_callback  → Setup, auth checks                │
│  after_agent_callback   → Cleanup, metrics                  │
│                                                             │
│  MODEL-LEVEL (each LLM call):                               │
│  ─────────────────────────────                              │
│  before_model_callback  → Modify prompts, inject context    │
│  after_model_callback   → Filter output, transform          │
│                                                             │
│  TOOL-LEVEL (each tool execution):                          │
│  ─────────────────────────────────                          │
│  before_tool_callback   → Validate args, add auth           │
│  after_tool_callback    → Cache results, transform          │
│                                                             │
└────────────────────────────────────────────────────────────┘

Return value rule:
- Return None  → Continue normally
- Return value → Skip the step, use your value

Common patterns:
- Observability: Log all interactions
- Guardrails: Block harmful content
- Caching: Skip LLM for repeated queries
- Metrics: Track latency and costs
    """)


if __name__ == "__main__":
    asyncio.run(main())
