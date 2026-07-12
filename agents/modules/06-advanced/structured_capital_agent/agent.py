"""Module 06 — Structured output with Pydantic schema.

Run:
  adk run modules/06-advanced/structured_capital_agent
"""

from __future__ import annotations

from google.adk.agents.llm_agent import LlmAgent
from google.genai import types
from pydantic import BaseModel, Field


class CapitalInfo(BaseModel):
    """Structured capital city payload."""

    country: str = Field(description="Country name as understood from the query")
    capital: str = Field(description="Capital city of the country")
    confidence: float = Field(
        description="Model confidence between 0 and 1",
        ge=0.0,
        le=1.0,
    )


root_agent = LlmAgent(
    model="gemini-flash-latest",
    name="structured_capital_agent",
    description="Returns capital cities as strict JSON objects.",
    instruction="""
You are a Capital Information Agent.
Given a country (or a question about a country's capital), respond with a
JSON object matching the required schema only — no markdown fences, no prose.

If the country is ambiguous, pick the most common interpretation and lower confidence.
""".strip(),
    output_schema=CapitalInfo,
    output_key="capital_info",
    generate_content_config=types.GenerateContentConfig(
        temperature=0.1,
        max_output_tokens=256,
    ),
)
