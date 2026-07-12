# Module 13 — MCP Tools, Built-ins & Integrations

**Time:** 3–4 hours · **Docs:** [MCP tools](https://adk.dev/tools-custom/mcp-tools/) · [Integrations](https://adk.dev/integrations/)

## Objectives

- Use ADK as an **MCP client** via `McpToolset`  
- Connect with **Stdio** (local npx servers) and **HTTP/SSE** (remote)  
- Filter tools for least privilege  
- Understand reverse pattern: expose ADK tools as an MCP server  
- Catalog built-in tools and ecosystem integrations  
- Deploy agents that embed MCP safely  

---

## 1. MCP in one minute

MCP standardizes how LLMs talk to external tools/resources.

```
LlmAgent ──tools──► McpToolset ──protocol──► MCP Server ──► real tools
```

`McpToolset`:

1. Connects (stdio / SSE / streamable HTTP)  
2. `list_tools` → ADK `BaseTool` adapters  
3. Proxies `call_tool` when the model invokes them  
4. Optional `tool_filter`  

**Deploy rule:** define agent + McpToolset **synchronously** in `agent.py` (async factories break Cloud Run / Agent Runtime).

---

## 2. Pattern A — Filesystem MCP (local)

```python
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
import os

FOLDER = os.path.abspath("./sandbox")

root_agent = LlmAgent(
    model="gemini-flash-latest",
    name="filesystem_assistant",
    instruction="Help manage files in the allowed folder only.",
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="npx",
                    args=["-y", "@modelcontextprotocol/server-filesystem", FOLDER],
                ),
            ),
            tool_filter=["list_directory", "read_file"],
        )
    ],
)
```

Requires Node.js/`npx` for community servers.

---

## 3. Pattern B — Remote HTTP MCP

```python
McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="https://example-mcp.server/mcp",
        headers={"Authorization": f"Bearer {token}"},
    )
)
```

Example: Google Maps Grounding Lite (`mapstools.googleapis.com/mcp`).

---

## 4. Pattern C — Expose ADK tools as MCP server

Use `mcp` Python SDK + `adk_to_mcp_tool_type` conversion utilities so any MCP client can call your ADK `FunctionTool`s. See official “Build an MCP server with ADK tools” section.

---

## 5. Built-in & integration catalog (study list)

Study each category on [integrations](https://adk.dev/integrations/):

| Category | Examples |
|----------|----------|
| Search / web | `google_search`, enterprise web search, Firecrawl |
| Maps | Google Maps grounding |
| Code | Built-in code execution |
| Data / DB | BigQuery, AlloyDB, Redis, Aerospike |
| Memory plugins | third-party persistent memory |
| Productivity | Workspace, Notion-style connectors |
| Resilience | Reflect and Retry plugin |
| Observability | BigQuery agent analytics, logging plugins |

You do **not** need every integration installed — know **when** to reach for each.

---

## 6. Other tool types (complete the toolkit)

### LongRunningFunctionTool

For operations that pause, wait on humans, or resume later (async jobs). See custom tools docs for signature patterns.

### Code execution

```python
from google.adk.code_executors import BuiltInCodeExecutor
# or code execution tools depending on version
agent = LlmAgent(..., code_executor=BuiltInCodeExecutor())
```

### Agent Skills

Portable skill packages ([agentskills.io](https://agentskills.io/)) that inject capabilities without bloating instructions — see ADK Skills docs.

---

## 7. Lab — Runnable MCP filesystem agent

**Full setup:** [SETUP_MCP.md](SETUP_MCP.md)

Package: `mcp_filesystem_agent/` with a curated `sandbox/` (policies, CSV, hello.txt).

```bash
# Requires Node.js (npx) + pip install mcp
adk run modules/13-mcp-integrations/mcp_filesystem_agent
```

The agent loads `McpToolset` **synchronously** with a **read-only** `tool_filter` rooted at `./sandbox`.  
If Node is missing, `mcp_status` still runs and explains how to fix setup.

### Exercises

1. Add a new file under `sandbox/` and have the agent read it.  
2. Write a security review: which filesystem tools are excluded and why?  
3. Compare AgentTool vs MCP vs FunctionTool for “check weather”.  
4. Sketch a Dockerfile that installs Node + the MCP server for Cloud Run.  
5. (Stretch) Connect a remote MCP (Maps Grounding Lite) with API key headers.

Legacy scaffold: `mcp_filesystem.example.py` (comments only).

---

## Checkpoint

1. What does McpToolset do on agent start?  
2. Why synchronous definition for deploy?  
3. Stdio vs SSE MCP — when each?  

## Next

→ [Module 14 — Graphs & Advanced Workflows](../14-graphs-workflows/README.md)
