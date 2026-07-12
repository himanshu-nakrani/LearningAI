#!/usr/bin/env python3
"""CI-friendly import smoke for A2A demo (no server, no API key)."""

from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
os.environ.setdefault("ADK_SUPPRESS_A2A_EXPERIMENTAL_FEATURE_WARNINGS", "1")


def main() -> int:
    from math_specialist.agent import root_agent as specialist

    print("specialist:", specialist.name, "tools:", len(specialist.tools))

    from google.adk.a2a.utils.agent_to_a2a import to_a2a

    app = to_a2a(specialist, host="127.0.0.1", port=9001)
    print("to_a2a app:", type(app).__name__)

    from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

    remote = RemoteA2aAgent(
        name="remote_math_specialist",
        agent_card="http://127.0.0.1:9001/.well-known/agent.json",
    )
    print("RemoteA2aAgent:", remote.name)
    print("OK — A2A imports and app construction work")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
