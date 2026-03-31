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

### General
| Tool | Description |
|------|-------------|
| `ping` | Verify API token and connectivity |

### Account
| Tool | Description |
|------|-------------|
| `get_account` | Get current account info |
| `update_account` | Update account profile |

### Devices (Computers & Contacts)
| Tool | Description |
|------|-------------|
| `list_devices` | List all devices |
| `get_device` | Get details for a specific device |
| `update_device` | Update device alias, group, or password |
| `delete_device` | Remove a device from Computers & Contacts |

### Groups
| Tool | Description |
|------|-------------|
| `list_groups` | List all groups |
| `create_group` | Create a new group |
| `update_group` | Rename a group or change its policy |
| `delete_group` | Delete a group |
| `share_group` | Share a group with other users |

### Users
| Tool | Description |
|------|-------------|
| `list_users` | List Management Console users |
| `create_user` | Create a new user |
| `get_user` | Get a specific user's details |
| `update_user` | Update user profile or permissions |

### Sessions (Service Queue)
| Tool | Description |
|------|-------------|
| `list_sessions` | List support sessions |
| `create_session` | Create a new support session |
| `get_session` | Get session details |
| `update_session` | Update session description |
| `close_session` | Close an open session (sets state to closed) |
| `delete_session` | Permanently delete a session |
| `get_session_custom_module_config` | Get custom module config ID for a session |
| `get_session_custom_modules_config_id` | Get custom modules config ID for a session (alternate endpoint) |

### Connection Reports
| Tool | Description |
|------|-------------|
| `get_connection_reports` | Query outgoing connection history with filters |
| `get_connection_report` | Get a single connection report by ID |
| `update_connection_report` | Update notes on a connection report |
| `delete_connection_report` | Delete a connection report |
| `list_connection_report_features` | List available feature filter options |
| `get_connection_report_features` | Get feature metadata for a set of report IDs |
| `get_connection_report_feature_connections` | Get reports filtered by feature name and ID |
| `get_connection_report_feature_connection` | Get a single report filtered by feature name and ID |
| `get_connection_report_ai_summary` | Get AI-generated session summary *(Tensor plan required)* |
| `get_connection_report_chat_transcript` | Get chat transcript for a session *(Tensor plan required)* |
| `get_connection_report_voice_transcript` | Get voice transcript for a session *(Tensor plan required)* |
| `get_connection_report_augmented_summary` | Get augmented AI session summary *(Tensor plan required)* |
| `list_connection_report_screenshots` | List screenshots captured during a session |
| `get_connection_report_screenshot` | Download a screenshot (returned as base64) |

### Device Reports (Incoming Sessions)
| Tool | Description |
|------|-------------|
| `get_device_reports` | Query incoming session reports with filters |
| `get_device_report_ai_summary` | Get AI-generated summary for an incoming session *(Tensor plan required)* |
| `get_device_report_chat_transcript` | Get chat transcript for an incoming session *(Tensor plan required)* |
| `list_device_report_features` | List available feature filter options for device reports |
| `get_device_report_features` | Get feature metadata for a set of device report IDs |
| `get_device_report_feature_connections` | Get device reports filtered by feature name and ID |
| `get_device_report_feature_connection` | Get a single device report filtered by feature name and ID |

### Meetings
| Tool | Description |
|------|-------------|
| `list_meetings` | List scheduled meetings |
| `create_meeting` | Schedule a new meeting |
| `get_meeting` | Get meeting details |
| `update_meeting` | Update a meeting |
| `delete_meeting` | Delete a meeting |

### Policies
| Tool | Description |
|------|-------------|
| `list_policies` | List all TeamViewer policies |
| `get_policy` | Get a specific policy |

## Example Prompts

Once connected to Claude:

- *"List all my online TeamViewer devices"*
- *"Show me connection reports from last week"*
- *"Get the AI summary for connection report abc-123"*
- *"Download the chat transcript from my last support session"*
- *"List all screenshots from session report xyz-456"*
- *"Create a support session in group g12345"*
- *"What users are in my TeamViewer company account?"*
- *"Schedule a meeting called 'Team Sync' tomorrow at 10am"*
- *"Show me incoming device session reports for this month"*

## Token Permissions

The required token permissions depend on which tools you use:

| Permission | Required for |
|------------|-------------|
| Account access | `get_account`, `update_account` |
| Computers & Contacts | `list_devices`, `get_device`, `update_device`, `delete_device` |
| Group management | `list_groups`, `create_group`, `update_group`, `delete_group`, `share_group` |
| User management | `list_users`, `create_user`, `get_user`, `update_user` |
| Session management | `list_sessions`, `create_session`, `get_session`, `update_session`, `close_session`, `delete_session`, `get_session_custom_module_config`, `get_session_custom_modules_config_id` |
| Connection reports | All `get_connection_report*`, `update_connection_report`, `delete_connection_report`, `list_connection_report*`, `get_device_report*`, `list_device_report*` |
| Meeting management | `list_meetings`, `create_meeting`, `get_meeting`, `update_meeting`, `delete_meeting` |
| **Tensor plan + AI features** | `get_connection_report_ai_summary`, `get_connection_report_chat_transcript`, `get_connection_report_voice_transcript`, `get_connection_report_augmented_summary`, `get_device_report_ai_summary`, `get_device_report_chat_transcript` |

## API Reference

Full TeamViewer Web API documentation: https://webapi.teamviewer.com/api/v1/docs/index

## License

MIT — see [LICENSE](LICENSE)

## Credits

- **Author**: Rajesh Huria
- **MCP framework**: [Model Context Protocol Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- **TeamViewer Web API**: [TeamViewer API documentation](https://webapi.teamviewer.com/api/v1/docs/index)
