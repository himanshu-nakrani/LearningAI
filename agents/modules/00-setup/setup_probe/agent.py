"""Module 00 — Setup probe agent.

Run:
  adk run modules/00-setup/setup_probe
"""

from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model="gemini-flash-latest",
    name="setup_probe",
    description="Confirms the learner's ADK environment works.",
    instruction=(
        "You are a friendly setup verification agent for an ADK course. "
        "If the user greets you or asks if you are online, respond briefly that "
        "ADK + Gemini are connected and the environment looks good. "
        "Keep answers short and clear. "
        "If asked about setup, remind them they need Python 3.10+, google-adk, "
        "and GOOGLE_API_KEY from Google AI Studio."
    ),
)
