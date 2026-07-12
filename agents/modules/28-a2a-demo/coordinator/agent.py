"""Coordinator that delegates math to a remote A2A specialist.

Requires serve_math_specialist.py running on A2A_URL (default :9001).
"""

from __future__ import annotations

import os

from google.adk.agents.llm_agent import Agent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

A2A_CARD_URL = os.getenv(
    "A2A_CARD_URL",
    "http://127.0.0.1:9001/.well-known/agent.json",
)

# RemoteA2aAgent accepts AgentCard object, URL, or file path to card JSON.
remote_math = RemoteA2aAgent(
    name="remote_math_specialist",
    description="Remote A2A math specialist (add/multiply).",
    agent_card=A2A_CARD_URL,
    timeout=60.0,
)

root_agent = Agent(
    model="gemini-flash-latest",
    name="a2a_coordinator",
    description="Routes math questions to a remote A2A specialist.",
    instruction="""
You coordinate work.
If the user asks arithmetic (add/multiply/sum/product), transfer or delegate
to remote_math_specialist.
For greetings, answer yourself briefly.
""".strip(),
    sub_agents=[remote_math],
)
