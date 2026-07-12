"""Agent whose instruction embeds the research-brief skill text."""

from pathlib import Path

from google.adk.agents.llm_agent import Agent
from google.adk.skills import load_skill_from_dir

_SKILL_DIR = (
    Path(__file__).resolve().parents[1] / "skills_repo" / "research-brief"
)
_skill = load_skill_from_dir(str(_SKILL_DIR))
_skill_body = _skill.instructions

root_agent = Agent(
    model="gemini-flash-latest",
    name="skill_agent",
    description="Uses the research-brief skill procedure.",
    instruction=f"""
You follow the Research Brief skill exactly.

--- SKILL ---
{_skill_body}
--- END SKILL ---

When the user asks anything research-related, apply the skill.
""".strip(),
)
