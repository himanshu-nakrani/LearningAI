#!/usr/bin/env python3
"""Run the Module 18 loan decision graph.

Usage:
  python modules/18-graphs/run_loan_graph.py
  python modules/18-graphs/run_loan_graph.py --text "I need 50000"
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from loan_graph.workflow import loan_workflow


async def run_once(text: str) -> dict:
    svc = InMemorySessionService()
    await svc.create_session(app_name="loan", user_id="u1", session_id="s1", state={})
    runner = Runner(node=loan_workflow, app_name="loan", session_service=svc)
    msg = Content(role="user", parts=[Part(text=text)])
    print(f"USER: {text}")
    async for event in runner.run_async(
        user_id="u1", session_id="s1", new_message=msg
    ):
        out = getattr(event, "output", None)
        path = None
        if getattr(event, "node_info", None):
            path = event.node_info.path
        if out is not None:
            print(f"  node {path}: {out}")
    sess = await svc.get_session(app_name="loan", user_id="u1", session_id="s1")
    state = dict(sess.state) if sess else {}
    print("FINAL STATE:", state)
    return state


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--text", default="Please approve a loan of 5000 dollars")
    args = p.parse_args()
    asyncio.run(run_once(args.text))


if __name__ == "__main__":
    main()
