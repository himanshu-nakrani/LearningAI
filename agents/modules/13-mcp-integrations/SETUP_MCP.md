# MCP Filesystem Lab — Setup Guide

## Verified environment

Course labs were dry-checked against **google-adk 2.4.0** + **mcp 1.28.x** with Node/npx available. Run:

```bash
source .venv/bin/activate
python scripts/verify_course_imports.py
```

---

## 1. Install Node.js (provides `npx`)

**macOS (Homebrew):**

```bash
brew install node
node -v && npx -v
```

**Other:** https://nodejs.org/ (LTS)

## 2. Python packages

```bash
source .venv/bin/activate
pip install -U google-adk mcp
```

## 3. Verify sandbox

```bash
ls modules/13-mcp-integrations/mcp_filesystem_agent/sandbox
```

## 4. Run the agent

```bash
export GOOGLE_API_KEY=...   # or use .env
adk run modules/13-mcp-integrations/mcp_filesystem_agent
```

First run may download `@modelcontextprotocol/server-filesystem` via `npx -y` (needs network).

## 5. Try prompts

```
Is MCP ready?
List the sandbox files.
Read hello.txt
Summarize the refund policy.
```

## 6. Dev UI

```bash
adk web modules/13-mcp-integrations --port 8000
```

Open Trace to see MCP tool calls.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `npx` not found | Install Node.js |
| MCP tools missing | `pip install mcp`; check `mcp_status` tool output |
| Permission errors | Agent only accesses `sandbox/`; don't point at `/` |
| Windows `_make_subprocess_transport` | Try `adk web --no-reload` |
| Slow first start | npx downloading package; wait or preinstall |

## Security notes (production)

- Use **tool_filter** allowlists (this lab is read-only)
- Never mount home directory or secrets
- Prefer remote MCP with auth over shelling out in multi-tenant hosts
- For deploy, define McpToolset **synchronously** and bake Node into the image
