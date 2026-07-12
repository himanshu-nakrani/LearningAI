"""Capstone required plugin: logging + light policy guardrail.

Compatible with google-adk 2.x BasePlugin signatures.
"""

from __future__ import annotations

from typing import Any, Optional

from google.adk.agents.base_agent import BaseAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.adk.plugins.base_plugin import BasePlugin
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from google.genai import types


class ResearchOpsPlugin(BasePlugin):
    """Cross-cutting plugin for Research Ops Assistant.

    - Counts agent / model / tool invocations
    - Blocks user messages containing EXFILTRATE_SECRETS
    """

    def __init__(self) -> None:
        super().__init__(name="research_ops_plugin")
        self.agent_count = 0
        self.model_count = 0
        self.tool_count = 0
        self.blocked = 0

    async def before_agent_callback(
        self, *, agent: BaseAgent, callback_context: CallbackContext
    ) -> Optional[types.Content]:
        self.agent_count += 1
        print(f"[ResearchOpsPlugin] agent_start name={agent.name} n={self.agent_count}")
        return None

    async def before_model_callback(
        self, *, callback_context: CallbackContext, llm_request: LlmRequest
    ) -> Optional[LlmResponse]:
        self.model_count += 1
        last = _last_user_text(llm_request)
        if "EXFILTRATE_SECRETS" in last.upper():
            self.blocked += 1
            print("[ResearchOpsPlugin] blocked disallowed user request")
            return LlmResponse(
                content=types.Content(
                    role="model",
                    parts=[
                        types.Part(
                            text=(
                                "Request blocked by ResearchOpsPlugin policy "
                                "(disallowed content)."
                            )
                        )
                    ],
                )
            )
        return None

    async def before_tool_callback(
        self,
        *,
        tool: BaseTool,
        tool_args: dict[str, Any],
        tool_context: ToolContext,
    ) -> Optional[dict]:
        self.tool_count += 1
        name = getattr(tool, "name", str(tool))
        keys = sorted(tool_args.keys()) if isinstance(tool_args, dict) else []
        print(
            f"[ResearchOpsPlugin] tool_call name={name} "
            f"arg_keys={keys} n={self.tool_count}"
        )
        return None


def _last_user_text(llm_request: LlmRequest) -> str:
    contents = getattr(llm_request, "contents", None) or []
    if not contents:
        return ""
    last = contents[-1]
    if getattr(last, "role", None) != "user":
        return ""
    parts = getattr(last, "parts", None) or []
    if not parts:
        return ""
    return getattr(parts[0], "text", None) or ""
