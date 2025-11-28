# 19. Artifacts

File and data handling in ADK agents.

**Blog Post:** [https://arjunprabhulal.com/adk-artifacts/](https://arjunprabhulal.com/adk-artifacts/)

## Table of Contents

1. [What are Artifacts?](#what-are-artifacts)
2. [Prerequisites](#prerequisites)
3. [Setup Steps](#setup-steps)
4. [Artifact Services](#artifact-services)
5. [Running the Demo](#running-the-demo)
6. [GCS Setup (Optional)](#gcs-setup-optional)
7. [Next Steps](#next-steps)

## What are Artifacts?

Artifacts are files or data that agents create or use during execution:

- Reports and documents
- Images and media
- Data exports
- Generated code

## Prerequisites

- Python 3.10+
- Gemini API key from [AI Studio](https://aistudio.google.com/apikey)

## Setup Steps

1. Navigate to this module:

```bash
cd 19-artifacts
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

4. Set up environment variables in `artifact_agent/.env`:

```
GOOGLE_API_KEY=your-api-key-here
```

## Artifact Services

| Service | Use Case | Persistence |
|---------|----------|-------------|
| `InMemoryArtifactService` | Development/testing | Memory only |
| `GcsArtifactService` | Production | Google Cloud Storage |

### Saving Artifacts

```python
artifact = types.Part.from_bytes(
    data=content.encode(),
    mime_type="text/plain"
)
await tool_context.save_artifact(filename="report.txt", artifact=artifact)
```

### Loading Artifacts

```python
artifact = await tool_context.load_artifact(filename="report.txt")
```

## Running the Demo

```bash
cd artifact_agent
python agent.py
```

The demo shows:
- Saving text artifacts
- Listing saved files
- Loading artifacts

## GCS Setup (Optional)

For production with Google Cloud Storage:

1. **Enable Cloud Storage API:**

```bash
gcloud services enable storage.googleapis.com
```

2. **Create a bucket:**

```bash
gsutil mb gs://your-bucket-name
```

3. **Required IAM Roles:**

- `roles/storage.objectAdmin` - Storage Object Admin

4. **Authenticate:**

```bash
gcloud auth application-default login
```

5. **Update `.env`:**

```
GCS_ARTIFACT_BUCKET=your-bucket-name
GOOGLE_CLOUD_PROJECT=your-project-id
```

6. **Run GCS demo:**

```bash
python agent.py --gcs
```

## Next Steps

Continue to [20. Events](../20-events/)
