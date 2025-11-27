# Google Cloud Platform Setup Guide

This guide covers the GCP setup required for Vertex AI modules (08, 09, 18).

## Prerequisites

- Google Cloud account with billing enabled
- `gcloud` CLI installed ([Install Guide](https://cloud.google.com/sdk/docs/install))

## Quick Setup

```bash
# Set your project
export PROJECT_ID="your-project-id"
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable aiplatform.googleapis.com
gcloud services enable discoveryengine.googleapis.com
gcloud services enable storage.googleapis.com

# Authenticate
gcloud auth application-default login
```

## Required IAM Roles

### For Vertex AI RAG (Module 08)

```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:YOUR_EMAIL" \
  --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:YOUR_EMAIL" \
  --role="roles/discoveryengine.editor"
```

### For Vertex AI Search (Module 09)

```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:YOUR_EMAIL" \
  --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:YOUR_EMAIL" \
  --role="roles/discoveryengine.viewer"
```

### For GCS Artifacts (Module 18)

```bash
# Create a bucket
gsutil mb -l us-central1 gs://$PROJECT_ID-artifacts

# Grant access
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:YOUR_EMAIL" \
  --role="roles/storage.objectAdmin"
```

## Environment Variables

After setup, configure your `.env` file:

```bash
# For Vertex AI modules
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1

# For RAG (Module 08)
RAG_CORPUS=projects/your-project-id/locations/us-central1/ragCorpora/your-corpus-id

# For Search (Module 09)
DATA_STORE_ID=projects/your-project-id/locations/global/collections/default_collection/dataStores/your-datastore-id
```

## Troubleshooting

### "Permission Denied" Errors

1. Verify you're authenticated:
   ```bash
   gcloud auth list
   ```

2. Check your IAM roles:
   ```bash
   gcloud projects get-iam-policy $PROJECT_ID --filter="bindings.members:YOUR_EMAIL"
   ```

### "API Not Enabled" Errors

```bash
# List enabled APIs
gcloud services list --enabled

# Enable missing API
gcloud services enable MISSING_API.googleapis.com
```

### "Quota Exceeded" Errors

Check quotas in the [Cloud Console](https://console.cloud.google.com/iam-admin/quotas).

## Resources

- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [Agent Builder Documentation](https://cloud.google.com/generative-ai-app-builder/docs)
- [IAM Roles Reference](https://cloud.google.com/iam/docs/understanding-roles)

