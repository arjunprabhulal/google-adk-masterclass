"""
19. Events - Real-time Streaming and Debugging

Events are the heartbeat of ADK. Every action during agent execution
emits events that you can capture for streaming UIs, debugging, and analytics.

Blog: https://arjunprabhulal.com/adk-events/

Event Flow During Agent Execution:
┌─────────────────────────────────────────────────────────────┐
│                     USER MESSAGE                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  runner.run_async()                          │
│                                                              │
│   Yields events as they happen:                              │
│                                                              │
│   ┌─────────────┐                                            │
│   │ ContentEvent│ ──► Streaming text from LLM                │
│   └─────────────┘     (partial=True while generating)        │
│          │                                                   │
│          ▼                                                   │
│   ┌─────────────┐                                            │
│   │ToolCallEvent│ ──► Agent decided to call a tool           │
│   └─────────────┘     (contains tool name and args)          │
│          │                                                   │
│          ▼                                                   │
│   ┌─────────────┐                                            │
│   │ToolResult   │ ──► Tool finished executing                │
│   │   Event     │     (contains the result)                  │
│   └─────────────┘                                            │
│          │                                                   │
│          ▼                                                   │
│   ┌─────────────┐                                            │
│   │ ContentEvent│ ──► Final response with tool result        │
│   └─────────────┘     (partial=False, complete)              │
│          │                                                   │
│          ▼                                                   │
│   ┌─────────────┐                                            │
│   │  EndEvent   │ ──► Execution complete                     │
│   └─────────────┘                                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   YOUR EVENT HANDLER                         │
│                                                              │
│   - Update UI with streaming text                            │
│   - Show "thinking..." for tool calls                        │
│   - Log for debugging                                        │
│   - Track for analytics                                      │
└─────────────────────────────────────────────────────────────┘
"""

import asyncio
from datetime import datetime
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


# ============================================================
# TOOLS (to trigger tool events)
# ============================================================

def calculate(expression: str) -> dict:
    """
    Evaluate a math expression safely.
    
    Args:
        expression: Math like "2 + 2" or "10 * 5"
    
    Returns:
        The calculation result
    """
    import ast
    import operator
    
    # Safe operators
    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
    }
    
    def safe_eval(node):
        if isinstance(node, ast.Num):  # Python 3.7
            return node.n
        elif isinstance(node, ast.Constant):  # Python 3.8+
            return node.value
        elif isinstance(node, ast.BinOp):
            left = safe_eval(node.left)
            right = safe_eval(node.right)
            return operators[type(node.op)](left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = safe_eval(node.operand)
            return operators[type(node.op)](operand)
        else:
            raise ValueError(f"Unsupported operation: {type(node)}")
    
    try:
        tree = ast.parse(expression, mode='eval')
        result = safe_eval(tree.body)
        return {"expression": expression, "result": result}
    except Exception as e:
        return {"error": str(e)}


def get_weather(city: str) -> dict:
    """
    Get weather for a city (mock data).
    
    Args:
        city: City name
    
    Returns:
        Weather information
    """
    weather = {
        "Tokyo": {"temp": "25°C", "condition": "Clear"},
        "London": {"temp": "15°C", "condition": "Cloudy"},
        "New York": {"temp": "20°C", "condition": "Sunny"},
    }
    
    data = weather.get(city, {"temp": "22°C", "condition": "Pleasant"})
    return {"city": city, **data, "time": datetime.now().strftime("%H:%M")}


# ============================================================
# AGENT
# ============================================================

root_agent = Agent(
    model="gemini-2.5-flash",
    name="event_agent",
    instruction="""You are a helpful assistant.
Use calculate for math and get_weather for weather questions.
Be concise.""",
    tools=[calculate, get_weather],
)


# ============================================================
# EVENT PROCESSOR
# ============================================================

def process_event(event, count: int) -> str:
    """Process and display an event."""
    event_type = type(event).__name__
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    
    print(f"\n  [{count}] {timestamp} | {event_type}")
    
    # Handle different event types
    if hasattr(event, 'content') and event.content:
        if hasattr(event.content, 'parts') and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, 'text') and part.text:
                    preview = part.text[:80].replace('\n', ' ')
                    print(f"      Text: {preview}...")
                elif hasattr(part, 'function_call') and part.function_call:
                    fc = part.function_call
                    if hasattr(fc, 'name'):
                        print(f"      Tool: {fc.name}({getattr(fc, 'args', {})})")
                elif hasattr(part, 'function_response') and part.function_response:
                    fr = part.function_response
                    if hasattr(fr, 'name'):
                        print(f"      Result: {fr.name} -> {getattr(fr, 'response', 'N/A')}")
    
    return event_type


# ============================================================
# DEMO
# ============================================================

async def main():
    """
    Watch events stream in real-time!
    """
    
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name="event_app",
        session_service=session_service,
    )
    
    print("=" * 60)
    print("EVENTS DEMO")
    print("=" * 60)
    print("\nWatch events stream as the agent processes requests!\n")
    
    user_id = "user_demo"
    session = await session_service.create_session(
        app_name="event_app",
        user_id=user_id,
    )
    
    # Test messages that trigger different events
    messages = [
        "What is 25 * 4?",
        "What's the weather in Tokyo?",
    ]
    
    for msg in messages:
        print("=" * 60)
        print(f"USER: {msg}")
        print("=" * 60)
        print("\nEVENTS:")
        
        content = types.Content(role="user", parts=[types.Part(text=msg)])
        
        event_count = 0
        event_types = []
        final_response = ""
        
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session.id,
            new_message=content,
        ):
            event_count += 1
            event_type = process_event(event, event_count)
            event_types.append(event_type)
            
            # Capture final text
            if hasattr(event, 'content') and event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        final_response = part.text
        
        print(f"\n  Total: {event_count} events")
        print(f"  Flow: {' → '.join(event_types)}")
        print(f"\nRESPONSE: {final_response}\n")
    
    # Summary
    print("=" * 60)
    print("EVENT CONCEPTS")
    print("=" * 60)
    print("""
┌────────────────────────────────────────────────────────────┐
│                    EVENT TYPES                              │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  ContentEvent                                               │
│    • Streaming text from the LLM                            │
│    • partial=True while generating, False when done         │
│                                                             │
│  ToolCallEvent                                              │
│    • Agent decided to call a tool                           │
│    • Contains tool name and arguments                       │
│                                                             │
│  ToolResultEvent                                            │
│    • Tool finished executing                                │
│    • Contains the return value                              │
│                                                             │
│  EndEvent                                                   │
│    • Execution completed successfully                       │
│                                                             │
│  ErrorEvent                                                 │
│    • Something went wrong                                   │
│                                                             │
└────────────────────────────────────────────────────────────┘

Why events matter:
- Streaming UIs: Show text as it generates (like ChatGPT)
- Progress: Show "thinking..." during tool calls
- Debugging: See exactly what happened step by step
- Analytics: Track tool usage, latency, errors
- Logging: Record all agent activity

Usage pattern:
    async for event in runner.run_async(...):
        if isinstance(event, ContentEvent):
            update_ui(event.content)
        elif isinstance(event, ToolCallEvent):
            show_progress("Using tool...")
    """)


if __name__ == "__main__":
    asyncio.run(main())
