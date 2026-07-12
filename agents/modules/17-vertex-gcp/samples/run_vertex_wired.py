"""Demonstrate wiring Vertex session + optional Memory Bank services.

Gracefully no-ops if GCP is not configured.
"""

from __future__ import annotations

import asyncio
import os


async def main() -> None:
    project = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    engine = os.getenv("AGENT_ENGINE_ID")

    print("=== Vertex wiring demo ===")
    print(f"project={project!r} location={location!r} engine={engine!r}")

    if not project:
        print("No GOOGLE_CLOUD_PROJECT — showing intended wiring only.\n")
        print(
            """
from google.adk.sessions import VertexAiSessionService
from google.adk.memory import VertexAiMemoryBankService
from google.adk.runners import Runner

session_service = VertexAiSessionService(project=PROJECT, location=LOCATION)
memory_service = VertexAiMemoryBankService(
    project=PROJECT, location=LOCATION, agent_engine_id=ENGINE_ID
)
runner = Runner(
    agent=root_agent,
    app_name=ENGINE_RESOURCE_OR_APP,
    session_service=session_service,
    memory_service=memory_service,
)
"""
        )
        return

    from google.adk.agents.llm_agent import Agent
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.genai.types import Content, Part

    agent = Agent(
        model="gemini-flash-latest",
        name="vertex_wired",
        instruction="Say hello in one short sentence.",
    )

    # Prefer Vertex session when available; fall back to in-memory for demo.
    session_service = InMemorySessionService()
    memory_service = None
    try:
        from google.adk.sessions import VertexAiSessionService

        session_service = VertexAiSessionService(project=project, location=location)
        print("Using VertexAiSessionService")
    except Exception as exc:  # noqa: BLE001
        print(f"Vertex sessions unavailable ({exc}); using InMemorySessionService")

    if engine:
        try:
            from google.adk.memory import VertexAiMemoryBankService

            memory_service = VertexAiMemoryBankService(
                project=project,
                location=location,
                agent_engine_id=engine,
            )
            print("Using VertexAiMemoryBankService")
        except Exception as exc:  # noqa: BLE001
            print(f"Memory Bank unavailable: {exc}")

    app = engine or "vertex_wired_app"
    await session_service.create_session(
        app_name=app, user_id="u1", session_id="s1", state={}
    )
    runner = Runner(
        agent=agent,
        app_name=app,
        session_service=session_service,
        memory_service=memory_service,
    )
    msg = Content(role="user", parts=[Part(text="Health check")])
    async for event in runner.run_async(
        user_id="u1", session_id="s1", new_message=msg
    ):
        if event.is_final_response() and event.content and event.content.parts:
            print("AGENT:", event.content.parts[0].text)


if __name__ == "__main__":
    asyncio.run(main())
