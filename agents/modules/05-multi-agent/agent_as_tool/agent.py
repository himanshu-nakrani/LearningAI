"""Module 05 — AgentTool: specialist agent invoked as a tool.

Run:
  adk run modules/05-multi-agent/agent_as_tool
"""

from __future__ import annotations

from google.adk.agents.llm_agent import Agent
from google.adk.tools.agent_tool import AgentTool

MODEL = "gemini-flash-latest"


def lookup_policy(topic: str) -> dict:
    """Looks up a demo company policy snippet.

    Args:
        topic: Policy topic such as refunds, shipping, or privacy.
    """
    policies = {
        "refunds": "Refunds within 30 days with receipt; digital goods non-refundable.",
        "shipping": "Standard 5-7 days; express 2 days in metro areas.",
        "privacy": "We store account email and order history; no sale of PII.",
    }
    key = topic.strip().lower()
    for k, v in policies.items():
        if k in key:
            return {"status": "success", "topic": k, "policy": v}
    return {
        "status": "error",
        "error_message": f"No policy for '{topic}'. Try refunds, shipping, privacy.",
    }


policy_specialist = Agent(
    model=MODEL,
    name="policy_specialist",
    description="Answers internal policy questions using lookup_policy.",
    instruction="""
You are a policy specialist. Always call lookup_policy for the topic.
Return a short factual answer from the tool. Do not invent policies.
""".strip(),
    tools=[lookup_policy],
)

# Wrap specialist so parent calls it like a tool (encapsulation).
policy_tool = AgentTool(agent=policy_specialist)

root_agent = Agent(
    model=MODEL,
    name="support_router",
    description="Front-line support that uses a policy specialist as a tool.",
    instruction="""
You are front-line support.
For any policy/legal/process question, call the policy_specialist tool
(AgentTool) rather than guessing.
For greetings/small talk, answer yourself briefly.
""".strip(),
    tools=[policy_tool],
)
