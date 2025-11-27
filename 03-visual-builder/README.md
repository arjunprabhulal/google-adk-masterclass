# 03. Build Agents with Visual Builder

Build and manage AI agents without coding using Google ADK Visual Agent Builder.

**Blog Post:** [https://arjunprabhulal.com/google-adk-visual-agent-builder/](https://arjunprabhulal.com/google-adk-visual-agent-builder/)

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Setup Steps](#setup-steps)
4. [Using the Visual Builder](#using-the-visual-builder)
5. [Next Steps](#next-steps)

## Overview

The Visual Agent Builder provides a no-code interface to create and manage AI agents using drag-and-drop components. Perfect for:

- Rapid prototyping
- Non-developers building agents
- Visual workflow design

## Prerequisites

- Python 3.10+
- ADK version 1.18.0 or higher
- Gemini API key from [AI Studio](https://aistudio.google.com/apikey)

## Setup Steps

1. Navigate to this module:

```bash
cd 03-visual-builder
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

4. Start the ADK web interface:

```bash
adk web
```

## Using the Visual Builder

1. Open http://127.0.0.1:8000 in your browser
2. Click the **edit icon** next to the agent dropdown
3. Use the visual interface to:
   - Configure agent properties (name, model, instruction)
   - Add tools and sub-agents
   - Set up workflow patterns
4. Test your agent in the chat interface
5. Export the generated code

## Next Steps

Continue to [04. LLM Agents](../04-llm-agents/)
