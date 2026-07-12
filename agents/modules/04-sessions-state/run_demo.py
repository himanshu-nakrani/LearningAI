"""Optional programmatic runner for Module 04.

Usage (from course root, with GOOGLE_API_KEY set):

  python -m modules.04-sessions-state.run_demo

Note: folder name starts with digits; run via path instead if imports fail:

  python modules/04-sessions-state/run_demo.py
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

# Allow importing preference_agent as a sibling package when run as a script.
THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(THIS_DIR))

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from preference_agent.agent import root_agent

APP_NAME = "preference_demo"
USER_ID = "demo_user"
SESSION_ID = "demo_session"


async def main() -> None:
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state={},
    )
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    turns = [
        "My name is Alex and I prefer dark theme.",
        "Add milk and eggs to my shopping list.",
        "What do you know about me and my list?",
    ]

    for text in turns:
        print(f"\nUSER: {text}")
        content = types.Content(role="user", parts=[types.Part(text=text)])
        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=content,
        ):
            if event.is_final_response() and event.content and event.content.parts:
                print(f"AGENT: {event.content.parts[0].text}")


if __name__ == "__main__":
    asyncio.run(main())
