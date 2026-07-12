#!/usr/bin/env python3
"""One-shot client against remote A2A math specialist.

Prereq: python modules/28-a2a-demo/serve_math_specialist.py
        GOOGLE_API_KEY set
"""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from coordinator.agent import root_agent

APP, USER, SID = "a2a_coord", "u1", "s1"


async def main() -> None:
    if not os.getenv("GOOGLE_API_KEY") and not os.getenv("GOOGLE_GENAI_USE_VERTEXAI"):
        print("Set GOOGLE_API_KEY. Server can still be smoke-tested separately.")
        sys.exit(0)

    sessions = InMemorySessionService()
    await sessions.create_session(app_name=APP, user_id=USER, session_id=SID, state={})
    runner = Runner(agent=root_agent, app_name=APP, session_service=sessions)
    msg = Content(
        role="user",
        parts=[Part(text="What is 17 + 25? Use the remote math specialist.")],
    )
    print("USER:", msg.parts[0].text)
    try:
        async for event in runner.run_async(
            user_id=USER, session_id=SID, new_message=msg
        ):
            if event.is_final_response() and event.content and event.content.parts:
                print("AGENT:", event.content.parts[0].text)
    except Exception as exc:  # noqa: BLE001
        print(f"Client failed (is the specialist server up?): {type(exc).__name__}: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
