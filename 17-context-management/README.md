# 17. Context Management

Context caching and compression for better performance.

**Blog Post:** [https://arjunprabhulal.com/adk-context-management/](https://arjunprabhulal.com/adk-context-management/)

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Setup Steps](#setup-steps)
4. [Context Strategies](#context-strategies)
5. [Running the Demo](#running-the-demo)
6. [Next Steps](#next-steps)

## Overview

Context management optimizes how agents handle conversation history and system prompts:

- **Context Caching** - Reduce API calls by caching static content
- **Context Compression** - Summarize long conversations to stay within token limits

## Prerequisites

- Python 3.10+
- Gemini API key from [AI Studio](https://aistudio.google.com/apikey)

## Setup Steps

1. Navigate to this module:

```bash
cd 17-context-management
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

4. Set up environment variables in `context_agent/.env`:

```
GOOGLE_API_KEY=your-api-key-here
```

## Context Strategies

### Context Caching

Cache frequently used context to reduce costs:

```python
from google.adk.agents.config import ContextCacheConfig

cache_config = ContextCacheConfig(
    max_entries=100,
    ttl_seconds=3600
)
```

### Context Compression

Summarize long conversations:

```python
from google.adk.agents.config import EventsCompactionConfig

compaction_config = EventsCompactionConfig(
    max_events=50,
    compaction_strategy="summarize"
)
```

## Running the Demo

```bash
cd context_agent
python agent.py
```

The demo shows:
- Caching configuration
- Compression strategies
- Performance optimization

## Next Steps

Continue to [18. Callbacks](../18-callbacks/)
