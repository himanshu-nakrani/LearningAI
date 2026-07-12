# research_ops_assistant

Capstone multi-agent package.

## Run

```bash
# From course root
adk run modules/09-capstone/research_ops_assistant

# Memory + plugin demonstration
python modules/09-capstone/run_with_services.py
```

## Architecture

```
research_ops_coordinator
  ├── brief_agent      → save_brief → state.brief
  ├── research_agent   → search_knowledge_base, load_memory, save_notes
  └── report_agent     → save_report, add_action_item
```

## State

| Key | Meaning |
|-----|---------|
| `brief` | Scoped research brief dict |
| `notes` | Merged research notes string |
| `report` | Final report string |
| `actions` | List of action items |

## Limitations

- Knowledge base is in-process demo data  
- `load_memory` needs a Runner with `memory_service` (see `run_with_services.py`)  
- Plugins attach on Runner, not via plain `adk run` unless your ADK version injects them  
