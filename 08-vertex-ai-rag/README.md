# 08. Vertex AI RAG Engine

Retrieval-Augmented Generation (RAG) with Vertex AI - Build agents that answer questions using your own documents.

**Blog Post:** [https://arjunprabhulal.com/adk-builtin-tools-rag/](https://arjunprabhulal.com/adk-builtin-tools-rag/)

## Table of Contents

1. [What is RAG?](#what-is-rag)
2. [Prerequisites](#prerequisites)
3. [Google Cloud Setup](#google-cloud-setup)
4. [Create a RAG Corpus](#create-a-rag-corpus)
5. [Setup Steps](#setup-steps)
6. [Running the Agent](#running-the-agent)
7. [Project Structure](#project-structure)
8. [Next Steps](#next-steps)

## What is RAG?

RAG (Retrieval-Augmented Generation) enhances LLM responses by:

1. **Retrieving** relevant documents from your knowledge base
2. **Augmenting** the prompt with retrieved context
3. **Generating** accurate answers grounded in your data

```
┌─────────────────────────────────────────────────────────────┐
│                      USER QUERY                              │
│              "What is our refund policy?"                    │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   RAG RETRIEVAL                              │
│                                                              │
│   Query → Vector Search → Top-K Documents                    │
│                                                              │
│   Retrieved: "policy.pdf", "faq.md", "terms.txt"            │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   LLM GENERATION                             │
│                                                              │
│   Context: [Retrieved documents]                             │
│   Query: "What is our refund policy?"                        │
│                                                              │
│   Response: "Based on our policy documents, refunds are..."  │
└─────────────────────────────────────────────────────────────┘
```

## Prerequisites

- Python 3.10+
- Google Cloud Project with billing enabled
- `gcloud` CLI installed and authenticated
- Documents to upload (PDF, TXT, HTML, etc.)

## Google Cloud Setup

### 1. Enable Required APIs

```bash
gcloud services enable aiplatform.googleapis.com
gcloud services enable discoveryengine.googleapis.com
```

### 2. Grant IAM Roles

```bash
# Replace with your project ID and email
PROJECT_ID="your-project-id"
USER_EMAIL="your-email@example.com"

# Vertex AI User - for using AI Platform
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$USER_EMAIL" \
  --role="roles/aiplatform.user"

# Discovery Engine Editor - for RAG operations
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$USER_EMAIL" \
  --role="roles/discoveryengine.editor"
```

### 3. Authenticate

```bash
gcloud auth application-default login
```

## Create a RAG Corpus

### Option A: Using Google Cloud Console

1. Go to [Vertex AI Console](https://console.cloud.google.com/vertex-ai)
2. Navigate to **RAG Engine** → **Corpora**
3. Click **Create Corpus**
4. Upload your documents
5. Copy the corpus resource name

### Option B: Using Python SDK

```python
from vertexai.preview import rag

# Create corpus
corpus = rag.create_corpus(display_name="my-knowledge-base")

# Upload documents
rag.upload_file(
    corpus_name=corpus.name,
    path="path/to/document.pdf",
    display_name="document.pdf"
)

print(f"Corpus: {corpus.name}")
```

## Setup Steps

1. Navigate to this module:

```bash
cd 08-vertex-ai-rag
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r ../requirements.txt
```

4. Configure environment variables in `rag_agent/.env`:

```
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
RAG_CORPUS=projects/your-project-id/locations/us-central1/ragCorpora/your-corpus-id
```

Replace `your-project-id` and `your-corpus-id` with your actual values.

## Running the Agent

### Using ADK Web

```bash
adk web
```

Open http://127.0.0.1:8000 and select `rag_agent`.

**Test Queries:**
- "What documents do you have access to?"
- "Summarize the main topics in my knowledge base"
- "Find information about [your document topic]"

### Using ADK CLI

```bash
adk run rag_agent
```

## Project Structure

```
08-vertex-ai-rag/
├── README.md
└── rag_agent/
    ├── __init__.py
    ├── agent.py          # RAG agent with VertexAiRagRetrieval tool
    └── .env              # Vertex AI configuration
```

## Key Configuration Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `similarity_top_k` | Number of documents to retrieve | 10 |
| `vector_distance_threshold` | Similarity threshold (0-1) | 0.6 |
| `rag_resources` | List of corpus resources | Required |

## Next Steps

Continue to [09. Vertex AI Search](../09-vertex-ai-search/)
