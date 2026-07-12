"""Two-session memory demo (InMemoryMemoryService + load_memory).

Usage (from course root, GOOGLE_API_KEY set):
  python modules/10-memory/run_memory_scenario.py
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from google.adk.agents.llm_agent import LlmAgent
from google.adk.memory import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import load_memory
from google.genai.types import Content, Part

APP = "memory_course_app"
USER = "mem_user"
MODEL = "gemini-flash-latest"


async def main() -> None:
    session_service = InMemorySessionService()
    memory_service = InMemoryMemoryService()

    capture = LlmAgent(
        model=MODEL,
        name="InfoCaptureAgent",
        instruction="Acknowledge the user's statement in one short sentence.",
    )
    recall = LlmAgent(
        model=MODEL,
        name="MemoryRecallAgent",
        instruction=(
            "Answer the user. Use the load_memory tool if the answer might "
            "be in past conversations."
        ),
        tools=[load_memory],
    )

    # Turn 1 — capture
    print("--- Turn 1: capture ---")
    r1 = Runner(
        agent=capture,
        app_name=APP,
        session_service=session_service,
        memory_service=memory_service,
    )
    s1 = "session_info"
    await session_service.create_session(app_name=APP, user_id=USER, session_id=s1)
    msg1 = Content(role="user", parts=[Part(text="My favorite project is Project Alpha.")])
    async for event in r1.run_async(user_id=USER, session_id=s1, new_message=msg1):
        if event.is_final_response() and event.content and event.content.parts:
            print("Agent:", event.content.parts[0].text)

    completed = await session_service.get_session(
        app_name=APP, user_id=USER, session_id=s1
    )
    print("--- Ingest session into memory ---")
    await memory_service.add_session_to_memory(completed)

    # Turn 2 — recall in a new session
    print("--- Turn 2: recall ---")
    r2 = Runner(
        agent=recall,
        app_name=APP,
        session_service=session_service,
        memory_service=memory_service,
    )
    s2 = "session_recall"
    await session_service.create_session(app_name=APP, user_id=USER, session_id=s2)
    msg2 = Content(role="user", parts=[Part(text="What is my favorite project?")])
    async for event in r2.run_async(user_id=USER, session_id=s2, new_message=msg2):
        if event.is_final_response() and event.content and event.content.parts:
            print("Agent:", event.content.parts[0].text)


if __name__ == "__main__":
    asyncio.run(main())
