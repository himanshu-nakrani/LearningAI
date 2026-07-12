#!/usr/bin/env python3
"""Text-driven live session using LiveRequestQueue + run_live.

Requires GOOGLE_API_KEY. Audio/mic not required for this text lab.
Live/BIDI support depends on model + backend; if unsupported, the script
prints the error and exits cleanly.
"""

from __future__ import annotations

import asyncio
import os
import sys

from google.adk.agents.live_request_queue import LiveRequestQueue
from google.adk.agents.llm_agent import Agent
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

APP, USER, SID = "live_demo", "u1", "s1"


async def main() -> None:
    if not os.getenv("GOOGLE_API_KEY") and not os.getenv("GOOGLE_GENAI_USE_VERTEXAI"):
        print("Set GOOGLE_API_KEY. Offline? use run_live_offline_queue.py")
        sys.exit(0)

    agent = Agent(
        model="gemini-flash-latest",
        name="live_text_agent",
        instruction="You are in a live session. Keep replies very short.",
    )
    sessions = InMemorySessionService()
    await sessions.create_session(app_name=APP, user_id=USER, session_id=SID, state={})
    runner = Runner(agent=agent, app_name=APP, session_service=sessions)

    queue = LiveRequestQueue()

    async def producer() -> None:
        await asyncio.sleep(0.2)
        queue.send_content(
            Content(role="user", parts=[Part(text="Say hi in five words.")])
        )
        await asyncio.sleep(8)
        queue.close()

    cfg = RunConfig(streaming_mode=StreamingMode.BIDI)
    prod = asyncio.create_task(producer())
    try:
        async for event in runner.run_live(
            user_id=USER,
            session_id=SID,
            live_request_queue=queue,
            run_config=cfg,
        ):
            if event.content and event.content.parts:
                texts = [p.text for p in event.content.parts if p.text]
                if texts:
                    print("EVENT:", " ".join(texts))
    except Exception as exc:  # noqa: BLE001
        print(f"Live session not available in this environment: {type(exc).__name__}: {exc}")
        print("SSE path still works via run_sse_stream.py")
    finally:
        await prod


if __name__ == "__main__":
    asyncio.run(main())
