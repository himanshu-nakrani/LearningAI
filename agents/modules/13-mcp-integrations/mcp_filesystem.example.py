"""EXAMPLE ONLY — enable when Node.js/npx is installed.

Copy to agent.py package and point FOLDER at a safe sandbox directory.
"""

from __future__ import annotations

import os

# Uncomment when ready:
# from google.adk.agents import LlmAgent
# from google.adk.tools.mcp_tool import McpToolset
# from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
# from mcp import StdioServerParameters

FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "sandbox"))

# root_agent = LlmAgent(
#     model="gemini-flash-latest",
#     name="mcp_filesystem_example",
#     instruction="List and read files only within the allowed sandbox.",
#     tools=[
#         McpToolset(
#             connection_params=StdioConnectionParams(
#                 server_params=StdioServerParameters(
#                     command="npx",
#                     args=["-y", "@modelcontextprotocol/server-filesystem", FOLDER],
#                 ),
#                 timeout=30,
#             ),
#             tool_filter=[
#                 "list_directory",
#                 "read_file",
#                 "directory_tree",
#             ],
#         )
#     ],
# )

print("This is an example scaffold. See Module 13 README to enable MCP filesystem.")
