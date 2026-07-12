#!/usr/bin/env python3
"""Dry-check course agents import against installed google-adk.

Usage:
  source .venv/bin/activate
  python scripts/verify_course_imports.py
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "modules" / "09-capstone"))

PASS = 0
FAIL = 0


def ok(msg: str) -> None:
    global PASS
    PASS += 1
    print(f"  OK  {msg}")


def bad(msg: str, exc: BaseException | None = None) -> None:
    global FAIL
    FAIL += 1
    detail = f" ({type(exc).__name__}: {exc})" if exc else ""
    print(f"  FAIL {msg}{detail}")


def load_agent(path: Path, label: str):
    spec = importlib.util.spec_from_file_location(label, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[label] = mod
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    print("google-adk version:", end=" ")
    try:
        import google.adk as adk

        print(getattr(adk, "__version__", "installed (no __version__)"))
        try:
            import importlib.metadata as md

            print("  dist:", md.version("google-adk"))
        except Exception:
            pass
    except Exception as exc:
        bad("import google.adk", exc)
        return 1

    agents = [
        ROOT / "modules/00-setup/setup_probe/agent.py",
        ROOT / "modules/02-first-agent/time_agent/agent.py",
        ROOT / "modules/03-tools/weather_sentiment_agent/agent.py",
        ROOT / "modules/04-sessions-state/preference_agent/agent.py",
        ROOT / "modules/05-multi-agent/travel_team/agent.py",
        ROOT / "modules/05-multi-agent/sequential_research/agent.py",
        ROOT / "modules/05-multi-agent/parallel_research/agent.py",
        ROOT / "modules/05-multi-agent/loop_refine/agent.py",
        ROOT / "modules/05-multi-agent/agent_as_tool/agent.py",
        ROOT / "modules/06-advanced/structured_capital_agent/agent.py",
        ROOT / "modules/06-advanced/planning_agent/agent.py",
        ROOT / "modules/08-deployment/sample_agent/agent.py",
        ROOT / "modules/12-callbacks-plugins/guardrail_agent/agent.py",
        ROOT / "modules/13-mcp-integrations/mcp_filesystem_agent/agent.py",
        ROOT / "modules/17-vertex-gcp/samples/vertex_hello/agent.py",
    ]

    print("\nAgent packages:")
    for path in agents:
        label = path.parent.name
        try:
            mod = load_agent(path, f"verify_{label}")
            name = getattr(mod.root_agent, "name", type(mod.root_agent).__name__)
            ok(f"{path.relative_to(ROOT)} → root={name}")
        except Exception as exc:
            bad(str(path.relative_to(ROOT)), exc)

    print("\nCapstone package + plugin:")
    try:
        from research_ops_assistant.agent import root_agent
        from plugins.research_ops_plugin import ResearchOpsPlugin

        ok(f"research_ops_assistant root={root_agent.name}")
        ok(f"subs={[a.name for a in root_agent.sub_agents]}")
        p = ResearchOpsPlugin()
        ok(f"plugin name={p.name}")
    except Exception as exc:
        bad("capstone imports", exc)

    print("\nMCP readiness:")
    try:
        mod = load_agent(
            ROOT / "modules/13-mcp-integrations/mcp_filesystem_agent/agent.py",
            "verify_mcp_again",
        )
        ok(f"mcp_ready={mod._MCP_AVAILABLE} tools={len(mod.root_agent.tools)}")
        if mod._MCP_AVAILABLE:
            import asyncio

            async def list_tools():
                for t in mod.root_agent.tools:
                    if type(t).__name__ == "McpToolset":
                        tools = await t.get_tools()
                        names = [x.name for x in tools]
                        ok(f"mcp discovered: {names}")
                        if hasattr(t, "close"):
                            await t.close()

            asyncio.run(list_tools())
    except Exception as exc:
        bad("mcp probe", exc)

    print("\nRunner wiring (no model call):")
    try:
        from google.adk.memory import InMemoryMemoryService
        from google.adk.runners import Runner
        from google.adk.sessions import InMemorySessionService
        from plugins.research_ops_plugin import ResearchOpsPlugin
        from research_ops_assistant.agent import root_agent

        r = Runner(
            agent=root_agent,
            app_name="verify_app",
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
            plugins=[ResearchOpsPlugin()],
        )
        ok(f"Runner(plugins+memory) constructed: {type(r).__name__}")
    except Exception as exc:
        bad("Runner construction", exc)

    print("\nGraph workflow import:")
    try:
        sys.path.insert(0, str(ROOT / "modules" / "18-graphs"))
        from loan_graph.workflow import loan_workflow

        ok(f"loan_workflow name={loan_workflow.name}")
    except Exception as exc:
        bad("loan_workflow import", exc)

    print(f"\nSummary: {PASS} passed, {FAIL} failed")
    return 1 if FAIL else 0


if __name__ == "__main__":
    raise SystemExit(main())
