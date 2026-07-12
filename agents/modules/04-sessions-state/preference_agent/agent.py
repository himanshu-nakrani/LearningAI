"""Module 04 — Session state via tools.

Run:
  adk run modules/04-sessions-state/preference_agent
"""

from __future__ import annotations

from google.adk.agents.llm_agent import Agent
from google.adk.tools import ToolContext


def set_user_profile(
    name: str,
    theme: str,
    tool_context: ToolContext,
) -> dict:
    """Saves the user's display name and UI theme preference.

    Args:
        name: User's preferred display name.
        theme: UI theme, typically "light" or "dark".
        tool_context: Injected by ADK; do not pass manually.

    Returns:
        Status payload confirming saved values.
    """
    tool_context.state["user_name"] = name.strip()
    tool_context.state["user:theme"] = theme.strip().lower()
    return {
        "status": "success",
        "user_name": tool_context.state["user_name"],
        "theme": tool_context.state["user:theme"],
    }


def add_to_shopping_list(item: str, tool_context: ToolContext) -> dict:
    """Adds an item to the session shopping list.

    Args:
        item: Grocery or todo item to add.
        tool_context: Injected by ADK.

    Returns:
        Updated list in a status payload.
    """
    items = list(tool_context.state.get("shopping_list", []))
    cleaned = item.strip()
    if cleaned and cleaned not in items:
        items.append(cleaned)
    tool_context.state["shopping_list"] = items
    return {"status": "success", "shopping_list": items}


def remove_from_shopping_list(item: str, tool_context: ToolContext) -> dict:
    """Removes an item from the shopping list (case-insensitive match).

    Args:
        item: Item to remove.
        tool_context: Injected by ADK.

    Returns:
        Updated list or error if not found.
    """
    items = list(tool_context.state.get("shopping_list", []))
    target = item.strip().lower()
    new_items = [i for i in items if i.lower() != target]
    if len(new_items) == len(items):
        return {
            "status": "error",
            "error_message": f"'{item}' was not on the list.",
            "shopping_list": items,
        }
    tool_context.state["shopping_list"] = new_items
    return {"status": "success", "shopping_list": new_items}


def get_session_summary(tool_context: ToolContext) -> dict:
    """Returns known profile fields and shopping list from session state.

    Args:
        tool_context: Injected by ADK.

    Returns:
        Snapshot of relevant state keys.
    """
    return {
        "status": "success",
        "user_name": tool_context.state.get("user_name"),
        "theme": tool_context.state.get("user:theme"),
        "shopping_list": tool_context.state.get("shopping_list", []),
    }


root_agent = Agent(
    model="gemini-flash-latest",
    name="preference_agent",
    description="Remembers user preferences and a shopping list in session state.",
    instruction="""
You are a stateful personal assistant for a demo app.

Known state (may be empty):
- Display name: {user_name?}
- Theme: {user:theme?}
- Shopping list: {shopping_list?}

Capabilities:
- When the user shares name/theme, call set_user_profile.
- For shopping list add/remove, call add_to_shopping_list or remove_from_shopping_list.
- When asked what you know / to summarize, call get_session_summary and report it.

Rules:
- Prefer tools over guessing prior preferences.
- Confirm writes briefly.
- If list operations error, explain clearly.
""".strip(),
    tools=[
        set_user_profile,
        add_to_shopping_list,
        remove_from_shopping_list,
        get_session_summary,
    ],
)
