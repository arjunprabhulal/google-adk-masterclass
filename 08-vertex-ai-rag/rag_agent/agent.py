import os
from google.adk.agents import Agent
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag

# Configure RAG retrieval from environment variable
# Set RAG_CORPUS in .env or export it:
# RAG_CORPUS=projects/YOUR_PROJECT/locations/us-central1/ragCorpora/YOUR_CORPUS_ID
RAG_CORPUS = os.environ.get(
    "RAG_CORPUS",
    "projects/YOUR_PROJECT/locations/us-central1/ragCorpora/YOUR_CORPUS_ID"
)

# Validate configuration
if "YOUR_PROJECT" in RAG_CORPUS:
    print("WARNING: RAG_CORPUS not configured. Set it in .env or as environment variable.")
    print("Example: RAG_CORPUS=projects/my-project/locations/us-central1/ragCorpora/123456")

rag_tool = VertexAiRagRetrieval(
    name='retrieve_documents',
    description='Retrieve relevant documents from the knowledge base',
    rag_resources=[
        rag.RagResource(rag_corpus=RAG_CORPUS)
    ],
    similarity_top_k=10,
    vector_distance_threshold=0.6,
)

root_agent = Agent(
    model="gemini-2.5-flash",
    name="rag_agent",
    instruction="""You are a helpful assistant with access to company documents.
Use the retrieval tool to find relevant information before answering.
Always cite your sources.""",
    tools=[rag_tool],
)
