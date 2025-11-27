"""
15. Session, State & Memory Demo

This module demonstrates three key ADK concepts:
1. Session - Conversation thread with history (Events)
2. State - Temporary data within a session (shopping cart, preferences)
3. Memory - Long-term knowledge across sessions

Blog: https://arjunprabhulal.com/adk-sessions-state/
"""

import asyncio
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import ToolContext
from google.genai import types


# ============================================================
# TOOLS: Demonstrate State Management (Shopping Cart Example)
# ============================================================

def add_to_cart(item: str, quantity: int, tool_context: ToolContext) -> dict:
    """
    Add an item to the shopping cart.
    
    Args:
        item (str): The item name to add.
        quantity (int): Number of items to add.
        tool_context (ToolContext): The tool context with session access.
    
    Returns:
        dict: Confirmation of the added item.
    """
    state = tool_context.state
    
    # Initialize cart if not exists
    if "cart" not in state:
        state["cart"] = {}
    
    # Add item to cart
    if item in state["cart"]:
        state["cart"][item] += quantity
    else:
        state["cart"][item] = quantity
    
    return {
        "status": "success",
        "message": f"Added {quantity} {item}(s) to cart",
        "cart": state["cart"]
    }


def get_cart(tool_context: ToolContext) -> dict:
    """
    Get the current shopping cart contents.
    
    Args:
        tool_context (ToolContext): The tool context with session access.
    
    Returns:
        dict: Current cart contents.
    """
    state = tool_context.state
    cart = state.get("cart", {})
    
    return {
        "cart": cart,
        "total_items": sum(cart.values()) if cart else 0
    }


def clear_cart(tool_context: ToolContext) -> dict:
    """
    Clear all items from the shopping cart.
    
    Args:
        tool_context (ToolContext): The tool context with session access.
    
    Returns:
        dict: Confirmation message.
    """
    state = tool_context.state
    state["cart"] = {}
    return {"status": "success", "message": "Cart cleared"}


def save_preference(key: str, value: str, tool_context: ToolContext) -> dict:
    """
    Save a user preference (persists across sessions for same user).
    
    Args:
        key (str): Preference name (e.g., 'favorite_color', 'shipping_address').
        value (str): Preference value.
        tool_context (ToolContext): The tool context with session access.
    
    Returns:
        dict: Confirmation message.
    """
    state = tool_context.state
    # Use 'user:' prefix for user-scoped state (persists across sessions)
    state[f"user:{key}"] = value
    return {"status": "success", "message": f"Saved preference: {key} = {value}"}


def get_preference(key: str, tool_context: ToolContext) -> dict:
    """
    Get a saved user preference.
    
    Args:
        key (str): Preference name to retrieve.
        tool_context (ToolContext): The tool context with session access.
    
    Returns:
        dict: The preference value or not found message.
    """
    state = tool_context.state
    value = state.get(f"user:{key}")
    if value:
        return {"status": "success", "key": key, "value": value}
    return {"status": "not_found", "message": f"No preference found for '{key}'"}


# ============================================================
# AGENT: Shopping Assistant with State Management
# ============================================================

root_agent = Agent(
    model="gemini-2.5-flash",
    name="shopping_assistant",
    instruction="""You are a helpful shopping assistant. You can:
1. Remember what users tell you during the conversation (Session)
2. Manage a shopping cart using add_to_cart, get_cart, clear_cart (State)
3. Save and retrieve user preferences using save_preference, get_preference (User State)

Be friendly and helpful. When users add items, confirm what was added.
When they ask about their cart, show the contents clearly.""",
    tools=[add_to_cart, get_cart, clear_cart, save_preference, get_preference],
)


# ============================================================
# DEMO: Multi-turn conversation showing Session & State
# ============================================================

async def chat(runner: Runner, user_id: str, session_id: str, message: str) -> str:
    """Send a message and get a response."""
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


async def main():
    """
    Demonstrates Session, State & Memory concepts:
    
    - USER_ID: Identifies the user (e.g., "user_alice", "user_bob")
    - SESSION_ID: Identifies a conversation thread (auto-generated)
    - STATE: Shopping cart persists within the session
    """
    
    # Initialize services
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name="shopping_app",
        session_service=session_service,
    )
    
    # ========================================
    # DEMO 1: Session - Conversation Memory
    # ========================================
    print("=" * 60)
    print("DEMO 1: SESSION - Conversation Memory")
    print("=" * 60)
    
    user_id = "user_alice"
    session = await session_service.create_session(
        app_name="shopping_app",
        user_id=user_id,
    )
    session_id = session.id
    
    print(f"\nUser ID: {user_id}")
    print(f"Session ID: {session_id[:8]}...")
    print("-" * 40)
    
    # Multi-turn conversation - agent remembers context
    conversations = [
        "Hi! My name is Alice and I'm looking for birthday gifts.",
        "What's my name and what am I shopping for?",
    ]
    
    for msg in conversations:
        print(f"\nUser: {msg}")
        response = await chat(runner, user_id, session_id, msg)
        print(f"Agent: {response}")
    
    # ========================================
    # DEMO 2: State - Shopping Cart
    # ========================================
    print("\n" + "=" * 60)
    print("DEMO 2: STATE - Shopping Cart Management")
    print("=" * 60)
    
    cart_conversations = [
        "Add 2 books and 1 puzzle to my cart",
        "Also add 3 candles",
        "What's in my cart now?",
    ]
    
    for msg in cart_conversations:
        print(f"\nUser: {msg}")
        response = await chat(runner, user_id, session_id, msg)
        print(f"Agent: {response}")
    
    # ========================================
    # DEMO 3: New Session - State Reset
    # ========================================
    print("\n" + "=" * 60)
    print("DEMO 3: NEW SESSION - Cart Resets")
    print("=" * 60)
    
    # Create a NEW session for the same user
    new_session = await session_service.create_session(
        app_name="shopping_app",
        user_id=user_id,
    )
    new_session_id = new_session.id
    
    print(f"\nSame User: {user_id}")
    print(f"NEW Session ID: {new_session_id[:8]}...")
    print("-" * 40)
    
    print("\nUser: What's in my cart?")
    response = await chat(runner, user_id, new_session_id, "What's in my cart?")
    print(f"Agent: {response}")
    print("\n(Cart is empty because it's a new session!)")
    
    # ========================================
    # DEMO 4: Different User
    # ========================================
    print("\n" + "=" * 60)
    print("DEMO 4: DIFFERENT USER - Separate Context")
    print("=" * 60)
    
    bob_user_id = "user_bob"
    bob_session = await session_service.create_session(
        app_name="shopping_app",
        user_id=bob_user_id,
    )
    
    print(f"\nUser ID: {bob_user_id}")
    print(f"Session ID: {bob_session.id[:8]}...")
    print("-" * 40)
    
    print("\nUser: Hi, I'm Bob. Add 5 headphones to my cart.")
    response = await chat(runner, bob_user_id, bob_session.id, 
                         "Hi, I'm Bob. Add 5 headphones to my cart.")
    print(f"Agent: {response}")
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("""
- SESSION: Each conversation has a unique session_id
  -> Conversation history (Events) is preserved within a session
  
- STATE: Temporary data like shopping cart
  -> Resets when a new session starts
  -> Use 'user:' prefix for cross-session persistence
  
- USER_ID: Identifies the user across sessions
  -> Different users have completely separate contexts
    """)


if __name__ == "__main__":
    asyncio.run(main())
