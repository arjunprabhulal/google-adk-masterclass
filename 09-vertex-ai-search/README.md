# 09. Vertex AI Search

Enterprise-grade search integration with ADK - Build agents that search across websites, documents, and structured data.

**Blog Post:** [https://arjunprabhulal.com/adk-builtin-tools-vertex-search/](https://arjunprabhulal.com/adk-builtin-tools-vertex-search/)

## Table of Contents

1. [What is Vertex AI Search?](#what-is-vertex-ai-search)
2. [RAG vs Search: When to Use Which](#rag-vs-search-when-to-use-which)
3. [Prerequisites](#prerequisites)
4. [Google Cloud Setup](#google-cloud-setup)
5. [Create a Data Store](#create-a-data-store)
6. [Setup Steps](#setup-steps)
7. [Running the Agent](#running-the-agent)
8. [Project Structure](#project-structure)
9. [Next Steps](#next-steps)

## What is Vertex AI Search?

Vertex AI Search (formerly Enterprise Search) provides Google-quality search for your data:

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA SOURCES                              │
│                                                              │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│   │ Websites │  │   PDFs   │  │ BigQuery │  │Cloud     │   │
│   │          │  │          │  │  Tables  │  │Storage   │   │
│   └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    VERTEX AI SEARCH                          │
│                                                              │
│   • Automatic indexing and ranking                           │
│   • Semantic understanding                                   │
│   • Multi-modal search (text, images)                        │
│   • Extractive answers with citations                        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    ADK AGENT                                 │
│                                                              │
│   Uses VertexAiSearchTool to query and synthesize results    │
└─────────────────────────────────────────────────────────────┘
```

## RAG vs Search: When to Use Which

| Feature | Vertex AI RAG | Vertex AI Search |
|---------|---------------|------------------|
| **Best For** | Q&A over documents | Enterprise search portals |
| **Data Size** | Smaller corpora | Large-scale data |
| **Updates** | Manual re-indexing | Automatic crawling |
| **Sources** | Uploaded files | Websites, GCS, BigQuery |
| **Output** | Generated answers | Search results + snippets |

**Use RAG when:** You need precise answers from a curated document set.

**Use Search when:** You need to search across websites, large document collections, or structured data.

## Prerequisites

- Python 3.10+
- Google Cloud Project with billing enabled
- `gcloud` CLI installed and authenticated
- Data to index (website URL, GCS bucket, or documents)

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

# Vertex AI User
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$USER_EMAIL" \
  --role="roles/aiplatform.user"

# Discovery Engine Viewer (or Editor to create data stores)
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$USER_EMAIL" \
  --role="roles/discoveryengine.viewer"
```

### 3. Authenticate

```bash
gcloud auth application-default login
```

## Create a Data Store

### Using Agent Builder Console

1. Go to [Agent Builder Console](https://console.cloud.google.com/gen-app-builder)
2. Click **Create App** → Select **Search**
3. Choose your data source type:
   - **Website**: Enter URLs to crawl
   - **Cloud Storage**: Select GCS bucket
   - **BigQuery**: Choose dataset
   - **Unstructured Documents**: Upload files
4. Configure indexing settings
5. Note the **Data Store ID** from the console

### Data Store ID Format

```
projects/PROJECT_ID/locations/global/collections/default_collection/dataStores/DATASTORE_ID
```

Example:
```
projects/my-project/locations/global/collections/default_collection/dataStores/my-docs-store_1234567890
```

## Setup Steps

1. Navigate to this module:

```bash
cd 09-vertex-ai-search
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

4. Configure environment variables in `vertex_search_agent/.env`:

```
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
DATA_STORE_ID=projects/your-project-id/locations/global/collections/default_collection/dataStores/your-datastore-id
```

Replace `your-project-id` and `your-datastore-id` with your actual values.

## Running the Agent

### Using ADK Web

```bash
adk web
```

Open http://127.0.0.1:8000 and select `vertex_search_agent`.

**Test Queries:**
- "Search for [topic in your data store]"
- "Find documents about [subject]"
- "What information do you have on [query]?"

### Using ADK CLI

```bash
adk run vertex_search_agent
```

## Project Structure

```
09-vertex-ai-search/
├── README.md
└── vertex_search_agent/
    ├── __init__.py
    ├── agent.py          # Search agent with VertexAiSearchTool
    └── .env              # Vertex AI configuration
```

## Key Features

| Feature | Description |
|---------|-------------|
| **Semantic Search** | Understands meaning, not just keywords |
| **Extractive Answers** | Highlights exact passages that answer queries |
| **Citations** | Links back to source documents |
| **Multi-turn** | Supports follow-up questions |
| **Filters** | Filter by metadata, date, etc. |

## Next Steps

Continue to [10. Custom Function Tools](../10-custom-function-tools/)
