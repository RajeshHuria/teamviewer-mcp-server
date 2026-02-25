# CLAUDE.md — TeamViewer MCP Server

This file gives Claude context about this project when used with Claude Code.

## Project Overview

`mcp-teamviewer` is an MCP (Model Context Protocol) server that exposes the [TeamViewer Web API v1](https://webapi.teamviewer.com/api/v1/docs/index) as callable tools for Claude.

## Project Structure

```
MCP_TV/
├── src/mcp_teamviewer/
│   ├── server.py        # All MCP tools are defined here
│   └── __init__.py
├── pyproject.toml       # Build config (hatchling), entry point: mcp-teamviewer
├── .env                 # Local only — contains TEAMVIEWER_API_TOKEN (gitignored)
├── .mcp.json            # Local only — Claude Code MCP config (gitignored)
├── .env.example         # Template for required environment variables
└── .mcp.json.example    # Template for Claude Code / Claude Desktop config
```

## Setup

```bash
# 1. Install the package
pip install -e .

# 2. Set your TeamViewer API token
cp .env.example .env
# Edit .env and add your TEAMVIEWER_API_TOKEN

# 3. Configure Claude Code
cp .mcp.json.example .mcp.json
# Edit .mcp.json if needed (e.g. use full path to venv binary)
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TEAMVIEWER_API_TOKEN` | Yes | TeamViewer Script Token from your account profile |

Get a token: Log in → Edit Profile → Apps → Create Script Token.

## Running / Testing

To verify the server starts and the token is valid:

```bash
# Quick API check (no MCP needed)
curl -H "Authorization: Bearer $TEAMVIEWER_API_TOKEN" \
     https://webapi.teamviewer.com/api/v1/ping
# Expected: {"token_valid":true}
```

To start the MCP server manually:

```bash
mcp-teamviewer
# or, if using a local venv:
.venv/bin/mcp-teamviewer
```

## Key Implementation Details

- All tools are defined in `src/mcp_teamviewer/server.py`
- API base URL: `https://webapi.teamviewer.com/api/v1`
- Auth: Bearer token via `TEAMVIEWER_API_TOKEN` env var, loaded with `python-dotenv`
- HTTP client: `httpx` (async)
- MCP framework: `mcp>=1.0.0`

## Adding New Tools

New tools follow this pattern in `server.py`:

```python
@server.tool()
async def tool_name(param: str) -> str:
    """Description shown to Claude."""
    resp = await client.get("/endpoint", params={"key": param})
    resp.raise_for_status()
    return resp.text
```

## Sensitive Files (Never Commit)

- `.env` — contains real API token
- `.mcp.json` — may contain real API token and local paths
- `.claude/` — local Claude Code settings

Both are listed in `.gitignore`.
