# Module 09 — Capstone: Research Ops Assistant (Expanded)

**Time:** 8–12 hours · **Difficulty:** Capstone (deep track)  
**Builds on:** Modules 00–08 + **10 (memory)** · **12 (plugins)** · **07 (eval/conformance)** · optional **17 (Vertex)**

## Mission

Ship a **Research Ops Assistant** that turns a research question into:

1. Scoped research **brief** (session state)  
2. Sourced **notes** (tools; no invented KB hits)  
3. Executive **report** + action items  
4. **Memory** recall across sessions (when MemoryService wired)  
5. **Plugin** observability / guardrails on the Runner  
6. **Eval + conformance** evidence for CI  

---

## Product brief

| | |
|--|--|
| **Users** | PMs, eng leads, analysts |
| **Input** | Natural language research questions |
| **Output** | Brief → notes → report → actions |
| **Constraints** | Demo KB OK; never invent tool results; label fiction |

Example prompts:

```
Research evaluation best practices for multi-agent systems.
What do we know about plugins and guardrails?
From past research, what did we say about evaluation?
```

---

## Required architecture

```
Runner
  ├── plugins=[ResearchOpsPlugin]     # REQUIRED (deep track)
  ├── memory_service=...              # REQUIRED (InMemory or Vertex)
  └── root_agent (coordinator)
        ├── brief_agent
        ├── research_agent  (+ load_memory, search_knowledge_base)
        └── report_agent
```

---

## Requirements (must pass)

| # | Requirement | Evidence |
|---|-------------|----------|
| **R1** | ≥ 4 tools with `{status,...}` contracts | code |
| **R2** | Session state: `brief`, `notes`, `report`, `actions` | code + demo |
| **R3** | Multi-agent hierarchy **or** Sequential pipeline | code |
| **R4** | No inventing KB results | instructions + eval miss case |
| **R5** | Eval set ≥ 3 cases (hit, miss, extra topic) | `evals/research_ops.evalset.json` |
| **R6** | Package README + architecture diagram | docs |
| **R7** | **Memory:** `load_memory` wired; demo cross-session recall | `run_with_services.py` |
| **R8** | **Plugin:** Runner-global plugin (log tools + 1 guardrail) | `plugins/research_ops_plugin.py` |
| **R9** | **Conformance:** `spec.yaml` + generate goldens **or** documented fallback | `conformance/` |

### Distinction stretch (90+)

| # | Stretch |
|---|---------|
| S1 | Vertex Memory Bank or DatabaseSessionService |
| S2 | Artifact for final report PDF/text |
| S3 | MCP or google_search integration |
| S4 | Deploy script notes (Module 17) |
| S5 | Parallel research fan-out |

---

## Starter package (runnable)

```bash
# Basic multi-agent CLI
adk run modules/09-capstone/research_ops_assistant

# REQUIRED deep demo: memory + plugin path
python modules/09-capstone/run_with_services.py

# Eval
adk eval \
  modules/09-capstone/research_ops_assistant \
  modules/09-capstone/evals/research_ops.evalset.json \
  --config_file_path=modules/09-capstone/evals/test_config.json \
  --print_detailed_results

# Conformance (after generating goldens — see conformance/README.md)
adk conformance test modules/09-capstone/conformance
```

Dev UI:

```bash
adk web modules/09-capstone --port 8000
```

---

## Layout

```
09-capstone/
├── README.md
├── SUBMISSION.template.md
├── run_with_services.py          # memory + plugin runner
├── plugins/
│   └── research_ops_plugin.py
├── research_ops_assistant/
│   ├── agent.py
│   └── __init__.py
├── evals/
│   ├── research_ops.evalset.json
│   └── test_config.json
└── conformance/
    ├── README.md
    └── research_ops_basic/
        └── spec.yaml
```

---

## Suggested build order

1. Confirm multi-agent pipeline (brief → research → report)  
2. Expand KB topics (`plugins`, `mcp`) and eval cases  
3. Wire `load_memory` + `run_with_services.py` memory ingest  
4. Implement / tune `ResearchOpsPlugin`  
5. Run `adk eval` and fix trajectory mismatches  
6. Generate conformance goldens; document results  
7. Fill `SUBMISSION.md` from template  

---

## Rubric (100)

| Criteria | Pts |
|----------|-----|
| Clear problem + agent boundaries | 10 |
| Tools + error handling | 15 |
| Multi-agent / workflow design | 15 |
| Session/state intentional use | 10 |
| **Memory integration (R7)** | 10 |
| **Plugin integration (R8)** | 10 |
| **Eval + conformance (R5/R9)** | 15 |
| Docs & run instructions | 10 |
| Stretch (S1–S5) | 5 |

- **Pass (deep):** **75+** and **R1–R9** met  
- **Pass (core-only legacy):** 70+ without R7–R9 is **not** enough for deep-track certificate  
- **Distinction:** **90+**

---

## Demo script (7 minutes)

1. Cold research question → brief/notes/report  
2. `run_with_services.py` second session memory recall  
3. Plugin blocks `EXFILTRATE_SECRETS`  
4. Show eval CLI summary  
5. Show conformance folder / fallback note  
6. Limitations + next production steps (Vertex optional)  

---

## Submission

Copy `SUBMISSION.template.md` → `SUBMISSION.md` and complete every section.

---

## Related modules

- [10 Memory](../10-memory/README.md)  
- [12 Callbacks & Plugins](../12-callbacks-plugins/README.md)  
- [07 Evaluation](../07-evaluation/README.md)  
- [17 Vertex / GCP](../17-vertex-gcp/README.md)  
