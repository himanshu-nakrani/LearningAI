# Module 22 — Database Session Service

**Time:** 1–2 hours · **Requires:** `pip install 'google-adk[db]'` (sqlalchemy + async driver)

## Objectives

- Persist sessions across process restarts  
- Use SQLite via `sqlite+aiosqlite://...`  
- Know concurrency/locking notes for Postgres  

```python
from google.adk.sessions import DatabaseSessionService

session_service = DatabaseSessionService(
    db_url="sqlite+aiosqlite:///./.data/adk_sessions.db"
)
```

## Lab

```bash
python modules/22-db-sessions/run_db_session_demo.py
python modules/22-db-sessions/run_db_session_demo.py  # second run resumes
```

State/history should survive restarts (file under `.data/`).

### Exercises

1. Switch URL to Postgres `postgresql+asyncpg://...` (design only OK).  
2. Document backup strategy for session DBs.  

## Next

→ [Module 23 — Long-running / HITL](../23-long-running-hitl/README.md)
