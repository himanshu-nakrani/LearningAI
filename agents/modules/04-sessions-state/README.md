# Module 04 — Sessions, State & Memory

**Time:** 3–4 hours · **Difficulty:** Intermediate

## Objectives

- Explain Session vs Event history vs State vs long-term Memory
- Use session services: in-memory, database, Vertex AI
- Read/write state from tools via `ToolContext`
- Inject state into instructions with `{var}` / `{var?}`
- Apply state key prefixes (`user:`, `app:`, `temp:`)

---

## 1. Mental model

| Concept | Lifetime | Purpose |
|---------|----------|---------|
| **Session** | One conversation thread | Container for events + state |
| **Events** | Ordered history in the session | User msgs, model msgs, tool calls |
| **State** | Key/value scratchpad on the session | Working memory, shared fields |
| **Memory** (long-term) | Across sessions (if configured) | Preferences, facts that should persist longer |

Analogy:

- **Session** = chat room
- **Events** = transcript
- **State** = whiteboard in that room
- **Memory** = CRM profile outside the room

---

## 2. Session object (recap)

Properties typically include:

- `id`, `app_name`, `user_id`
- `events` — chronological interactions
- `state` — dict-like working data
- `last_update_time`

You rarely construct sessions manually; use a **`SessionService`**:

```python
from google.adk.sessions import InMemorySessionService

session_service = InMemorySessionService()
session = await session_service.create_session(
    app_name="prefs_app",
    user_id="user_1",
    state={"onboarding_complete": False},
)
```

---

## 3. SessionService implementations

| Service | Persistence | Best for |
|---------|-------------|----------|
| `InMemorySessionService` | No (lost on restart) | Local labs, unit tests |
| `DatabaseSessionService` | Yes (SQLite/Postgres/…) | Self-hosted apps |
| `VertexAiSessionService` | Yes (GCP Agent Platform) | Production on Google Cloud |

SQLite example (async driver required):

```python
from google.adk.sessions import DatabaseSessionService

session_service = DatabaseSessionService(
    db_url="sqlite+aiosqlite:///./my_agent_data.db"
)
```

---

## 4. State prefixes

| Key pattern | Scope |
|-------------|--------|
| `my_key` (no prefix) | Current session only |
| `user:theme` | User across sessions (when backend supports) |
| `app:feature_flag` | All users of the app |
| `temp:scratch` | Temporary; not for durable storage |

Write from a tool:

```python
def set_theme(theme: str, tool_context: ToolContext) -> dict:
    """Sets the user's preferred UI theme (light or dark)."""
    tool_context.state["user:theme"] = theme
    tool_context.state["theme_updated"] = True
    return {"status": "success", "theme": theme}
```

---

## 5. Instruction templating

ADK instructions can interpolate state:

```python
instruction="""
You are a personal assistant.
User display name: {user_name?}
Preferred theme: {user:theme?}
Shopping list: {shopping_list?}
...
"""
```

- `{var}` — required; may error if missing
- `{var?}` — optional; empty if missing

This is how multi-agent pipelines pass intermediate results without stuffing everything into free-form chat.

Also: `output_key="found_capital"` stores the agent’s final text into state under that key (Module 05–06).

---

## 6. Lab — Preference agent

Package: `modules/04-sessions-state/preference_agent`

```bash
adk run modules/04-sessions-state/preference_agent
```

**Try multi-turn:**

```
My name is Alex and I like dark mode.
What do you know about me?
Add milk and eggs to my shopping list.
Show my shopping list.
Remove milk.
```

**What to notice:**

- Tools mutate `tool_context.state`
- Later turns still “know” preferences (same session)
- Restarting CLI with InMemory loses state (by design)

### Exercises

1. Add `user:language` preference and greet in that language when set.
2. Add tool `clear_shopping_list`.
3. Change instruction to print state fields using `{shopping_list?}`.
4. **Stretch:** switch the programmatic runner (see `run_demo.py`) to `DatabaseSessionService` and restart process—state should survive.

---

## 7. Session lifecycle (one turn)

1. Create or resume session via `SessionService`
2. Runner supplies session to agent
3. Agent reasons; tools may update state
4. Runner appends events; state deltas persist
5. Next turn loads updated session

---

## 8. Memory vs state (practical rule)

| Need | Use |
|------|-----|
| Values needed for *this* workflow | Session **state** |
| Full dialogue for context | Session **events** (automatic) |
| Facts across days/products | Long-term **memory** / external DB |
| Large files (PDFs, images) | **Artifacts**, not giant state strings |

---

## Checkpoint

1. Difference between `events` and `state`?
2. What happens to InMemory sessions after process exit?
3. Why use `{theme?}` instead of `{theme}` during onboarding?
4. Which prefix would you use for a feature flag shared by all users?

---

## Next

→ [Module 05 — Multi-Agent Workflows](../05-multi-agent/README.md)
