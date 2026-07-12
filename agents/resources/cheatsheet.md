# ADK Cheatsheet

## Install & auth

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install google-adk
export GOOGLE_API_KEY=...
```

## CLI

```bash
adk create my_agent
adk run my_agent
adk web --port 8000          # parent of agent folders
adk eval <agent> <evalset>
adk deploy cloud_run --help
```

## Minimal agent

```python
from google.adk.agents.llm_agent import Agent

def get_x(q: str) -> dict:
    """Does X. Returns status dict."""
    return {"status": "success", "result": q}

root_agent = Agent(
    model="gemini-flash-latest",
    name="root_agent",
    description="Does X.",
    instruction="Use get_x when needed. Handle errors.",
    tools=[get_x],
)
```

## Package layout

```
my_agent/
  __init__.py   # from . import agent
  agent.py      # root_agent = ...
  .env          # GOOGLE_API_KEY=...
```

## ToolContext state

```python
from google.adk.tools import ToolContext

def save(v: str, tool_context: ToolContext) -> dict:
    """Saves v."""
    tool_context.state["my_key"] = v
    tool_context.state["user:pref"] = v
    return {"status": "success"}
```

Instruction inject: `{my_key?}` `{user:pref?}`

## Sequential pipeline

```python
from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent

a = LlmAgent(..., output_key="a_out")
b = LlmAgent(..., instruction="Use {a_out}", output_key="b_out")
root_agent = SequentialAgent(name="pipe", sub_agents=[a, b])
```

## Hierarchy

```python
child = Agent(name="child", ...)
root_agent = Agent(name="parent", sub_agents=[child], instruction="...")
```

## Structured output

```python
from pydantic import BaseModel, Field

class Out(BaseModel):
    answer: str = Field(description="...")

agent = LlmAgent(..., output_schema=Out, output_key="out")
```

## Programmatic run (async sketch)

```python
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

svc = InMemorySessionService()
await svc.create_session(app_name="app", user_id="u", session_id="s")
runner = Runner(agent=root_agent, app_name="app", session_service=svc)
content = types.Content(role="user", parts=[types.Part(text="hi")])
async for event in runner.run_async(user_id="u", session_id="s", new_message=content):
    if event.is_final_response():
        print(event.content.parts[0].text)
```

## Session services

```python
InMemorySessionService()
DatabaseSessionService(db_url="sqlite+aiosqlite:///./data.db")
# VertexAiSessionService(project=..., location=...)
```

## Eval criteria sample

```json
{
  "criteria": {
    "tool_trajectory_avg_score": 1.0,
    "response_match_score": 0.8
  }
}
```

## Instruction recipe

```text
Role: ...
Goal: ...
Process: numbered steps
Tools: when to call each by name
Errors: what to do on status=error
Style: concise / JSON / markdown
Boundaries: refuse off-topic / unsafe
```

## State prefixes

| Prefix | Scope |
|--------|--------|
| (none) | session |
| `user:` | user |
| `app:` | app-wide |
| `temp:` | ephemeral |

## Workflow agents

```python
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.agents.parallel_agent import ParallelAgent
from google.adk.agents.loop_agent import LoopAgent

SequentialAgent(name="pipe", sub_agents=[a, b, c])
ParallelAgent(name="fanout", sub_agents=[a, b, c])
LoopAgent(name="loop", sub_agents=[critic, refiner], max_iterations=5)
```

Exit loop:

```python
tool_context.actions.escalate = True
```

## AgentTool

```python
from google.adk.tools.agent_tool import AgentTool
tools=[AgentTool(agent=specialist)]
```

## Memory

```python
from google.adk.memory import InMemoryMemoryService
from google.adk.tools import load_memory, preload_memory
await memory_service.add_session_to_memory(session)
Runner(..., memory_service=memory_service)
```

## Artifacts

```python
from google.adk.artifacts import InMemoryArtifactService
Runner(..., artifact_service=InMemoryArtifactService())
await tool_context.save_artifact("f.txt", part)
await tool_context.load_artifact("f.txt")
```

## Callbacks / plugins

```python
LlmAgent(..., before_model_callback=fn)  # return None or LlmResponse
InMemoryRunner(..., plugins=[MyPlugin()])
```

## MCP (sketch)

```python
from google.adk.tools.mcp_tool import McpToolset
# StdioConnectionParams + StdioServerParameters(command="npx", args=[...])
```

## Deploy

```bash
adk deploy cloud_run --project=... --region=... --service_name=... ./agent_dir
adk deploy agent_engine --project=... --region=... --staging_bucket=gs://... ./agent_dir
adk api_server ./agents_parent
adk conformance test
```

## Full coverage checklist

See [ADK_COVERAGE.md](../ADK_COVERAGE.md).
