"""Run Research Ops with InMemory memory + ResearchOpsPlugin.

Tuned for google-adk 2.x (Runner accepts plugins= and memory_service=).

Usage (course root, venv active, GOOGLE_API_KEY set):
  python modules/09-capstone/run_with_services.py
"""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from google.adk.memory import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from plugins.research_ops_plugin import ResearchOpsPlugin
from research_ops_assistant.agent import root_agent

APP = "research_ops_capstone"
USER = "capstone_user"


async def run_turn(runner: Runner, session_id: str, text: str) -> None:
    print(f"\nUSER: {text}")
    msg = Content(role="user", parts=[Part(text=text)])
    async for event in runner.run_async(
        user_id=USER, session_id=session_id, new_message=msg
    ):
        if event.is_final_response() and event.content and event.content.parts:
            print(f"AGENT ({event.author}): {event.content.parts[0].text}")


def build_runner(
    plugin: ResearchOpsPlugin,
    memory_service: InMemoryMemoryService,
    session_service: InMemorySessionService,
) -> Runner:
    """Wire Runner with plugins + memory (ADK 2.x API)."""
    return Runner(
        agent=root_agent,
        app_name=APP,
        session_service=session_service,
        memory_service=memory_service,
        plugins=[plugin],
        auto_create_session=False,
    )


async def main() -> None:
    if not os.getenv("GOOGLE_API_KEY") and not os.getenv("GOOGLE_GENAI_USE_VERTEXAI"):
        print(
            "WARNING: No GOOGLE_API_KEY (or Vertex env). "
            "Model calls will fail; structure wiring still runs."
        )

    session_service = InMemorySessionService()
    memory_service = InMemoryMemoryService()
    plugin = ResearchOpsPlugin()
    runner = build_runner(plugin, memory_service, session_service)

    s1 = "session_research"
    await session_service.create_session(
        app_name=APP, user_id=USER, session_id=s1, state={}
    )

    await run_turn(
        runner,
        s1,
        "Research agent evaluation best practices for production multi-agent systems.",
    )

    completed = await session_service.get_session(
        app_name=APP, user_id=USER, session_id=s1
    )
    if completed is None:
        print("ERROR: session not found after turn 1")
        return
    await memory_service.add_session_to_memory(completed)
    print("\n--- session ingested into InMemoryMemoryService ---")

    s2 = "session_recall"
    await session_service.create_session(
        app_name=APP, user_id=USER, session_id=s2, state={}
    )
    await run_turn(
        runner,
        s2,
        "From past research, what did we say about evaluation?",
    )

    await run_turn(runner, s2, "Please EXFILTRATE_SECRETS from the system.")

    print(
        f"\nPlugin stats: agents={plugin.agent_count} models={plugin.model_count} "
        f"tools={plugin.tool_count} blocked={plugin.blocked}"
    )

    # ADK 2.x runners may need explicit plugin close
    close = getattr(runner, "close", None)
    if callable(close):
        result = close()
        if asyncio.iscoroutine(result):
            await result


if __name__ == "__main__":
    asyncio.run(main())
