#!/usr/bin/env python3
"""SSE streaming text responses via RunConfig.streaming_mode=SSE.

Requires GOOGLE_API_KEY (or Vertex env).
"""

from __future__ import annotations

import asyncio
import os
import sys

from google.adk.agents.llm_agent import Agent
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

APP, USER, SID = "sse_demo", "u1", "s1"


async def main() -> None:
    if not os.getenv("GOOGLE_API_KEY") and not os.getenv("GOOGLE_GENAI_USE_VERTEXAI"):
        print("Set GOOGLE_API_KEY (or Vertex env). Offline? use run_live_offline_queue.py")
        sys.exit(0)

    agent = Agent(
        model="gemini-flash-latest",
        name="sse_agent",
        instruction="Answer in 2-3 short sentences.",
    )
    sessions = InMemorySessionService()
    await sessions.create_session(app_name=APP, user_id=USER, session_id=SID, state={})
    runner = Runner(agent=agent, app_name=APP, session_service=sessions)

    msg = Content(role="user", parts=[Part(text="Explain SSE streaming in one analogy.")])
    cfg = RunConfig(streaming_mode=StreamingMode.SSE)
    print("Streaming (partials may appear):\n")
    async for event in runner.run_async(
        user_id=USER, session_id=SID, new_message=msg, run_config=cfg
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    partial = getattr(event, "partial", None)
                    tag = "partial" if partial else "chunk"
                    print(f"[{tag}] {part.text}")


if __name__ == "__main__":
    asyncio.run(main())
