"""Module 13 — Fully runnable MCP filesystem agent (stdio + npx).

Prerequisites:
  - Node.js + npx on PATH
  - pip install google-adk mcp  (mcp usually pulled by google-adk extras)

Run:
  # from course root
  adk run modules/13-mcp-integrations/mcp_filesystem_agent
  adk web modules/13-mcp-integrations --port 8000

Security: tools are filtered to read-only operations on ./sandbox only.
"""

from __future__ import annotations

import os
import shutil

from google.adk.agents.llm_agent import LlmAgent

# Absolute path to the sandbox shipped with this package.
_SANDBOX = os.path.abspath(os.path.join(os.path.dirname(__file__), "sandbox"))
os.makedirs(_SANDBOX, exist_ok=True)

_NPX = shutil.which("npx")
_MCP_AVAILABLE = False
_tools: list = []

if _NPX:
    try:
        from google.adk.tools.mcp_tool import McpToolset
        from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
        from mcp import StdioServerParameters

        # Read-only filter — never expose write/delete in the course lab.
        _READ_ONLY = [
            "list_directory",
            "read_file",
            "read_multiple_files",
            "directory_tree",
            "search_files",
            "get_file_info",
            "list_allowed_directories",
        ]

        _tools = [
            McpToolset(
                connection_params=StdioConnectionParams(
                    server_params=StdioServerParameters(
                        command=_NPX,
                        args=[
                            "-y",
                            "@modelcontextprotocol/server-filesystem",
                            _SANDBOX,
                        ],
                    ),
                    # First npx download can exceed the 5s default.
                    timeout=120.0,
                ),
                tool_filter=_READ_ONLY,
            )
        ]
        _MCP_AVAILABLE = True
    except ImportError:
        _MCP_AVAILABLE = False


def mcp_status() -> dict:
    """Reports whether MCP filesystem tools are available in this environment.

    Returns:
        Status dict with sandbox path and readiness flags.
    """
    return {
        "status": "success",
        "mcp_ready": _MCP_AVAILABLE,
        "npx_found": bool(_NPX),
        "sandbox_path": _SANDBOX,
        "hint": (
            "MCP tools loaded."
            if _MCP_AVAILABLE
            else "Install Node.js (npx) and `pip install mcp google-adk`, then restart."
        ),
    }


root_agent = LlmAgent(
    model="gemini-flash-latest",
    name="mcp_filesystem_agent",
    description=(
        "Lists and reads files in the course MCP sandbox via Model Context Protocol."
    ),
    instruction=f"""
You help users explore a **read-only sandbox directory** for the ADK MCP lab.

Sandbox absolute path: {_SANDBOX}

Rules:
1. First, if unsure about environment, call mcp_status.
2. When MCP tools are available, use them to list directories and read files
   (list_directory, read_file, directory_tree, etc.).
3. Only discuss files under the sandbox. Never invent file contents —
   always read via tools.
4. If MCP is not ready, explain how to install Node.js/npx and retry.
5. Keep answers concise; quote short file snippets when relevant.
""".strip(),
    tools=[mcp_status, *_tools],
)
