# Glossary — Agentic AI & Google ADK

| Term | Definition |
|------|------------|
| **Agent** | Autonomous unit that uses an LLM (+ tools) to pursue a goal over one or more steps |
| **LlmAgent / Agent** | ADK class for model-powered agents |
| **Workflow agent** | Orchestrator with fixed control flow (Sequential, Parallel, Loop) |
| **Tool** | Callable capability (function, API, search, sub-agent) exposed to the model |
| **Function calling** | Model emits structured call args; runtime executes the tool |
| **Instruction** | System policy guiding persona, process, and tool use |
| **Description** | Short capability summary for routing among agents |
| **Session** | One conversation thread: ids, events, state |
| **Event** | Unit in history: user/model message, tool call/result, etc. |
| **State** | Key/value working memory on a session |
| **Memory** | Longer-lived knowledge across sessions (service-dependent) |
| **Artifact** | Persistent file-like object produced or consumed by agents |
| **Runner** | Runtime that drives agent execution against a session |
| **SessionService** | Storage lifecycle for sessions (memory, DB, Vertex) |
| **Trajectory** | Ordered steps (esp. tool calls) taken before final answer |
| **Planner** | Component that encourages multi-step plans before/while acting |
| **Callback** | Hook around model/tool lifecycle for logging, guards, metrics |
| **Sub-agent** | Child agent under a parent for hierarchy / transfer |
| **Agent-as-tool** | Specialist agent invoked like a tool by a parent |
| **output_key** | Writes agent final text into session state under a key |
| **output_schema** | Enforces structured JSON final responses |
| **Eval set** | Dataset of conversations + expected tools/responses |
| **ReAct** | Reason + Act loop pattern for tool-using agents |
| **Orchestration** | How multiple agents/nodes are scheduled and synchronized |
| **Guardrail** | Policy that constrains unsafe or out-of-scope behavior |
| **Hallucination** | Model content not grounded in tools/context |
| **Human-in-the-loop** | Require human approval for sensitive actions |
| **ADK Web** | Local Dev UI for chat, traces, and evals (not production) |
| **Agent Runtime** | Managed Google Cloud runtime for production agents |
| **MemoryService** | Long-term searchable knowledge across sessions |
| **Memory Bank** | Vertex managed memory extraction/search |
| **ArtifactService** | Versioned binary blob storage (session/user) |
| **Plugin** | Runner-global BasePlugin hooks (vs per-agent callbacks) |
| **McpToolset** | ADK client adapter for Model Context Protocol servers |
| **AgentTool** | Wrap an agent so a parent can call it as a tool |
| **SequentialAgent** | Deterministic A→B→C workflow |
| **ParallelAgent** | Concurrent sub-agent execution |
| **LoopAgent** | Repeat sub-agents until max or escalate |
| **Graph workflow** | ADK 2.0 explicit node/edge orchestration |
| **Dynamic workflow** | Programmatic workflow control (ADK 2.0) |
| **RunConfig** | Live/streaming run parameters |
| **InvocationContext** | Per-invocation services + session context |
| **Conformance test** | Golden replay regression for agent behavior |
| **Agent Config** | YAML/declarative agent authoring |
| **LiteLLM / Ollama / vLLM** | Alternate model connectors |
