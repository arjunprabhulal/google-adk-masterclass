import os
from google.adk.agents import LlmAgent
from google.adk.tools import VertexAiSearchTool

# Configure Data Store ID from environment variable
# Set DATA_STORE_ID in .env or export it:
# DATA_STORE_ID=projects/YOUR_PROJECT/locations/global/collections/default_collection/dataStores/YOUR_DATASTORE_ID
DATA_STORE_ID = os.environ.get(
    "DATA_STORE_ID",
    "projects/YOUR_PROJECT/locations/global/collections/default_collection/dataStores/YOUR_DATASTORE_ID"
)

# Validate configuration
if "YOUR_PROJECT" in DATA_STORE_ID:
    print("WARNING: DATA_STORE_ID not configured. Set it in .env or as environment variable.")
    print("Example: DATA_STORE_ID=projects/my-project/locations/global/collections/default_collection/dataStores/my-store_123")

search_tool = VertexAiSearchTool(data_store_id=DATA_STORE_ID)

root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="enterprise_search_agent",
    instruction="""You are a helpful assistant with access to company documents.
Use the search tool to find relevant information.
Provide accurate answers based on the search results.""",
    tools=[search_tool],
)
