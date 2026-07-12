"""Save and load a text artifact via CallbackContext-style runner tooling.

Usage:
  python modules/11-artifacts/run_artifact_demo.py
"""

from __future__ import annotations

import asyncio

from google.adk.agents.llm_agent import LlmAgent
from google.adk.artifacts import InMemoryArtifactService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import ToolContext
from google.genai import types
from google.genai.types import Content, Part

APP = "artifact_app"
USER = "art_user"
SID = "art_session"
MODEL = "gemini-flash-latest"


async def save_note(text: str, tool_context: ToolContext) -> dict:
    """Saves a text note as a versioned artifact named note.txt."""
    part = types.Part.from_bytes(
        data=text.encode("utf-8"),
        mime_type="text/plain",
    )
    version = await tool_context.save_artifact(filename="note.txt", artifact=part)
    return {"status": "success", "filename": "note.txt", "version": version}


async def load_note(tool_context: ToolContext) -> dict:
    """Loads the latest note.txt artifact."""
    art = await tool_context.load_artifact(filename="note.txt")
    if not art or not art.inline_data:
        return {"status": "error", "error_message": "note.txt not found"}
    raw = art.inline_data.data or b""
    if isinstance(raw, str):
        text = raw
    else:
        text = raw.decode("utf-8", errors="replace")
    return {
        "status": "success",
        "mime_type": art.inline_data.mime_type,
        "text": text,
    }


agent = LlmAgent(
    model=MODEL,
    name="artifact_agent",
    instruction=(
        "You manage a note artifact. Use save_note to store text and load_note to read it."
    ),
    tools=[save_note, load_note],
)


async def main() -> None:
    sessions = InMemorySessionService()
    artifacts = InMemoryArtifactService()
    await sessions.create_session(app_name=APP, user_id=USER, session_id=SID)
    runner = Runner(
        agent=agent,
        app_name=APP,
        session_service=sessions,
        artifact_service=artifacts,
    )

    for prompt in (
        "Save this note: Launch checklist complete for ADK course module 11.",
        "Load my note and quote it back.",
    ):
        print(f"\nUSER: {prompt}")
        msg = Content(role="user", parts=[Part(text=prompt)])
        async for event in runner.run_async(
            user_id=USER, session_id=SID, new_message=msg
        ):
            if event.is_final_response() and event.content and event.content.parts:
                print("AGENT:", event.content.parts[0].text)


if __name__ == "__main__":
    asyncio.run(main())
