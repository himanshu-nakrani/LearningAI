"""Module 12 — before_model_callback guardrail lab."""

from __future__ import annotations

from typing import Optional

from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.llm_agent import LlmAgent
from google.adk.models import LlmRequest, LlmResponse
from google.genai import types


def simple_before_model_modifier(
    callback_context: CallbackContext,
    llm_request: LlmRequest,
) -> Optional[LlmResponse]:
    """Blocks requests containing BLOCK; otherwise allows the LLM call."""
    last_user = ""
    if llm_request.contents and llm_request.contents[-1].role == "user":
        parts = llm_request.contents[-1].parts or []
        if parts and parts[0].text:
            last_user = parts[0].text

    if "BLOCK" in last_user.upper():
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[
                    types.Part(
                        text="Request blocked by before_model_callback guardrail."
                    )
                ],
            )
        )
    return None


root_agent = LlmAgent(
    model="gemini-flash-latest",
    name="guardrail_agent",
    description="Demo agent with a before_model BLOCK guardrail.",
    instruction="You are a helpful assistant. Keep answers short.",
    before_model_callback=simple_before_model_modifier,
)
