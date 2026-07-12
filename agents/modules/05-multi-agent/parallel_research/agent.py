"""Module 05 — ParallelAgent + Sequential merge pipeline.

Run:
  adk run modules/05-multi-agent/parallel_research

Note: Uses mock research tools (no live google_search) so labs work offline.
Swap in google_search from google.adk.tools when API/tooling allows.
"""

from __future__ import annotations

from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.parallel_agent import ParallelAgent
from google.adk.agents.sequential_agent import SequentialAgent

MODEL = "gemini-flash-latest"


def research_topic_a(query: str) -> dict:
    """Returns mock research notes for renewable energy (demo)."""
    return {
        "status": "success",
        "topic": "renewable_energy",
        "summary": (
            f"Demo findings for '{query}': solar LCOE continues to fall; "
            "grid storage deployment is accelerating in utility markets."
        ),
    }


def research_topic_b(query: str) -> dict:
    """Returns mock research notes for electric vehicles (demo)."""
    return {
        "status": "success",
        "topic": "ev_technology",
        "summary": (
            f"Demo findings for '{query}': solid-state battery pilots expand; "
            "charging networks densify on major corridors."
        ),
    }


def research_topic_c(query: str) -> dict:
    """Returns mock research notes for carbon capture (demo)."""
    return {
        "status": "success",
        "topic": "carbon_capture",
        "summary": (
            f"Demo findings for '{query}': DAC remains costly; "
            "point-source capture leads near-term industrial abatement."
        ),
    }


researcher_a = LlmAgent(
    name="RenewableEnergyResearcher",
    model=MODEL,
    description="Researches renewable energy (demo tool).",
    instruction="""
Research renewable energy for the user request.
Call research_topic_a once. Output ONLY a 1-2 sentence summary of the tool result.
""".strip(),
    tools=[research_topic_a],
    output_key="renewable_energy_result",
)

researcher_b = LlmAgent(
    name="EVResearcher",
    model=MODEL,
    description="Researches EV technology (demo tool).",
    instruction="""
Research EV technology for the user request.
Call research_topic_b once. Output ONLY a 1-2 sentence summary of the tool result.
""".strip(),
    tools=[research_topic_b],
    output_key="ev_technology_result",
)

researcher_c = LlmAgent(
    name="CarbonCaptureResearcher",
    model=MODEL,
    description="Researches carbon capture (demo tool).",
    instruction="""
Research carbon capture for the user request.
Call research_topic_c once. Output ONLY a 1-2 sentence summary of the tool result.
""".strip(),
    tools=[research_topic_c],
    output_key="carbon_capture_result",
)

parallel_research_agent = ParallelAgent(
    name="ParallelWebResearchAgent",
    description="Runs three research agents concurrently.",
    sub_agents=[researcher_a, researcher_b, researcher_c],
)

merger_agent = LlmAgent(
    name="SynthesisAgent",
    model=MODEL,
    description="Merges parallel research results from state.",
    instruction="""
Synthesize a short report grounded ONLY on these inputs:

Renewable energy: {renewable_energy_result?}
Electric vehicles: {ev_technology_result?}
Carbon capture: {carbon_capture_result?}

Use headings for each topic and a 1-2 sentence conclusion.
Do not invent facts beyond the inputs.
""".strip(),
)

root_agent = SequentialAgent(
    name="ResearchAndSynthesisPipeline",
    description="Parallel research then sequential synthesis.",
    sub_agents=[parallel_research_agent, merger_agent],
)
