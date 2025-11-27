from google.adk.agents import Agent


def get_order_status(order_id: str) -> dict:
    """
    Retrieves the status of an order by order ID.
    
    Args:
        order_id (str): The unique order identifier.
    
    Returns:
        dict: Order status information including status and delivery date.
    """
    # In a real scenario, this would query a database or API.
    return {
        "status": "success",
        "order_id": order_id,
        "order_status": "Shipped",
        "delivery_date": "Nov 24, 2025"
    }


root_agent = Agent(
    model="gemini-2.5-flash",
    name="support_agent",
    instruction="You are a helpful customer support assistant. Use the get_order_status tool when users ask about their orders.",
    tools=[get_order_status],  # ADK automatically wraps functions as FunctionTool
)

