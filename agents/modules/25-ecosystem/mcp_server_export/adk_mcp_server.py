#!/usr/bin/env python3
"""Minimal pattern: expose a simple ADK-style tool function via MCP stdio.

This is a teaching skeleton. For production, use ADK conversion utils:
  google.adk.tools.mcp_tool.conversion_utils.adk_to_mcp_tool_type
and the official "Build an MCP server with ADK tools" guide on adk.dev.
"""

from __future__ import annotations

import asyncio
import json


def echo_tool(message: str) -> dict:
    """Echo a message (demo tool to expose)."""
    return {"status": "success", "echo": message}


async def main() -> None:
    # Real MCP servers use mcp.server; here we only demonstrate the tool contract.
    print(
        json.dumps(
            {
                "info": "Run this under a full MCP host implementation",
                "tools": [
                    {
                        "name": "echo_tool",
                        "description": echo_tool.__doc__,
                        "example": echo_tool("hello"),
                    }
                ],
                "next_step": "See adk.dev MCP tools — expose ADK tools section",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    asyncio.run(main())
