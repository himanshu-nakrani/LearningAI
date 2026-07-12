#!/usr/bin/env python3
"""Persist a session with DatabaseSessionService (SQLite)."""

from __future__ import annotations

import asyncio
from pathlib import Path

from google.adk.sessions import DatabaseSessionService

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / ".data" / "adk_sessions.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
DB_URL = f"sqlite+aiosqlite:///{DB_PATH}"

APP = "db_session_demo"
USER = "db_user"
SID = "persistent_session_1"


async def main() -> None:
    svc = DatabaseSessionService(db_url=DB_URL)
    existing = await svc.get_session(app_name=APP, user_id=USER, session_id=SID)
    if existing is None:
        sess = await svc.create_session(
            app_name=APP,
            user_id=USER,
            session_id=SID,
            state={"visits": 1, "note": "first create"},
        )
        print("CREATED", sess.id, dict(sess.state))
    else:
        visits = int(existing.state.get("visits", 0)) + 1
        # Append via state update pattern: create event or re-save depending on API
        # For demo, delete+recreate is wrong; use append_event in full apps.
        # Here we show get after prior run:
        print("LOADED existing", existing.id, dict(existing.state), "events", len(existing.events))
        print(
            f"(visits counter was {existing.state.get('visits')}; "
            "full apps update state via tool_context / events)"
        )
        # Update state by creating a new session is not allowed; demonstrate persistence only.
        print(f"DB file: {DB_PATH}")
        return

    again = await svc.get_session(app_name=APP, user_id=USER, session_id=SID)
    print("RELOADED", again.id if again else None, dict(again.state) if again else None)
    print(f"DB file: {DB_PATH}")
    print("Re-run this script to confirm the session still loads after process exit.")


if __name__ == "__main__":
    asyncio.run(main())
