"""Minimal BasePlugin registration demo.

Usage:
  python modules/12-callbacks-plugins/run_plugin_demo.py
"""

from __future__ import annotations

import asyncio

from google.adk.agents.base_agent import BaseAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.llm_agent import Agent
from google.adk.models.llm_request import LlmRequest
from google.adk.plugins.base_plugin import BasePlugin
from google.adk.runners import InMemoryRunner
from google.genai import types


class CountInvocationPlugin(BasePlugin):
    """Counts agent and model invocations (observe-only)."""

    def __init__(self) -> None:
        super().__init__(name="count_invocation")
        self.agent_count = 0
        self.llm_request_count = 0

    async def before_agent_callback(
        self, *, agent: BaseAgent, callback_context: CallbackContext
    ) -> None:
        self.agent_count += 1
        print(f"[Plugin] Agent run count: {self.agent_count}")

    async def before_model_callback(
        self, *, callback_context: CallbackContext, llm_request: LlmRequest
    ) -> None:
        self.llm_request_count += 1
        print(f"[Plugin] LLM request count: {self.llm_request_count}")


async def main() -> None:
    root_agent = Agent(
        model="gemini-flash-latest",
        name="hello_world",
        instruction="Reply with a short greeting.",
    )
    runner = InMemoryRunner(
        agent=root_agent,
        app_name="plugin_demo_app",
        plugins=[CountInvocationPlugin()],
    )
    session = await runner.session_service.create_session(
        user_id="user",
        app_name="plugin_demo_app",
    )
    prompt = types.Content(role="user", parts=[types.Part.from_text(text="hi")])
    async for event in runner.run_async(
        user_id="user",
        session_id=session.id,
        new_message=prompt,
    ):
        print(f"** event from {event.author}")


if __name__ == "__main__":
    asyncio.run(main())
