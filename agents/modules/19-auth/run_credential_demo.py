#!/usr/bin/env python3
"""Demo: tool reads a credential-like secret from session state (auth pattern).

Full OAuth browser flows are environment-specific; this lab teaches the
Runner + credential/state wiring pattern used by ADK auth.
"""

from __future__ import annotations

import asyncio
import os

from google.adk.agents.llm_agent import Agent
from google.adk.auth.credential_service.in_memory_credential_service import (
    InMemoryCredentialService,
)
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import ToolContext
from google.genai.types import Content, Part

APP = "auth_demo"
USER = "u1"
SID = "s1"


def call_protected_api(resource: str, tool_context: ToolContext) -> dict:
    """Calls a mock protected API using a key from session state.

    Args:
        resource: Resource name to fetch (e.g. profile).
        tool_context: Injected ADK context.
    """
    # Pattern: tools should not hardcode secrets — read from state/credential service.
    api_key = tool_context.state.get("user:demo_api_key") or os.getenv(
        "DEMO_TOOL_API_KEY", ""
    )
    if not api_key:
        return {
            "status": "error",
            "error_message": (
                "Missing demo API key. Set state user:demo_api_key or DEMO_TOOL_API_KEY."
            ),
        }
    # Never return the raw key to the model in production logs.
    return {
        "status": "success",
        "resource": resource,
        "payload": f"mock-data-for-{resource}",
        "auth_present": True,
        "key_fingerprint": api_key[:4] + "…" if len(api_key) >= 4 else "set",
    }


def save_demo_key(api_key: str, tool_context: ToolContext) -> dict:
    """Stores a demo API key in user-scoped session state."""
    tool_context.state["user:demo_api_key"] = api_key.strip()
    return {"status": "success", "saved": True}


root_agent = Agent(
    model="gemini-flash-latest",
    name="credential_demo_agent",
    instruction="""
You help users call a protected demo API.
1. If they provide an API key, call save_demo_key.
2. To fetch data, call call_protected_api with the resource name.
Never print the full API key back to the user — only confirm success.
""".strip(),
    tools=[save_demo_key, call_protected_api],
)


async def main() -> None:
    sessions = InMemorySessionService()
    creds = InMemoryCredentialService()
    await sessions.create_session(app_name=APP, user_id=USER, session_id=SID, state={})
    runner = Runner(
        agent=root_agent,
        app_name=APP,
        session_service=sessions,
        credential_service=creds,
    )

    if not os.getenv("GOOGLE_API_KEY") and not os.getenv("GOOGLE_GENAI_USE_VERTEXAI"):
        # Offline path: exercise tools directly via state.
        print("No model key — running tool-only offline demo")
        from google.adk.tools.tool_context import ToolContext as TC

        # Minimal offline simulation without full ToolContext factory:
        class Fake:
            state = {}

        fake = Fake()
        print(save_demo_key("sk-demo-123456", fake))  # type: ignore[arg-type]
        print(call_protected_api("profile", fake))  # type: ignore[arg-type]
        return

    for text in (
        "Save API key sk-demo-abcdef",
        "Fetch the profile resource from the protected API",
    ):
        print(f"\nUSER: {text}")
        msg = Content(role="user", parts=[Part(text=text)])
        async for event in runner.run_async(
            user_id=USER, session_id=SID, new_message=msg
        ):
            if event.is_final_response() and event.content and event.content.parts:
                print("AGENT:", event.content.parts[0].text)


if __name__ == "__main__":
    asyncio.run(main())
