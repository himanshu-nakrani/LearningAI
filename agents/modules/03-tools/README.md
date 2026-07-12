# Module 03 — Tools Deep Dive

**Time:** 3–4 hours · **Difficulty:** Beginner → Intermediate

## Objectives

- Design reliable function tools (contracts, errors, docstrings)
- Chain multiple tools in one turn / multi-turn
- Use `ToolContext` for advanced control (preview of state)
- Know built-in / integration tools vs custom tools
- Treat agents-as-tools as a composition pattern

---

## 1. What is a tool in ADK?

A **tool** is developer-defined, deterministic (or semi-deterministic) code the LLM can invoke via function calling.

The model:

1. **Selects** a tool from names + descriptions
2. **Fills** arguments from schema
3. **Receives** the return value as observation
4. **Continues** reasoning toward a user-facing answer

Tools do **not** “think.” The LLM thinks; tools execute.

---

## 2. Tool types

| Type | Use when |
|------|----------|
| **Function tool** | Custom business logic, APIs, DB queries |
| **Long-running tool** | Jobs that pause / resume (async workflows) |
| **Built-in / integrations** | Google Search, code execution, RAG, etc. |
| **Agent-as-tool** | Encapsulate a specialist agent behind a tool interface |
| **MCP / third-party** | Connect external tool ecosystems |

Docs: [Custom tools](https://adk.dev/tools-custom/) · [Integrations](https://adk.dev/integrations/)

---

## 3. Designing a good tool API

### Naming

- Verbs + nouns: `get_weather_report`, `create_ticket`, `search_catalog`
- Avoid vague names: `handle`, `process`, `do_stuff`

### Docstrings

The model reads them. Include:

- What the tool does
- When to use it (implicit via description)
- Argument meanings
- Return shape and error cases

### Return values

Prefer structured, stable JSON-serializable dicts:

```python
{"status": "success", "report": "..."}
{"status": "error", "error_message": "..."}
```

**Do not** rely on exceptions alone for expected failures (unknown city, not found). Exceptions are for unexpected bugs.

### Side effects

- Make mutations **idempotent** when possible
- Log externally with correlation IDs for prod
- Prefer dry-run flags for destructive ops

---

## 4. ToolContext (advanced control)

Add `tool_context: ToolContext` as a parameter (not in the docstring). ADK injects it.

Common uses:

```python
from google.adk.tools import ToolContext

def save_preference(theme: str, tool_context: ToolContext) -> dict:
    """Saves the user's UI theme preference."""
    tool_context.state["user:theme"] = theme
    return {"status": "success", "theme": theme}
```

Also available on context/actions (see Module 04–05):

- Read/write **state**
- `transfer_to_agent` for handoffs
- `skip_summarization`
- Artifact / memory service access

---

## 5. Instructing the model about tools

In `instruction`, reference tools by **function name**:

```text
If the user asks about weather, call get_weather_report.
If it returns status "error", tell the user and ask for another city.
After a successful report, if the user reacts emotionally, call analyze_sentiment.
```

Describe **sequences** when order matters.

---

## 6. Lab — Weather + sentiment agent

Package: `modules/03-tools/weather_sentiment_agent`

```bash
adk run modules/03-tools/weather_sentiment_agent
```

**Scripted conversation:**

```
What's the weather in London?
I don't like rain.
Weather in Berlin?
```

**Observe:**

1. Tool call for weather
2. Tool call for sentiment after feedback
3. Graceful handling of unknown cities

### Exercises

1. Add `get_weather_report` data for **Berlin** and **Mumbai**.
2. Add a third tool `suggest_activity(weather_summary: str)` that returns indoor/outdoor ideas.
3. Update instructions so the agent **always** suggests an activity after a successful weather fetch.
4. Force structured errors: never return free-form strings from tools—only dicts.

### Stretch

- Wrap tools explicitly with `FunctionTool(func=...)`.
- Add a fake `httpx`-style comment block showing how you’d call a real weather API.
- Try `google_search` built-in tool in a separate mini-agent (requires model/tool support in your environment).

---

## 7. Anti-patterns

| Anti-pattern | Prefer |
|--------------|--------|
| One mega-tool that does everything | Small tools, single responsibility |
| Tools returning prose paragraphs | Structured fields + let LLM phrase |
| Hidden globals for per-user data | Session/user state via ToolContext |
| 20 tools dumped on one agent | Split agents / workflows |
| Undocumented optional args | Explicit required params |

---

## 8. Complete tool taxonomy (ADK)

| Type | Module / notes |
|------|----------------|
| Function / FunctionTool | This module |
| LongRunningFunctionTool | Async jobs, human wait — see M13 |
| AgentTool | M05 `agent_as_tool` |
| Built-ins (`google_search`, code exec, memory, artifacts) | M10–M13 |
| MCP `McpToolset` | M13 |
| Third-party integrations | [adk.dev/integrations](https://adk.dev/integrations/) |

### ToolContext.actions (must know)

| Action | Effect |
|--------|--------|
| `transfer_to_agent = "name"` | Hand off to sub-agent |
| `escalate = True` | Bubble up / stop LoopAgent |
| `skip_summarization = True` | Skip LLM summary of tool output |

### Error-handling contract (recommended)

```python
{"status": "success", ...}
{"status": "error", "error_message": "..."}
```

Instruction must tell the model how to react to each status.

### Built-in google_search sketch

```python
from google.adk.tools import google_search
agent = Agent(..., tools=[google_search])
```

Requires model/tool support in your environment; mock tools are used in offline labs.

---

## Checkpoint

1. Who decides *which* tool to call—the tool or the LLM?
2. Why put `status` in every tool response?
3. Should `tool_context` appear in the tool docstring? Why?
4. When would you use **agent-as-tool** instead of sub_agents transfer?

---

## Next

→ [Module 04 — Sessions, State & Memory](../04-sessions-state/README.md)
