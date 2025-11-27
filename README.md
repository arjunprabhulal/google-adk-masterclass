# Google ADK Masterclass

<p align="center">
  <a href="https://arjunprabhulal.com/courses/adk-masterclass-hands-on-series/">
    <img src="https://arjunprabhulal.com/assets/images/blog/adk-masterclass-hands-on-series.png" alt="ADK Masterclass" width="400">
  </a>
</p>

<p align="center">
  <strong><a href="https://arjunprabhulal.com/courses/adk-masterclass-hands-on-series/">View Full Course</a></strong>
</p>

A free, hands-on masterclass for building AI agents with Google's Agent Development Kit (ADK).

[![Course](https://img.shields.io/badge/Course-ADK%20Masterclass-blue)](https://arjunprabhulal.com/courses/adk-masterclass-hands-on-series/)
[![ADK Docs](https://img.shields.io/badge/Docs-ADK-green)](https://google.github.io/adk-docs/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Table of Contents

### Module 1: Foundations
| # | Module | Description | Blog |
|---|--------|-------------|------|
| 01 | [Getting Started](./01-getting-started/) | Introduction to ADK, environment setup, first agent | [Read](https://arjunprabhulal.com/adk-getting-started/) |
| 02 | [Setting Up Agents](./02-setting-up-agent/) | CLI, Web, and Programmatic setup methods | [Read](https://arjunprabhulal.com/adk-setting-up-agent/) |
| 03 | [Visual Builder](./03-visual-builder/) | No-code agent building with Visual Builder | [Read](https://arjunprabhulal.com/google-adk-visual-agent-builder/) |

### Module 2: Agent Types
| # | Module | Description | Blog |
|---|--------|-------------|------|
| 04 | [LLM Agents](./04-llm-agents/) | Building intelligent LLM-powered agents | [Read](https://arjunprabhulal.com/adk-llm-agents/) |
| 05 | [Workflow Agents](./05-workflow-agents/) | Sequential, Parallel, and Loop patterns | [Read](https://arjunprabhulal.com/adk-workflow-sequential-loop-parallel/) |
| 06 | [Multi-Agent Systems](./06-multi-agent-systems/) | Agent orchestration and collaboration | [Read](https://arjunprabhulal.com/adk-multi-agent-systems/) |

### Module 3: Tools & Integrations
| # | Module | Description | Blog |
|---|--------|-------------|------|
| 07 | [Built-in Tools](./07-built-in-tools/) | Google Search, Code Executor | [Read](https://arjunprabhulal.com/adk-built-in-tools/) |
| 08 | [Vertex AI RAG](./08-vertex-ai-rag/) | RAG Engine integration | [Read](https://arjunprabhulal.com/adk-builtin-tools-rag/) |
| 09 | [Vertex AI Search](./09-vertex-ai-search/) | Enterprise search integration | [Read](https://arjunprabhulal.com/adk-builtin-tools-vertex-search/) |
| 10 | [Custom Function Tools](./10-custom-function-tools/) | Building custom Python tools | [Read](https://arjunprabhulal.com/adk-custom-tools-function/) |
| 11 | [OpenAPI Tools](./11-openapi-tools/) | REST API integration | [Read](https://arjunprabhulal.com/adk-custom-tools-openapi/) |
| 12 | [Multi-Tool Agent](./12-multi-tool-agent/) | Combining multiple tools | [Read](https://arjunprabhulal.com/adk-multi-tool-agent/) |
| 13 | [Third-Party MCP Tools](./13-third-party-mcp-tools/) | GitHub, Firecrawl integration | [Read](https://arjunprabhulal.com/adk-third-party-tools-github/) |

### Module 4: Protocols
| # | Module | Description | Blog |
|---|--------|-------------|------|
| 14 | [Model Context Protocol](./14-mcp-deep-dive/) | MCP architecture and patterns | [Read](https://arjunprabhulal.com/adk-mcp-deep-dive/) |

### Module 5: Core Components
| # | Module | Description | Blog |
|---|--------|-------------|------|
| 15 | [Session, State & Memory](./15-sessions-state-memory/) | Conversation history and state management | [Read](https://arjunprabhulal.com/adk-sessions-state/) |
| 16 | [Context Management](./16-context-management/) | Caching and compaction | [Read](https://arjunprabhulal.com/adk-context-management/) |
| 17 | [Callbacks](./17-callbacks/) | Intercepting agent behavior | [Read](https://arjunprabhulal.com/adk-callbacks/) |
| 18 | [Artifacts](./18-artifacts/) | File and data handling | [Read](https://arjunprabhulal.com/adk-artifacts/) |
| 19 | [Events](./19-events/) | Event streaming and debugging | [Read](https://arjunprabhulal.com/adk-events/) |

## Prerequisites

**For most modules:**
- Python 3.10+
- Gemini API key from [AI Studio](https://aistudio.google.com/apikey)

**For Vertex AI modules (08, 09, 18):**
- See [GCP Setup Guide](./docs/GCP_SETUP.md) for detailed instructions

## Quick Start

```bash
# Clone the repository
git clone https://github.com/arjunprabhulal/google-adk-masterclass.git
cd google-adk-masterclass

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
echo "GOOGLE_API_KEY=your-api-key-here" > .env

# Run your first agent
cd 01-getting-started
adk web
```

## Resources

- [ADK Documentation](https://google.github.io/adk-docs/)
- [ADK GitHub Repository](https://github.com/google/adk-python)
- [Course Homepage](https://arjunprabhulal.com/courses/adk-masterclass-hands-on-series/)
- [Author's Blog](https://arjunprabhulal.com/)

## Author

**Arjun Prabhulal**
- Website: [arjunprabhulal.com](https://arjunprabhulal.com)
- GitHub: [@arjunprabhulal](https://github.com/arjunprabhulal)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
