"""Minimal agent for deployment demos."""

from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model="gemini-flash-latest",
    name="sample_deploy_agent",
    description="Tiny health-check style agent for deployment demos.",
    instruction=(
        "You are a deployment demo agent. "
        "Answer briefly. If asked for health, reply that the service is up."
    ),
)
