"""
20. Events

Understanding the event system in ADK agent execution.

Blog: https://arjunprabhulal.com/adk-events/

Event Structure:
┌─────────────────────────────────────────────────────────────┐
│                       EVENT PROPERTIES                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  event.author        - Who sent it ('user' or agent name)   │
│  event.id            - Unique identifier                     │
│  event.invocation_id - Tracks the interaction cycle          │
│  event.timestamp     - When it was created                   │
│  event.content       - The message payload                   │
│  event.partial       - True if streaming (incomplete)        │
│  event.actions       - Control signals (state_delta, etc.)   │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│                     HELPER METHODS                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  event.get_function_calls()     - Get tool call requests     │
│  event.get_function_responses() - Get tool results           │
│  event.is_final_response()      - Check if displayable       │
│                                                              │
└─────────────────────────────────────────────────────────────┘

Event Flow:
  User Message → runner.run_async() yields events:
    1. Text content (event.partial=True while streaming)
    2. Function calls (use get_function_calls())
    3. Function responses (use get_function_responses())
    4. Final response (is_final_response() returns True)
"""

import asyncio
from datetime import datetime
from google.adk.agents import Agent
from google.adk.events import Event, EventActions
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

    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
    }

    def safe_eval(node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.Constant):
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
        "Tokyo": {"temp": "25C", "condition": "Clear"},
        "London": {"temp": "15C", "condition": "Cloudy"},
        "New York": {"temp": "20C", "condition": "Sunny"},
    }

    data = weather.get(city, {"temp": "22C", "condition": "Pleasant"})
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
# EVENT PROCESSOR (Using Official ADK Methods)
# ============================================================

def process_event(event, count: int) -> str:
    """
    Process and display an event using official ADK methods.

    Key methods used:
    - event.get_function_calls() - Returns list of tool call requests
    - event.get_function_responses() - Returns list of tool results
    - event.is_final_response() - True if event is for user display
    """
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]

    # Event metadata
    author = getattr(event, 'author', 'unknown')
    event_id = getattr(event, 'id', 'N/A')
    is_partial = getattr(event, 'partial', False)

    print(f"\n  [{count}] {timestamp}")
    print(f"      Author: {author} | ID: {event_id[:8] if event_id != 'N/A' else 'N/A'}...")

    event_type = "unknown"

    # Check for function calls using official method
    function_calls = event.get_function_calls()
    if function_calls:
        event_type = "function_call"
        for call in function_calls:
            print(f"      Tool Call: {call.name}({call.args})")

    # Check for function responses using official method
    function_responses = event.get_function_responses()
    if function_responses:
        event_type = "function_response"
        for response in function_responses:
            print(f"      Tool Result: {response.name} -> {response.response}")

    # Check for text content
    if event.content and event.content.parts:
        for part in event.content.parts:
            if hasattr(part, 'text') and part.text:
                event_type = "text_partial" if is_partial else "text_complete"
                status = "[Streaming...]" if is_partial else "[Complete]"
                preview = part.text[:80].replace('\n', ' ')
                print(f"      {status} {preview}...")

    # Check if this is a final response
    if event.is_final_response():
        print(f"      >> Final response (displayable)")

    # Check for state changes
    if event.actions and hasattr(event.actions, 'state_delta') and event.actions.state_delta:
        print(f"      State Delta: {event.actions.state_delta}")

    return event_type


# ============================================================
# DEMO
# ============================================================

async def main():
    """
    Watch events stream in real-time using official ADK methods!
    """

    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name="event_app",
        session_service=session_service,
    )

    print("=" * 60)
    print("ADK EVENTS DEMO")
    print("=" * 60)
    print("\nWatch events stream as the agent processes requests!")
    print("Using official ADK methods: get_function_calls(),")
    print("get_function_responses(), is_final_response()\n")

    user_id = "user_demo"
    session = await session_service.create_session(
        app_name="event_app",
        user_id=user_id,
    )

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

            # Capture final response using is_final_response()
            if event.is_final_response():
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            final_response = part.text

        print(f"\n  Total: {event_count} events")
        print(f"  Flow: {' -> '.join(event_types)}")
        print(f"\nRESPONSE: {final_response}\n")

    # Summary with correct API info
    print("=" * 60)
    print("ADK EVENT API REFERENCE")
    print("=" * 60)
    print("""
┌────────────────────────────────────────────────────────────┐
│                  EVENT PROPERTIES                           │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  event.author         'user' or agent name                  │
│  event.id             Unique event identifier               │
│  event.invocation_id  Tracks interaction cycle              │
│  event.timestamp      Event creation time                   │
│  event.content        Message payload (text, parts)         │
│  event.partial        True if streaming incomplete          │
│  event.actions        Control signals                       │
│                                                             │
├────────────────────────────────────────────────────────────┤
│                  HELPER METHODS                             │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  event.get_function_calls()                                 │
│    Returns list of tool calls: call.name, call.args         │
│                                                             │
│  event.get_function_responses()                             │
│    Returns list of results: response.name, response.response│
│                                                             │
│  event.is_final_response()                                  │
│    True when event should be displayed to user              │
│                                                             │
├────────────────────────────────────────────────────────────┤
│                  EVENT ACTIONS                              │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  event.actions.state_delta      Session state changes       │
│  event.actions.artifact_delta   Artifact updates            │
│  event.actions.transfer_to_agent  Agent routing             │
│  event.actions.escalate         Terminate loops             │
│  event.actions.skip_summarization  Skip LLM processing      │
│                                                             │
└────────────────────────────────────────────────────────────┘

Usage pattern (official API):

    from google.adk.events import Event, EventActions

    async for event in runner.run_async(...):
        # Check for tool calls
        function_calls = event.get_function_calls()
        if function_calls:
            for call in function_calls:
                print(f"Calling: {call.name}({call.args})")

        # Check for tool results
        function_responses = event.get_function_responses()
        if function_responses:
            for resp in function_responses:
                print(f"Result: {resp.name} -> {resp.response}")

        # Check for displayable content
        if event.is_final_response():
            if event.content and event.content.parts:
                print(event.content.parts[0].text)

        # Check for state changes
        if event.actions and event.actions.state_delta:
            print(f"State updated: {event.actions.state_delta}")

Why events matter:
- Streaming UIs: Show text as it generates (check event.partial)
- Progress: Show status during tool calls (get_function_calls)
- Debugging: Trace with event.author, event.id
- Analytics: Track tool usage via function calls/responses
- State: Monitor changes via event.actions.state_delta
    """)


if __name__ == "__main__":
    asyncio.run(main())
