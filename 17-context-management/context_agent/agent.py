"""
16. Context Management - Caching and Compression

Managing context efficiently is crucial for production agents.
This module covers two key techniques:
1. Context Caching - Store and reuse system prompts
2. Events Compaction - Summarize old messages to save tokens

Blog: https://arjunprabhulal.com/adk-context-management/

How Context Flows Through ADK:
┌─────────────────────────────────────────────────────────────┐
│                     USER MESSAGE                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   CONTEXT LAYER                              │
│                                                              │
│  ┌──────────────────┐      ┌──────────────────────────┐     │
│  │  CONTEXT CACHE   │      │   EVENTS COMPACTION      │     │
│  │                  │      │                          │     │
│  │  System Prompt   │      │  Old Messages → Summary  │     │
│  │  Tool Defs       │      │  Recent Messages Kept    │     │
│  │  (Reused)        │      │  Token Count Reduced     │     │
│  └──────────────────┘      └──────────────────────────┘     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     LLM CALL                                 │
│         (Faster with cache, cheaper with compaction)         │
└─────────────────────────────────────────────────────────────┘
"""

import asyncio
from datetime import datetime
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


# ============================================================
# AGENT
# ============================================================

root_agent = Agent(
    model="gemini-2.5-flash",
    name="context_agent",
    instruction="""You are a helpful assistant with excellent memory.
You remember everything discussed in our conversation.
When asked to recall information, be specific and accurate.""",
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
    Shows how context is maintained across conversation turns.
    
    In production, you'd add:
    - ContextCacheConfig for faster repeated calls
    - EventsCompactionConfig for long conversations
    """
    
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name="context_app",
        session_service=session_service,
    )
    
    print("=" * 60)
    print("CONTEXT MANAGEMENT DEMO")
    print("=" * 60)
    
    user_id = "user_demo"
    session = await session_service.create_session(
        app_name="context_app",
        user_id=user_id,
    )
    
    print(f"\nSession: {session.id[:8]}...")
    print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
    print("-" * 40)
    
    # Conversation that builds context
    turns = [
        ("Turn 1: Introduce yourself", 
         "Hi! I'm Sarah, a software engineer from Seattle. I love hiking and Python."),
        
        ("Turn 2: Add more details",
         "I've been coding for 8 years and currently work on machine learning projects."),
        
        ("Turn 3: Test context recall",
         "What's my name, where am I from, and what do I do for work?"),
        
        ("Turn 4: Test deeper recall",
         "What are my hobbies and how long have I been coding?"),
    ]
    
    for label, msg in turns:
        print(f"\n[{label}]")
        print(f"User: {msg}")
        response = await chat(runner, user_id, session.id, msg)
        print(f"Agent: {response}")
    
    # Summary
    print("\n" + "=" * 60)
    print("CONTEXT MANAGEMENT TECHNIQUES")
    print("=" * 60)
    print("""
┌────────────────────────────────────────────────────────────┐
│                    CONTEXT CACHING                          │
├────────────────────────────────────────────────────────────┤
│ What it does:                                               │
│   Stores system prompts and tool definitions               │
│   Reuses them across requests (no re-sending)              │
│                                                             │
│ Benefits:                                                   │
│   - Faster response times                                   │
│   - Lower costs (fewer input tokens)                        │
│                                                             │
│ Configuration:                                              │
│   ContextCacheConfig(                                       │
│       min_tokens=2048,    # Min size to trigger caching     │
│       ttl_seconds=600,    # How long to keep cache          │
│   )                                                         │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│                   EVENTS COMPACTION                         │
├────────────────────────────────────────────────────────────┤
│ What it does:                                               │
│   Summarizes old conversation messages                      │
│   Keeps recent messages intact                              │
│                                                             │
│ Benefits:                                                   │
│   - Handle very long conversations                          │
│   - Stay within token limits                                │
│   - Preserve important context                              │
│                                                             │
│ Configuration:                                              │
│   EventsCompactionConfig(                                   │
│       compaction_interval=3,  # Compress every N turns      │
│       overlap_size=1,         # Keep N turns from previous  │
│   )                                                         │
└────────────────────────────────────────────────────────────┘

When to use each:
- Caching: Agents with long instructions or many tools
- Compaction: Chat apps with extended conversations
- Both: Production agents handling heavy traffic
    """)


if __name__ == "__main__":
    asyncio.run(main())
