"""CLI agent that can call load_memory when MemoryService is configured.

With plain `adk run`, memory may be empty unless you use a Runner with
memory_service (see run_memory_scenario.py). This agent still teaches the
tool wiring pattern.
"""

from google.adk.agents.llm_agent import Agent
from google.adk.tools import load_memory

root_agent = Agent(
    model="gemini-flash-latest",
    name="memory_recall_demo",
    description="Uses load_memory to answer questions about past chats when available.",
    instruction="""
You help users recall prior context.
If the question might depend on past conversations, call load_memory first.
If memory is empty or unavailable, say so and answer from the current session only.
""".strip(),
    tools=[load_memory],
)
