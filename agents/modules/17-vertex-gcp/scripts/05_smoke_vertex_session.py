#!/usr/bin/env python3
"""Smoke-test VertexAiSessionService connectivity.

Requires:
  GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION
  ADC: gcloud auth application-default login
  Optional: REASONING_ENGINE_APP_NAME / AGENT_ENGINE resource name

Usage:
  python modules/17-vertex-gcp/scripts/05_smoke_vertex_session.py
"""

from __future__ import annotations

import asyncio
import os
import sys


async def main() -> int:
    project = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    app_name = os.environ.get(
        "REASONING_ENGINE_APP_NAME",
        os.environ.get("AGENT_ENGINE_ID", "smoke-test-app"),
    )

    if not project:
        print("SKIP: GOOGLE_CLOUD_PROJECT not set")
        return 0

    try:
        from google.adk.sessions import VertexAiSessionService
    except ImportError as exc:
        print(f"SKIP: Vertex session import failed: {exc}")
        print("Install: pip install 'google-adk[vertexai]'")
        return 0

    print(f"Creating VertexAiSessionService project={project} location={location}")
    service = VertexAiSessionService(project=project, location=location)

    try:
        session = await service.create_session(
            app_name=app_name,
            user_id="course_smoke_user",
            state={"smoke": True},
        )
        print("OK: session created:", getattr(session, "id", session))
        return 0
    except Exception as exc:  # noqa: BLE001 — smoke test surfaces any config error
        print("FAIL: could not create session.")
        print("  This usually means Agent Runtime/resource setup is incomplete.")
        print(f"  Error: {type(exc).__name__}: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
