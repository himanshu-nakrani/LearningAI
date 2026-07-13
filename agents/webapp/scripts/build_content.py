#!/usr/bin/env python3
"""Build course-data.json from agents/ modules for the learning webapp."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # agents/
OUT = Path(__file__).resolve().parents[1] / "public" / "course-data.json"

# (id, title, track, level, hours, summary, extra_docs[])
MODULE_META: list[dict] = [
    {"id": "00-setup", "title": "Environment & ADK Setup", "track": "core", "level": "Beginner", "hours": "1–2h", "summary": "Install ADK, API keys, adk run/web."},
    {"id": "01-foundations", "title": "Agentic AI Foundations", "track": "core", "level": "Beginner", "hours": "2–3h", "summary": "Agents vs chatbots, loops, trajectories."},
    {"id": "02-first-agent", "title": "Your First ADK Agent", "track": "core", "level": "Beginner", "hours": "2–3h", "summary": "LlmAgent, tools, Dev UI traces."},
    {"id": "03-tools", "title": "Tools Deep Dive", "track": "core", "level": "Beginner", "hours": "3–4h", "summary": "Function tools, contracts, ToolContext."},
    {"id": "04-sessions-state", "title": "Sessions, State & Memory Intro", "track": "core", "level": "Intermediate", "hours": "3–4h", "summary": "Session services, state prefixes."},
    {"id": "05-multi-agent", "title": "Multi-Agent Workflows", "track": "core", "level": "Intermediate", "hours": "4–5h", "summary": "Hierarchy, Sequential, Parallel, Loop, AgentTool."},
    {"id": "06-advanced", "title": "Advanced LlmAgent Patterns", "track": "core", "level": "Advanced", "hours": "3–4h", "summary": "Schemas, planners, generation config."},
    {"id": "07-evaluation", "title": "Evaluation & Testing", "track": "core", "level": "Intermediate", "hours": "2–3h", "summary": "Trajectory metrics, eval CLI, conformance."},
    {"id": "08-deployment", "title": "Deployment & Production", "track": "core", "level": "Advanced", "hours": "2–3h", "summary": "Cloud Run, Agent Runtime, checklists."},
    {"id": "09-capstone", "title": "Capstone: Research Ops Assistant", "track": "core", "level": "Capstone", "hours": "8–12h", "summary": "Multi-agent + memory + plugin + eval."},
    {"id": "10-memory", "title": "Long-Term Memory", "track": "deep", "level": "Intermediate", "hours": "3–4h", "summary": "MemoryService, load_memory, Memory Bank."},
    {"id": "11-artifacts", "title": "Artifacts", "track": "deep", "level": "Intermediate", "hours": "2–3h", "summary": "Versioned binary blobs and namespaces."},
    {"id": "12-callbacks-plugins", "title": "Callbacks & Plugins", "track": "deep", "level": "Advanced", "hours": "3–4h", "summary": "Lifecycle hooks and Runner plugins."},
    {"id": "13-mcp-integrations", "title": "MCP & Integrations", "track": "deep", "level": "Advanced", "hours": "3–4h", "summary": "McpToolset filesystem lab and catalog.", "docs": ["SETUP_MCP.md"]},
    {"id": "14-graphs-workflows", "title": "Workflow Concepts", "track": "deep", "level": "Advanced", "hours": "2–3h", "summary": "Templates vs graphs vs dynamic."},
    {"id": "15-streaming-live", "title": "Streaming Concepts", "track": "deep", "level": "Advanced", "hours": "2h", "summary": "Live toolkit architecture overview."},
    {"id": "16-models-config-runtime", "title": "Models, Config & Runtime", "track": "deep", "level": "Advanced", "hours": "3–4h", "summary": "Connectors, Runner, Events, context."},
    {"id": "17-vertex-gcp", "title": "Vertex / GCP Pack", "track": "deep", "level": "Advanced", "hours": "4–6h", "summary": "Vertex sessions, Memory Bank, deploy scripts."},
    {"id": "18-graphs", "title": "Graph Workflows (ADK 2.x)", "track": "production", "level": "Advanced", "hours": "3–4h", "summary": "Workflow, FunctionNode, routes."},
    {"id": "19-auth", "title": "Auth & Credentials", "track": "production", "level": "Advanced", "hours": "2–3h", "summary": "Credential services and tool auth."},
    {"id": "20-telemetry", "title": "Telemetry & Observability", "track": "production", "level": "Advanced", "hours": "2–3h", "summary": "OpenTelemetry spans and metrics."},
    {"id": "21-code-executors", "title": "Code Executors", "track": "production", "level": "Intermediate", "hours": "2h", "summary": "BuiltInCodeExecutor calculator."},
    {"id": "22-db-sessions", "title": "Database Sessions", "track": "production", "level": "Intermediate", "hours": "1–2h", "summary": "SQLite DatabaseSessionService."},
    {"id": "23-long-running-hitl", "title": "Long-Running & HITL", "track": "production", "level": "Advanced", "hours": "2–3h", "summary": "Approval gates and long jobs."},
    {"id": "24-skills", "title": "Agent Skills", "track": "production", "level": "Intermediate", "hours": "2h", "summary": "Load skills from SKILL.md packages."},
    {"id": "25-ecosystem", "title": "Ecosystem Survey", "track": "production", "level": "Advanced", "hours": "3–4h", "summary": "A2A, multi-model, MCP export, optimizers."},
    {"id": "26-live-streaming", "title": "Live & SSE Streaming", "track": "production", "level": "Advanced", "hours": "2–3h", "summary": "LiveRequestQueue, SSE, run_live."},
    {"id": "27-oauth-flow", "title": "OAuth2 Credential Flow", "track": "production", "level": "Advanced", "hours": "2–3h", "summary": "AuthConfig simulation and local OAuth server."},
    {"id": "28-a2a-demo", "title": "A2A Two-Process Demo", "track": "production", "level": "Advanced", "hours": "2–3h", "summary": "to_a2a server + RemoteA2aAgent client."},
]

RESOURCES = [
    {"id": "glossary", "title": "Glossary", "path": "resources/glossary.md", "kind": "reference"},
    {"id": "cheatsheet", "title": "ADK Cheatsheet", "path": "resources/cheatsheet.md", "kind": "reference"},
    {"id": "further-reading", "title": "Further Reading", "path": "resources/further-reading.md", "kind": "reference"},
    {"id": "coverage", "title": "ADK Coverage Matrix", "path": "ADK_COVERAGE.md", "kind": "reference"},
    {"id": "curriculum", "title": "Curriculum", "path": "curriculum.md", "kind": "reference"},
    {"id": "progress", "title": "Progress Tracker", "path": "PROGRESS.md", "kind": "reference"},
]

TRACKS = [
    {
        "id": "core",
        "title": "Core",
        "blurb": "From setup to capstone multi-agent systems",
        "color": "#2dd4bf",
    },
    {
        "id": "deep",
        "title": "Deep ADK",
        "blurb": "Memory, artifacts, plugins, MCP, Vertex",
        "color": "#a78bfa",
    },
    {
        "id": "production",
        "title": "Production ADK 2.x",
        "blurb": "Graphs, auth, telemetry, live, OAuth, A2A",
        "color": "#fbbf24",
    },
]


def read_md(path: Path) -> str:
    if not path.is_file():
        return f"_Missing file: `{path.name}`_\n"
    return path.read_text(encoding="utf-8")


def extract_title(md: str, fallback: str) -> str:
    for line in md.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def main() -> None:
    modules_out = []
    for i, meta in enumerate(MODULE_META):
        mod_dir = ROOT / "modules" / meta["id"]
        readme = mod_dir / "README.md"
        body = read_md(readme)
        docs = []
        for extra in meta.get("docs", []):
            p = mod_dir / extra
            docs.append(
                {
                    "id": f"{meta['id']}:{extra}",
                    "title": extra,
                    "markdown": read_md(p),
                }
            )
        modules_out.append(
            {
                **{k: v for k, v in meta.items() if k != "docs"},
                "order": i,
                "slug": meta["id"],
                "title": extract_title(body, meta["title"]),
                "markdown": body,
                "extra_docs": docs,
                "path": f"modules/{meta['id']}/README.md",
            }
        )

    resources_out = []
    for r in RESOURCES:
        p = ROOT / r["path"]
        md = read_md(p)
        resources_out.append(
            {
                **r,
                "title": extract_title(md, r["title"]),
                "markdown": md,
            }
        )

    course = {
        "title": "Agentic AI with Google ADK",
        "subtitle": "End-to-end course — agents, multi-agent systems, production ADK 2.x",
        "version": "2.4.0-compatible",
        "moduleCount": len(modules_out),
        "tracks": TRACKS,
        "modules": modules_out,
        "resources": resources_out,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(course, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT} ({len(modules_out)} modules, {len(resources_out)} resources)")


if __name__ == "__main__":
    main()
