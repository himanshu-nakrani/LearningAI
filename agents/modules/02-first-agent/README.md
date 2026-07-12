# Module 02 — Your First ADK Agent

**Time:** 2–3 hours · **Difficulty:** Beginner

## Objectives

- Configure a full `LlmAgent` / `Agent`
- Write clear instructions that drive tool use
- Implement a simple function tool
- Run via `adk run` and inspect behavior in `adk web`

---

## 1. Anatomy of an ADK agent

```python
from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model="gemini-flash-latest",          # required: which LLM
    name="root_agent",                    # required: unique id
    description="...",                    # recommended (routing)
    instruction="...",                    # critical: behavior
    tools=[...],                          # optional capabilities
)
```

| Field | Role |
|-------|------|
| `name` | Internal identity; used in multi-agent routing |
| `description` | Helps *other* agents decide when to delegate here |
| `model` | Intelligence / cost / latency tradeoff |
| `instruction` | Policy, persona, tool usage rules, output format |
| `tools` | Functions the model may call |

`Agent` is commonly an alias for `LlmAgent` — an LLM-powered, non-deterministic agent.

---

## 2. Instruction writing tips

Good instructions are **specific, procedural, and tool-aware**:

```text
You are a city time assistant.
When the user asks for the time in a city:
1. Extract the city name.
2. Call get_current_time with that city.
3. Reply with a short, friendly sentence including the city and time.
If the tool returns an error, apologize and suggest another city.
Do not invent times without calling the tool.
```

Techniques:

- Numbered steps for multi-stage behavior
- Explicit **do / don't**
- How to handle tool **errors**
- Few-shot examples for format-sensitive tasks
- State templates later: `User theme is {user:theme?}` (Module 04)

---

## 3. Your first tool

ADK wraps plain Python functions as tools. **Docstrings and type hints matter** — they become the schema the model sees.

```python
def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city: City name, e.g. "Tokyo" or "New York".

    Returns:
        dict with status and time or error_message.
    """
    ...
```

Prefer returning **dicts** with `status: "success" | "error"` so instructions can branch reliably.

---

## 4. Lab A — Time agent

Package: `modules/02-first-agent/time_agent`

```bash
# from course root, venv active, GOOGLE_API_KEY set
adk run modules/02-first-agent/time_agent
```

**Prompts to try:**

```
What time is it in New York?
Time in London please
What's the time in Atlantis?
```

**Expected behavior:**

- Known cities → tool call → real-ish mocked time
- Unknown city → tool error → polite message (no invented clocks)

### Dev UI + traces

```bash
adk web modules/02-first-agent --port 8000
```

Open the **Trace** tab after a turn. You should see model → function call → function response → final text.

---

## 5. Lab B — Improve the agent (exercises)

Edit `time_agent/agent.py` (or copy to `time_agent_v2/`):

1. **Add a city** to the mock database (e.g. `"mumbai"`).
2. **Add tool** `list_supported_cities()` and instruct the agent to call it when users ask “which cities?”
3. **Tone change:** make the agent reply like a ship captain (“Aye, in New York the bells strike…”).
4. **Guardrail:** refuse to discuss topics unrelated to time/cities.

### Stretch

- Use `datetime` + `zoneinfo` for real timezone conversion for 3 cities.
- Lower creativity: set `generate_content_config` with `temperature=0.2` (see Module 06).

---

## 6. Running agents programmatically (preview)

CLI is enough for labs. Under the hood:

```python
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

session_service = InMemorySessionService()
# await session_service.create_session(...)
runner = Runner(agent=root_agent, app_name="demo", session_service=session_service)
# events = runner.run(...) or run_async(...)
```

You will use this pattern more in Modules 04–07.

---

## 7. Mental model: one turn

```
User message
   → Runner loads Session (history + state)
   → LLM sees instruction + tools + contents
   → Maybe FunctionCall: get_current_time(city="London")
   → Tool executes, result appended
   → LLM produces final natural language
   → Event(s) saved on Session
```

---

## Checkpoint

1. Why is `description` important in multi-agent systems?
2. Why return `{"status": "error", ...}` instead of raising always?
3. What happens if your docstring is empty or misleading?
4. Where do you look in Dev UI to debug a wrong tool call?

**Solution notes:** see comments inside `time_agent/agent.py`.

---

## Next

→ [Module 03 — Tools Deep Dive](../03-tools/README.md)
