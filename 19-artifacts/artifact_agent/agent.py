"""
18. Artifacts - Storing Files and Binary Data

Artifacts let agents save and retrieve files like reports, images,
and other binary data. Think of them as a file system for your agent.

Key concepts:
- Artifacts are stored as types.Part objects
- Each save creates a new version
- Use "user:" prefix for cross-session persistence

Blog: https://arjunprabhulal.com/adk-artifacts/

How Artifacts Work:
┌─────────────────────────────────────────────────────────────┐
│                      AGENT TOOL                              │
│                  (e.g., save_report)                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    ARTIFACT CREATION                         │
│                                                              │
│   data (bytes) ──► types.Part.from_bytes() ──► artifact     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   ARTIFACT SERVICE                           │
│                                                              │
│  ┌─────────────────────┐    ┌─────────────────────────┐     │
│  │ InMemoryArtifact    │    │  GcsArtifactService     │     │
│  │ Service (Dev)       │    │  (Production)           │     │
│  │                     │    │                         │     │
│  │ - Fast, local       │    │  - Persistent           │     │
│  │ - Lost on restart   │    │  - Scalable             │     │
│  └─────────────────────┘    └─────────────────────────┘     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      STORAGE                                 │
│                                                              │
│   Filename: "report.json"                                    │
│   Version:  1, 2, 3... (auto-incremented)                    │
│   Scope:    Session (default) or User ("user:filename")      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
"""

import asyncio
import json
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts import InMemoryArtifactService, GcsArtifactService
from google.adk.tools import ToolContext
from google.genai import types


# ============================================================
# ARTIFACT TOOLS
# ============================================================

async def save_report(title: str, content: str, tool_context: ToolContext) -> dict:
    """
    Save a report as a JSON artifact.
    
    Args:
        title: Report title
        content: Report content
        tool_context: Provides artifact storage access
    
    Returns:
        Confirmation with filename and version
    """
    report = {"title": title, "content": content}
    report_bytes = json.dumps(report, indent=2).encode('utf-8')
    
    # Wrap in types.Part
    artifact = types.Part.from_bytes(
        data=report_bytes,
        mime_type="application/json"
    )
    
    # Save and get version number (async)
    version = await tool_context.save_artifact(
        filename="report.json",
        artifact=artifact
    )
    
    return {
        "status": "saved",
        "filename": "report.json",
        "version": version
    }


async def get_report(filename: str, tool_context: ToolContext) -> dict:
    """
    Load a previously saved report.
    
    Args:
        filename: Name of the artifact to load
        tool_context: Provides artifact storage access
    
    Returns:
        Report content or error message
    """
    try:
        artifact = await tool_context.load_artifact(filename)
        
        if artifact is None:
            return {"error": f"'{filename}' not found"}
        
        # Extract the data with error handling
        if not hasattr(artifact, 'inline_data') or artifact.inline_data is None:
            return {"error": f"'{filename}' has no inline data"}
        
        data = artifact.inline_data.data
        if data is None:
            return {"error": f"'{filename}' data is empty"}
        
        # Try to decode as JSON, fall back to plain text
        try:
            content = json.loads(data.decode('utf-8'))
        except json.JSONDecodeError:
            content = data.decode('utf-8')
        
        return {"found": True, "content": content}
    except Exception as e:
        return {"error": f"Failed to load '{filename}': {str(e)}"}


async def list_saved_files(tool_context: ToolContext) -> dict:
    """
    List all saved artifacts.
    
    Args:
        tool_context: Provides artifact storage access
    
    Returns:
        List of artifact filenames
    """
    filenames = await tool_context.list_artifacts()
    
    return {
        "count": len(filenames),
        "files": filenames
    }


# ============================================================
# AGENT DEFINITION
# ============================================================

root_agent = Agent(
    model="gemini-2.5-flash",
    name="artifact_agent",
    instruction="""You help users save and retrieve reports.

Available tools:
- save_report: Save a new report with title and content
- get_report: Retrieve a saved report by filename
- list_saved_files: See all saved artifacts

When saving, confirm the filename so users can retrieve it later.""",
    tools=[save_report, get_report, list_saved_files],
)


# ============================================================
# DEMO
# ============================================================

async def chat(runner: Runner, user_id: str, session_id: str, message: str) -> str:
    """Send a message and get a response."""
    content = types.Content(role="user", parts=[types.Part(text=message)])
    
    response_text = ""
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    ):
        if hasattr(event, 'content') and event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, 'text') and part.text:
                    response_text += part.text
    
    return response_text


