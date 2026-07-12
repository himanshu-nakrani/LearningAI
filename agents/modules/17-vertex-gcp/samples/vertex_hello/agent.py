"""Minimal agent for Vertex / Cloud Run / Agent Engine deploys.

Run locally (API key or Vertex env):
  adk run modules/17-vertex-gcp/samples/vertex_hello
"""

from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model="gemini-flash-latest",
    name="vertex_hello",
    description="Health-check agent for Vertex/GCP deploy labs.",
    instruction=(
        "You are a deploy smoke-test agent for the ADK course. "
        "If asked for health, reply that the Vertex-ready sample is up. "
        "Keep answers to 1-2 sentences."
    ),
)
