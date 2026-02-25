# TeamViewer MCP Server

An MCP (Model Context Protocol) server that exposes the [TeamViewer Web API v1](https://webapi.teamviewer.com/api/v1/docs/index) as tools callable by Claude and other MCP clients.

## Prerequisites

- Python 3.10+
- A TeamViewer account with a **Business, Premium, Corporate, or Tensor** plan
- A **Script Token** (or OAuth 2.0 access token)

### Creating a Script Token

1. Log in to [login.teamviewer.com](https://login.teamviewer.com)
2. Click your account name → **Edit Profile**
3. Go to **Apps** → **Create Script Token**
4. Select the required permissions and save the token

## Installation

```bash
cd MCP_TV
pip install -e .
```

## Configuration

Set the token as an environment variable:

```bash
export TEAMVIEWER_API_TOKEN="your_token_here"
```

## Usage with Claude Desktop

Add the following to your Claude Desktop config file:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "teamviewer": {
      "command": "mcp-teamviewer",
      "env": {
        "TEAMVIEWER_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

If `mcp-teamviewer` is not on your PATH (e.g. installed in a local venv), use the full path to the binary:

```json
{
  "mcpServers": {
    "teamviewer": {
      "command": "/path/to/.venv/bin/mcp-teamviewer",
      "env": {
        "TEAMVIEWER_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

## Available Tools

| Tool | Description |
|------|-------------|
| `ping` | Verify API token and connectivity |
| `get_account` | Get current account info |
| `update_account` | Update account profile |
| `list_devices` | List all devices (Computers & Contacts) |
| `get_device` | Get details for a specific device |
| `update_device` | Update device alias, group, password |
| `delete_device` | Remove a device from Computers & Contacts |
| `list_groups` | List all groups |
| `create_group` | Create a new group |
| `update_group` | Rename a group or change its policy |
| `delete_group` | Delete a group |
| `share_group` | Share a group with other users |
| `list_users` | List Management Console users |
| `create_user` | Create a new user |
| `get_user` | Get a specific user's details |
| `update_user` | Update user profile or permissions |
| `list_sessions` | List support sessions |
| `create_session` | Create a new support session |
| `get_session` | Get session details |
| `update_session` | Update session description |
| `close_session` | Close an open session |
| `get_connection_reports` | Query connection history with filters |
| `list_meetings` | List scheduled meetings |
| `create_meeting` | Schedule a new meeting |
| `get_meeting` | Get meeting details |
| `update_meeting` | Update a meeting |
| `delete_meeting` | Delete a meeting |
| `list_policies` | List all TeamViewer policies |
| `get_policy` | Get a specific policy |

## Example Prompts

Once connected to Claude:

- *"List all my online TeamViewer devices"*
- *"Show me connection reports from last week"*
- *"Create a support session in group g12345"*
- *"What users are in my TeamViewer company account?"*
- *"Schedule a meeting called 'Team Sync' tomorrow at 10am"*

## Token Permissions

The required token permissions depend on which tools you use:

| Permission | Required for |
|------------|-------------|
| Account access | `get_account`, `update_account` |
| Computers & Contacts | `list_devices`, `get_device`, `update_device`, `delete_device` |
| Group management | `list_groups`, `create_group`, `update_group`, `delete_group`, `share_group` |
| User management | `list_users`, `create_user`, `get_user`, `update_user` |
| Session management | `list_sessions`, `create_session`, `get_session`, `update_session`, `close_session` |
| Connection reports | `get_connection_reports` |
| Meeting management | `list_meetings`, `create_meeting`, `get_meeting`, `update_meeting`, `delete_meeting` |

## API Reference

Full TeamViewer Web API documentation: https://webapi.teamviewer.com/api/v1/docs/index

## License

MIT — see [LICENSE](LICENSE)

## Credits

- **Author**: Rajesh Huria
- **MCP framework**: [Model Context Protocol Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- **TeamViewer Web API**: [TeamViewer API documentation](https://webapi.teamviewer.com/api/v1/docs/index)
- Built with [Claude](https://claude.ai) and [Claude Code](https://claude.ai/claude-code)
