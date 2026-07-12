"""Module 05 — Deterministic SequentialAgent pipeline.

Run:
  adk run modules/05-multi-agent/sequential_research
"""

from __future__ import annotations

from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent

MODEL = "gemini-flash-latest"

outline_agent = LlmAgent(
    name="outline_agent",
    model=MODEL,
    description="Creates a structured outline for the user topic.",
    instruction="""
You are an outlining specialist.
Given the user's topic, produce a concise bullet outline (5–8 bullets).
Output only the outline — no preamble.
""".strip(),
    output_key="outline",
)

draft_agent = LlmAgent(
    name="draft_agent",
    model=MODEL,
    description="Writes a draft from the outline in state.",
    instruction="""
You are a technical writer.

Outline:
{outline}

Write a clear 2–4 paragraph draft covering the outline.
Audience: software engineers new to agentic systems.
Output only the draft.
""".strip(),
    output_key="draft",
)

editor_agent = LlmAgent(
    name="editor_agent",
    model=MODEL,
    description="Edits the draft for clarity and structure.",
    instruction="""
You are a strict editor.

Draft:
{draft}

Improve clarity, fix fluff, keep technical accuracy.
Return the final polished article only (markdown allowed).
""".strip(),
    output_key="final_article",
)

root_agent = SequentialAgent(
    name="research_pipeline",
    description="Runs outline → draft → edit in a fixed sequence.",
    sub_agents=[outline_agent, draft_agent, editor_agent],
)