async def main():
    """
    Demonstrates Artifact operations:
    1. SAVE - Store a report as an artifact
    2. LIST - Show all saved artifacts
    3. LOAD - Retrieve the saved report
    """
    
    # Initialize services
    session_service = InMemorySessionService()
    artifact_service = InMemoryArtifactService()  # For production: GcsArtifactService
    
    runner = Runner(
        agent=root_agent,
        app_name="artifact_app",
        session_service=session_service,
        artifact_service=artifact_service,  # Enable artifact storage
    )
    
    print("=" * 60)
    print("ARTIFACTS DEMO")
    print("=" * 60)
    
    user_id = "user_demo"
    session = await session_service.create_session(
        app_name="artifact_app",
        user_id=user_id,
    )
    
    print(f"\nUser ID: {user_id}")
    print(f"Session ID: {session.id[:8]}...")
    print("-" * 40)
    
    # --- DEMO 1: SAVE ---
    print("\n" + "=" * 60)
    print("STEP 1: SAVE A REPORT")
    print("=" * 60)
    
    msg1 = "Save a report titled 'Q4 Summary' with content: 'Revenue grew 15% this quarter. Key wins include new enterprise clients.'"
    print(f"\nUser: {msg1}")
    response1 = await chat(runner, user_id, session.id, msg1)
    print(f"Agent: {response1}")
    
    # --- DEMO 2: LIST ---
    print("\n" + "=" * 60)
    print("STEP 2: LIST ALL ARTIFACTS")
    print("=" * 60)
    
    msg2 = "What files have I saved?"
    print(f"\nUser: {msg2}")
    response2 = await chat(runner, user_id, session.id, msg2)
    print(f"Agent: {response2}")
    
    # --- DEMO 3: LOAD ---
    print("\n" + "=" * 60)
    print("STEP 3: LOAD THE REPORT")
    print("=" * 60)
    
    msg3 = "Get the report from report.json"
    print(f"\nUser: {msg3}")
    response3 = await chat(runner, user_id, session.id, msg3)
    print(f"Agent: {response3}")
    
    # --- DEMO 4: SAVE ANOTHER (shows versioning) ---
    print("\n" + "=" * 60)
    print("STEP 4: SAVE UPDATED REPORT (Versioning)")
    print("=" * 60)
    
    msg4 = "Save a report titled 'Q4 Summary Updated' with content: 'Revenue grew 15%. Added: Customer retention at 95%.'"
    print(f"\nUser: {msg4}")
    response4 = await chat(runner, user_id, session.id, msg4)
    print(f"Agent: {response4}")
    print("\n(Notice: Same filename, new version!)")
    
    # Summary
    print("\n" + "=" * 60)
    print("ARTIFACT CONCEPTS")
    print("=" * 60)
    print("""
KEY OPERATIONS:
- save_artifact(filename, artifact) -> Returns version number
- load_artifact(filename) -> Returns types.Part or None
- list_artifacts() -> Returns list of filenames

VERSIONING:
- Each save to same filename creates new version (1, 2, 3...)
- load_artifact() gets the latest version by default

SCOPING:
- Default: Artifacts are session-scoped (temporary)
- Use "user:filename.json" for cross-session persistence

STORAGE BACKENDS:
- InMemoryArtifactService: Development (lost on restart)
- GcsArtifactService: Production (Google Cloud Storage)
    """)


async def demo_gcs():
    """
    Demonstrates GcsArtifactService for production use.
    
    Prerequisites:
    - Google Cloud project with Storage API enabled
    - GCS bucket created
    - Application Default Credentials configured
      (run: gcloud auth application-default login)
    """
    import os
    
    # Get bucket name from environment
    bucket_name = os.getenv("GCS_ARTIFACT_BUCKET")
    
    if not bucket_name:
        print("=" * 60)
        print("GCS ARTIFACT SERVICE DEMO")
        print("=" * 60)
        print("""
To run this demo, set the GCS_ARTIFACT_BUCKET environment variable:

    export GCS_ARTIFACT_BUCKET="your-bucket-name"
    python agent.py --gcs

Prerequisites:
1. Create a GCS bucket in your Google Cloud project
2. Enable the Cloud Storage API
3. Configure Application Default Credentials:
   gcloud auth application-default login

Example setup:
    # Create bucket
    gsutil mb gs://my-adk-artifacts-bucket
    
    # Run demo
    export GCS_ARTIFACT_BUCKET="my-adk-artifacts-bucket"
    python agent.py --gcs
        """)
        return
    
    print("=" * 60)
    print("GCS ARTIFACT SERVICE DEMO")
    print("=" * 60)
    print(f"\nBucket: {bucket_name}")
    
    # Initialize GCS artifact service
    session_service = InMemorySessionService()
    
    try:
        artifact_service = GcsArtifactService(bucket_name=bucket_name)
        print("GcsArtifactService initialized successfully!")
    except Exception as e:
        print(f"Error initializing GcsArtifactService: {e}")
        print("\nMake sure you have:")
        print("1. Created the GCS bucket")
        print("2. Configured Application Default Credentials")
        return
    
    runner = Runner(
        agent=root_agent,
        app_name="artifact_gcs_app",
        session_service=session_service,
        artifact_service=artifact_service,
    )
    
    user_id = "user_gcs_demo"
    session = await session_service.create_session(
        app_name="artifact_gcs_app",
        user_id=user_id,
    )
    
    print(f"User ID: {user_id}")
    print(f"Session ID: {session.id[:8]}...")
    print("-" * 40)
    
    # Save to GCS
    print("\n[SAVE TO GCS]")
    msg = "Save a report titled 'Cloud Report' with content: 'This report is stored in Google Cloud Storage!'"
    print(f"User: {msg}")
    response = await chat(runner, user_id, session.id, msg)
    print(f"Agent: {response}")
    
    # List from GCS
    print("\n[LIST FROM GCS]")
    msg2 = "What files are saved?"
    print(f"User: {msg2}")
    response2 = await chat(runner, user_id, session.id, msg2)
    print(f"Agent: {response2}")
    
    # Load from GCS
    print("\n[LOAD FROM GCS]")
    msg3 = "Get the report from report.json"
    print(f"User: {msg3}")
    response3 = await chat(runner, user_id, session.id, msg3)
    print(f"Agent: {response3}")
    
    print("\n" + "=" * 60)
    print("GCS BENEFITS")
    print("=" * 60)
    print("""
- Persistent: Data survives app restarts
- Scalable: Handles large files and high traffic
- Secure: IAM-based access control
- Versioned: Each save creates a new GCS object
- Shareable: Multiple app instances can access same bucket
    """)


if __name__ == "__main__":
    import sys
    
    if "--gcs" in sys.argv:
        asyncio.run(demo_gcs())
    else:
        asyncio.run(main())
