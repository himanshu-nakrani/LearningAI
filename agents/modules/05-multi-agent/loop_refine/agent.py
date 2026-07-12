"""Module 05 — LoopAgent with escalate exit (critique/refine).

Run:
  adk run modules/05-multi-agent/loop_refine
"""

from __future__ import annotations

from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.loop_agent import LoopAgent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.tools import ToolContext

MODEL = "gemini-flash-latest"
STATE_DOC = "current_document"
STATE_CRIT = "criticism"
COMPLETION = "No major issues found."


def exit_loop(tool_context: ToolContext) -> dict:
    """Call ONLY when critique says no further changes are needed.

    Sets escalate=True so the LoopAgent terminates.
    """
    tool_context.actions.escalate = True
    tool_context.actions.skip_summarization = True
    return {"status": "success", "exiting": True}


initial_writer = LlmAgent(
    name="InitialWriterAgent",
    model=MODEL,
    include_contents="none",
    description="Writes a minimal first draft.",
    instruction="""
Write a VERY basic first draft short story (1-2 plain sentences) on the user's topic.
Output only the story text.
""".strip(),
    output_key=STATE_DOC,
)

critic = LlmAgent(
    name="CriticAgent",
    model=MODEL,
    include_contents="none",
    description="Critiques the current draft or signals completion.",
    instruction=f"""
Review this draft:

```
{{{STATE_DOC}}}
```

Completion criteria (ALL must be met):
1. At least 4 sentences
2. Clear beginning, middle, end
3. At least one sensory or emotional detail

If incomplete, output ONLY concise critique.
If complete, respond EXACTLY: "{COMPLETION}"
""".strip(),
    output_key=STATE_CRIT,
)

refiner = LlmAgent(
    name="RefinerAgent",
    model=MODEL,
    include_contents="none",
    description="Refines draft or exits the loop.",
    instruction=f"""
Current document:
```
{{{STATE_DOC}}}
```
Critique:
{{{STATE_CRIT}}}

If critique is exactly "{COMPLETION}", call exit_loop and output nothing else.
Otherwise apply the critique and output ONLY the refined document.
""".strip(),
    tools=[exit_loop],
    output_key=STATE_DOC,
)

refinement_loop = LoopAgent(
    name="RefinementLoop",
    description="Critique then refine until done or max iterations.",
    sub_agents=[critic, refiner],
    max_iterations=5,
)

root_agent = SequentialAgent(
    name="IterativeWritingPipeline",
    description="Initial draft then iterative refinement loop.",
    sub_agents=[initial_writer, refinement_loop],
)
