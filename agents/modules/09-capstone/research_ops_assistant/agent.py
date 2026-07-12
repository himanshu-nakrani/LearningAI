"""Capstone — Research Ops Assistant (required: multi-agent + state + tools).

Also designed for:
  - Memory tools (load_memory) when Runner has MemoryService
  - Plugin registration via run_with_services.py
  - Eval / conformance suites under modules/09-capstone/

Run (basic CLI):
  adk run modules/09-capstone/research_ops_assistant

Run (memory + plugin wiring):
  python modules/09-capstone/run_with_services.py
"""

from __future__ import annotations

from google.adk.agents.llm_agent import Agent
from google.adk.tools import ToolContext, load_memory

# ---------------------------------------------------------------------------
# Demo knowledge base
# ---------------------------------------------------------------------------

KNOWLEDGE = {
    "multi-agent": {
        "title": "Multi-agent systems",
        "bullets": [
            "Split roles to improve instruction following and modularity.",
            "Share data via session state and output_key pipelines.",
            "Evaluate trajectories, not only final prose.",
        ],
    },
    "evaluation": {
        "title": "Agent evaluation",
        "bullets": [
            "Compare tool trajectories to expected paths.",
            "Use ROUGE/semantic judges for final answers.",
            "Keep regression evals and conformance tests in CI.",
        ],
    },
    "sessions": {
        "title": "Sessions and memory",
        "bullets": [
            "Sessions hold events + state for one conversation thread.",
            "Use durable SessionService in production.",
            "Long-term MemoryService spans sessions; artifacts hold files.",
        ],
    },
    "plugins": {
        "title": "Plugins and guardrails",
        "bullets": [
            "Plugins register once on the Runner and apply globally.",
            "Prefer plugins for logging, metrics, and security policies.",
            "Plugin callbacks run before agent-local callbacks.",
        ],
    },
    "mcp": {
        "title": "MCP tools",
        "bullets": [
            "McpToolset connects ADK agents to MCP servers.",
            "Filter tools and limit filesystem roots in production.",
            "Define MCP tools synchronously for deploy.",
        ],
    },
}


def save_brief(
    question: str,
    scope: str,
    success_criteria: str,
    tool_context: ToolContext,
) -> dict:
    """Saves a structured research brief into session state.

    Args:
        question: Core research question.
        scope: What is in/out of scope.
        success_criteria: How we know the research is done.
        tool_context: Injected by ADK.

    Returns:
        Status and stored brief.
    """
    brief = {
        "question": question.strip(),
        "scope": scope.strip(),
        "success_criteria": success_criteria.strip(),
    }
    tool_context.state["brief"] = brief
    return {"status": "success", "brief": brief}


def search_knowledge_base(topic: str) -> dict:
    """Searches the demo knowledge base for a topic keyword.

    Args:
        topic: Topic key or free text (e.g. multi-agent, evaluation, sessions).

    Returns:
        Matching notes or an error if nothing found.
    """
    key = topic.strip().lower().replace("_", "-")
    for k, v in KNOWLEDGE.items():
        if k in key or key in k:
            return {"status": "success", "topic": k, "result": v}
    return {
        "status": "error",
        "error_message": (
            f"No demo knowledge for '{topic}'. "
            f"Try: {', '.join(KNOWLEDGE)}."
        ),
    }


def save_notes(notes: str, tool_context: ToolContext) -> dict:
    """Persists research notes string into session state.

    Args:
        notes: Synthesized notes from research tools.
        tool_context: Injected by ADK.

    Returns:
        Status payload.
    """
    tool_context.state["notes"] = notes.strip()
    return {"status": "success", "notes": tool_context.state["notes"]}


def save_report(report: str, tool_context: ToolContext) -> dict:
    """Persists the final report into session state.

    Args:
        report: Executive summary / final write-up.
        tool_context: Injected by ADK.

    Returns:
        Status payload.
    """
    tool_context.state["report"] = report.strip()
    return {"status": "success", "report": tool_context.state["report"]}


def list_action_items(tool_context: ToolContext) -> dict:
    """Returns action items from state or empty list."""
    items = tool_context.state.get("actions", [])
    return {"status": "success", "actions": items}


def add_action_item(item: str, tool_context: ToolContext) -> dict:
    """Appends an action item for the team."""
    items = list(tool_context.state.get("actions", []))
    cleaned = item.strip()
    if cleaned:
        items.append(cleaned)
    tool_context.state["actions"] = items
    return {"status": "success", "actions": items}


def get_pipeline_snapshot(tool_context: ToolContext) -> dict:
    """Returns brief, notes, report, and actions currently in session state."""
    return {
        "status": "success",
        "brief": tool_context.state.get("brief"),
        "notes": tool_context.state.get("notes"),
        "report": tool_context.state.get("report"),
        "actions": tool_context.state.get("actions", []),
    }


# ---------------------------------------------------------------------------
# Specialists
# ---------------------------------------------------------------------------

brief_agent = Agent(
    model="gemini-flash-latest",
    name="brief_agent",
    description="Turns a user question into a scoped research brief.",
    instruction="""
You create research briefs.
Ask only if the question is extremely vague; otherwise infer a reasonable scope.
Always call save_brief with question, scope, and success_criteria.
Then show the brief to the user.
""".strip(),
    tools=[save_brief],
)

research_agent = Agent(
    model="gemini-flash-latest",
    name="research_agent",
    description="Gathers notes from the demo knowledge base and saves them.",
    instruction="""
You research using tools only.

Current brief: {brief?}

Steps:
1. Call search_knowledge_base with relevant topics (may call multiple times).
   Supported topics include multi-agent, evaluation, sessions, plugins, mcp.
2. Optionally call load_memory if prior research context might help
   (only when a MemoryService is configured).
3. Merge findings into clear bullet notes.
4. Call save_notes with the merged notes.
5. Present the notes.

If search fails, report the error and do not invent sources.
""".strip(),
    tools=[search_knowledge_base, save_notes, load_memory],
)

report_agent = Agent(
    model="gemini-flash-latest",
    name="report_agent",
    description="Writes an executive summary from brief and notes in state.",
    instruction="""
You are the report writer.

Brief: {brief?}
Notes: {notes?}

If brief or notes are missing, say what is missing.

Otherwise write:
- Executive summary (5–8 sentences)
- Key findings (bullets)
- Risks / open questions
- Suggested next steps

Call save_report with the full report text.
Optionally call add_action_item for each concrete next step.
Then show the report to the user.
""".strip(),
    tools=[save_report, add_action_item, list_action_items],
)

root_agent = Agent(
    model="gemini-flash-latest",
    name="research_ops_coordinator",
    description=(
        "Coordinates brief, research, and report specialists for research ops."
    ),
    instruction="""
You are the Research Ops coordinator.

Specialists:
- brief_agent — scope the work
- research_agent — gather notes via knowledge tools (+ memory when available)
- report_agent — final write-up

Default pipeline for a new research question:
1. brief_agent
2. research_agent
3. report_agent
4. Deliver a short wrap-up pointing at the final report.

If the user asks for status / snapshot of the pipeline, call get_pipeline_snapshot
yourself or summarize known state fields.

If the user asks about something from a *previous session*, prefer load_memory
(when available) before saying you don't know.

Never fabricate knowledge base results.
""".strip(),
    tools=[get_pipeline_snapshot, load_memory],
    sub_agents=[brief_agent, research_agent, report_agent],
)
