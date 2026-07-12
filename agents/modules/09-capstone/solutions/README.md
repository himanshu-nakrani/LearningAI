# Capstone reference solution

## What “passing deep track” looks like

| Req | Reference location |
|-----|---------------------|
| R1–R4 tools/state/multi-agent | `../research_ops_assistant/agent.py` |
| R5 evalset (3 cases) | `../evals/research_ops.evalset.json` |
| R7 memory wiring | `../run_with_services.py` |
| R8 plugin | `../plugins/research_ops_plugin.py` |
| R9 conformance | `../conformance/` |

## How to use

1. Attempt the capstone yourself first.  
2. Diff your agent against `../research_ops_assistant/agent.py`.  
3. Run the reference path:

```bash
python modules/09-capstone/run_with_services.py
adk eval modules/09-capstone/research_ops_assistant \
  modules/09-capstone/evals/research_ops.evalset.json \
  --config_file_path=modules/09-capstone/evals/test_config.json
```

4. Fill `SUBMISSION.md` with **your** traces and scores (not copied empty).

## Architecture (reference)

```
Runner
  plugins=[ResearchOpsPlugin]   # logs + blocks EXFILTRATE_SECRETS
  memory_service=InMemoryMemoryService
  session_service=InMemorySessionService
  └── research_ops_coordinator
        ├── brief_agent
        ├── research_agent (+ search_knowledge_base, load_memory, save_notes)
        └── report_agent
```

## Grading note

Using this reference without understanding it fails oral defense / demo script expectations.
