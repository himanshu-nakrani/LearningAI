#!/usr/bin/env python3
"""Serve math_specialist as an A2A HTTP app.

  python modules/28-a2a-demo/serve_math_specialist.py
  # http://127.0.0.1:9001
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Ensure package import
sys.path.insert(0, str(Path(__file__).resolve().parent))

import uvicorn
from google.adk.a2a.utils.agent_to_a2a import to_a2a

from math_specialist.agent import root_agent

HOST = os.getenv("A2A_HOST", "127.0.0.1")
PORT = int(os.getenv("A2A_PORT", "9001"))


def main() -> None:
    # Suppress is noisy but intentional for learners
    os.environ.setdefault("ADK_SUPPRESS_A2A_EXPERIMENTAL_FEATURE_WARNINGS", "1")
    app = to_a2a(root_agent, host=HOST, port=PORT, protocol="http")
    print(f"Serving math_specialist A2A on http://{HOST}:{PORT}")
    print("Agent card is published by the A2A app (see /.well-known/agent.json or docs).")
    uvicorn.run(app, host=HOST, port=PORT, log_level="info")


if __name__ == "__main__":
    main()
