"""TeamViewer MCP Server

Exposes TeamViewer Web API (https://webapi.teamviewer.com/api/v1) as MCP tools.
Authentication: Bearer token (Script Token or OAuth 2.0 access token).
"""

import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

# Load .env from the project root (two levels up from this file)
load_dotenv(Path(__file__).parent.parent.parent / ".env")

import httpx
import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions

BASE_URL = "https://webapi.teamviewer.com/api/v1"

server = Server("mcp-teamviewer")


def get_token() -> str:
    token = os.environ.get("TEAMVIEWER_API_TOKEN", "")
    if not token:
        raise ValueError(
            "TEAMVIEWER_API_TOKEN environment variable is not set. "
            "Create a Script Token in TeamViewer Management Console under "
            "Edit Profile → Apps → Create Script Token."
        )
    return token


def build_headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {get_token()}",
        "Content-Type": "application/json",
    }


async def tv_get(path: str, params: dict | None = None) -> Any:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}{path}",
            headers=build_headers(),
            params=params,
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()


async def tv_post(path: str, body: dict | None = None) -> Any:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}{path}",
            headers=build_headers(),
            json=body or {},
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()


async def tv_put(path: str, body: dict | None = None) -> Any:
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{BASE_URL}{path}",
            headers=build_headers(),
            json=body or {},
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()


async def tv_delete(path: str) -> Any:
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{BASE_URL}{path}",
            headers=build_headers(),
            timeout=30.0,
        )
        response.raise_for_status()
        if response.status_code == 204:
            return {"success": True}
        return response.json()


def ok(data: Any) -> list[types.TextContent]:
    return [types.TextContent(type="text", text=json.dumps(data, indent=2))]


# ---------------------------------------------------------------------------
# Tool definitions
# ---------------------------------------------------------------------------

TOOLS = [
    # ── Account ─────────────────────────────────────────────────────────────
    types.Tool(
        name="get_account",
        description="Get the current TeamViewer account information (email, name, company, etc.).",
        inputSchema={"type": "object", "properties": {}, "required": []},
    ),
    types.Tool(
        name="update_account",
        description="Update the current TeamViewer account's profile information.",
        inputSchema={
            "type": "object",
            "properties": {
                "email": {"type": "string", "description": "New email address"},
                "name": {"type": "string", "description": "Display name"},
                "company": {"type": "string", "description": "Company name"},
                "password": {"type": "string", "description": "New password"},
                "old_password": {"type": "string", "description": "Current password (required when changing password)"},
            },
            "required": [],
        },
    ),
    # ── Devices / Computers & Contacts ───────────────────────────────────────
    types.Tool(
        name="list_devices",
        description=(
            "List all devices (Computers & Contacts) in the account. "
            "Optionally filter by group ID, online status, or name."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "groupid": {"type": "string", "description": "Filter by group ID"},
                "online_state": {
                    "type": "string",
                    "enum": ["Online", "Busy", "Away", "Offline"],
                    "description": "Filter by online status",
                },
                "full_list": {"type": "boolean", "description": "Return full device details"},
            },
            "required": [],
        },
    ),
    types.Tool(
        name="get_device",
        description="Get details of a specific device by its device ID.",
        inputSchema={
            "type": "object",
            "properties": {
                "device_id": {"type": "string", "description": "The device ID (e.g. d123456789)"},
            },
            "required": ["device_id"],
        },
    ),
    types.Tool(
        name="update_device",
        description="Update a device's alias, description, password, or group assignment.",
        inputSchema={
            "type": "object",
            "properties": {
                "device_id": {"type": "string", "description": "Device ID"},
                "alias": {"type": "string", "description": "New alias/display name"},
                "description": {"type": "string", "description": "Description"},
                "password": {"type": "string", "description": "Remote control password"},
                "groupid": {"type": "string", "description": "Target group ID to move the device"},
            },
            "required": ["device_id"],
        },
    ),
    types.Tool(
        name="delete_device",
        description="Remove a device from the Computers & Contacts list.",
        inputSchema={
            "type": "object",
            "properties": {
                "device_id": {"type": "string", "description": "Device ID to remove"},
            },
            "required": ["device_id"],
        },
    ),
    # ── Groups ───────────────────────────────────────────────────────────────
    types.Tool(
        name="list_groups",
        description="List all groups in the account. Optionally filter by name.",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Filter groups by name (partial match)"},
            },
            "required": [],
        },
    ),
    types.Tool(
        name="create_group",
        description="Create a new group in Computers & Contacts.",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Group name"},
                "policy_id": {"type": "string", "description": "Policy ID to assign to the group"},
            },
            "required": ["name"],
        },
    ),
    types.Tool(
        name="update_group",
        description="Rename a group or change its assigned policy.",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {"type": "string", "description": "Group ID"},
                "name": {"type": "string", "description": "New group name"},
                "policy_id": {"type": "string", "description": "New policy ID"},
            },
            "required": ["group_id"],
        },
    ),
    types.Tool(
        name="delete_group",
        description="Delete a group from Computers & Contacts.",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {"type": "string", "description": "Group ID to delete"},
            },
            "required": ["group_id"],
        },
    ),
    types.Tool(
        name="share_group",
        description="Share a group with other TeamViewer users.",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {"type": "string", "description": "Group ID to share"},
                "users": {
                    "type": "array",
                    "description": "List of user objects to share with",
                    "items": {
                        "type": "object",
                        "properties": {
                            "userid": {"type": "string"},
                            "permissions": {"type": "string", "enum": ["read", "readwrite", "full"]},
                        },
                        "required": ["userid", "permissions"],
                    },
                },
            },
            "required": ["group_id", "users"],
        },
    ),
    # ── Users (Management Console) ──────────────────────────────────────────
    types.Tool(
        name="list_users",
        description="List all users in the TeamViewer Management Console company account.",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Filter by name"},
                "email": {"type": "string", "description": "Filter by email"},
                "permissions": {"type": "string", "description": "Filter by permission level"},
                "full_list": {"type": "boolean", "description": "Return full user details"},
            },
            "required": [],
        },
    ),
    types.Tool(
        name="create_user",
        description="Create a new user in the TeamViewer Management Console.",
        inputSchema={
            "type": "object",
            "properties": {
                "email": {"type": "string", "description": "User email address"},
                "name": {"type": "string", "description": "User display name"},
                "password": {"type": "string", "description": "Initial password"},
                "permissions": {
                    "type": "string",
                    "description": "Permission level (e.g. Administrator, User)",
                },
                "language": {"type": "string", "description": "Language code (e.g. en, de)"},
            },
            "required": ["email", "name", "password"],
        },
    ),
    types.Tool(
        name="get_user",
        description="Get details of a specific user by user ID.",
        inputSchema={
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "User ID (e.g. u123456)"},
            },
            "required": ["user_id"],
        },
    ),
    types.Tool(
        name="update_user",
        description="Update a user's profile or permissions.",
        inputSchema={
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "User ID"},
                "email": {"type": "string", "description": "New email"},
                "name": {"type": "string", "description": "New display name"},
                "permissions": {"type": "string", "description": "New permission level"},
                "active": {"type": "boolean", "description": "Whether the account is active"},
            },
            "required": ["user_id"],
        },
    ),
    # ── Sessions (Service Queue) ─────────────────────────────────────────────
    types.Tool(
        name="list_sessions",
        description="List support sessions (service queue) optionally filtered by group or state.",
        inputSchema={
            "type": "object",
            "properties": {
                "groupid": {"type": "string", "description": "Filter by group ID"},
                "state": {
                    "type": "string",
                    "enum": ["open", "closed"],
                    "description": "Session state filter",
                },
            },
            "required": [],
        },
    ),
    types.Tool(
        name="create_session",
        description="Create a new support session (service case).",
        inputSchema={
            "type": "object",
            "properties": {
                "groupid": {"type": "string", "description": "Group ID for the session"},
                "description": {"type": "string", "description": "Session description"},
                "custom_internal_id": {"type": "string", "description": "Custom reference ID"},
            },
            "required": ["groupid"],
        },
    ),
    types.Tool(
        name="get_session",
        description="Get details of a specific support session by session code.",
        inputSchema={
            "type": "object",
            "properties": {
                "session_code": {"type": "string", "description": "Session code (e.g. s00-000-000)"},
            },
            "required": ["session_code"],
        },
    ),
    types.Tool(
        name="update_session",
        description="Update a support session's description or custom internal ID.",
        inputSchema={
            "type": "object",
            "properties": {
                "session_code": {"type": "string", "description": "Session code"},
                "description": {"type": "string", "description": "New description"},
                "custom_internal_id": {"type": "string", "description": "New custom reference ID"},
            },
            "required": ["session_code"],
        },
    ),
    types.Tool(
        name="close_session",
        description="Close an open support session.",
        inputSchema={
            "type": "object",
            "properties": {
                "session_code": {"type": "string", "description": "Session code to close"},
            },
            "required": ["session_code"],
        },
    ),
    # ── Connection Reports ──────────────────────────────────────────────────
    types.Tool(
        name="get_connection_reports",
        description=(
            "Retrieve connection reports. Filter by date range, device ID, user, or session. "
            "Returns details about all remote connections made."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "from_date": {
                    "type": "string",
                    "description": "Start date in ISO 8601 format (e.g. 2024-01-01T00:00:00)",
                },
                "to_date": {
                    "type": "string",
                    "description": "End date in ISO 8601 format",
                },
                "device_id": {"type": "string", "description": "Filter by device ID"},
                "user_id": {"type": "string", "description": "Filter by user ID"},
                "session_code": {"type": "string", "description": "Filter by session code"},
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of records to return",
                    "default": 100,
                },
                "offset": {
                    "type": "integer",
                    "description": "Pagination offset",
                    "default": 0,
                },
            },
            "required": [],
        },
    ),
    # ── Meetings ────────────────────────────────────────────────────────────
    types.Tool(
        name="list_meetings",
        description="List all scheduled meetings in the account.",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    ),
    types.Tool(
        name="create_meeting",
        description="Schedule a new TeamViewer meeting.",
        inputSchema={
            "type": "object",
            "properties": {
                "subject": {"type": "string", "description": "Meeting subject/title"},
                "start": {
                    "type": "string",
                    "description": "Start time in ISO 8601 format (e.g. 2024-06-01T10:00:00)",
                },
                "end": {
                    "type": "string",
                    "description": "End time in ISO 8601 format",
                },
                "password": {"type": "string", "description": "Optional meeting password"},
            },
            "required": ["subject", "start", "end"],
        },
    ),
    types.Tool(
        name="get_meeting",
        description="Get details of a specific meeting by meeting ID.",
        inputSchema={
            "type": "object",
            "properties": {
                "meeting_id": {"type": "string", "description": "Meeting ID"},
            },
            "required": ["meeting_id"],
        },
    ),
    types.Tool(
        name="update_meeting",
        description="Update an existing meeting's subject, time, or password.",
        inputSchema={
            "type": "object",
            "properties": {
                "meeting_id": {"type": "string", "description": "Meeting ID"},
                "subject": {"type": "string", "description": "New subject"},
                "start": {"type": "string", "description": "New start time (ISO 8601)"},
                "end": {"type": "string", "description": "New end time (ISO 8601)"},
                "password": {"type": "string", "description": "New meeting password"},
            },
            "required": ["meeting_id"],
        },
    ),
    types.Tool(
        name="delete_meeting",
        description="Delete a scheduled meeting.",
        inputSchema={
            "type": "object",
            "properties": {
                "meeting_id": {"type": "string", "description": "Meeting ID to delete"},
            },
            "required": ["meeting_id"],
        },
    ),
    # ── Policies ────────────────────────────────────────────────────────────
    types.Tool(
        name="list_policies",
        description="List all TeamViewer policies defined in the Management Console.",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    ),
    types.Tool(
        name="get_policy",
        description="Get details of a specific policy by policy ID.",
        inputSchema={
            "type": "object",
            "properties": {
                "policy_id": {"type": "string", "description": "Policy ID"},
            },
            "required": ["policy_id"],
        },
    ),
    # ── Ping ────────────────────────────────────────────────────────────────
    types.Tool(
        name="ping",
        description="Verify the API token is valid and the TeamViewer API is reachable.",
        inputSchema={"type": "object", "properties": {}, "required": []},
    ),
]


# ---------------------------------------------------------------------------
# Handler registration
# ---------------------------------------------------------------------------

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return TOOLS


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    args = arguments or {}

    try:
        # ── Ping ────────────────────────────────────────────────────────────
        if name == "ping":
            data = await tv_get("/ping")
            return ok(data)

        # ── Account ─────────────────────────────────────────────────────────
        elif name == "get_account":
            data = await tv_get("/account")
            return ok(data)

        elif name == "update_account":
            payload = {k: v for k, v in args.items() if v is not None}
            data = await tv_put("/account", payload)
            return ok(data)

        # ── Devices ─────────────────────────────────────────────────────────
        elif name == "list_devices":
            params: dict[str, Any] = {}
            if args.get("groupid"):
                params["groupid"] = args["groupid"]
            if args.get("online_state"):
                params["online_state"] = args["online_state"]
            if args.get("full_list"):
                params["full_list"] = "true"
            data = await tv_get("/devices", params or None)
            return ok(data)

        elif name == "get_device":
            data = await tv_get(f"/devices/{args['device_id']}")
            return ok(data)

        elif name == "update_device":
            device_id = args.pop("device_id")
            payload = {k: v for k, v in args.items() if v is not None}
            data = await tv_put(f"/devices/{device_id}", payload)
            return ok(data)

        elif name == "delete_device":
            data = await tv_delete(f"/devices/{args['device_id']}")
            return ok(data)

        # ── Groups ──────────────────────────────────────────────────────────
        elif name == "list_groups":
            params = {}
            if args.get("name"):
                params["name"] = args["name"]
            data = await tv_get("/groups", params or None)
            return ok(data)

        elif name == "create_group":
            payload: dict[str, Any] = {"name": args["name"]}
            if args.get("policy_id"):
                payload["policy_id"] = args["policy_id"]
            data = await tv_post("/groups", payload)
            return ok(data)

        elif name == "update_group":
            group_id = args.pop("group_id")
            payload = {k: v for k, v in args.items() if v is not None}
            data = await tv_put(f"/groups/{group_id}", payload)
            return ok(data)

        elif name == "delete_group":
            data = await tv_delete(f"/groups/{args['group_id']}")
            return ok(data)

        elif name == "share_group":
            group_id = args["group_id"]
            payload = {"users": args["users"]}
            data = await tv_post(f"/groups/{group_id}/share_group", payload)
            return ok(data)

        # ── Users ────────────────────────────────────────────────────────────
        elif name == "list_users":
            params = {}
            for field in ("name", "email", "permissions"):
                if args.get(field):
                    params[field] = args[field]
            if args.get("full_list"):
                params["full_list"] = "true"
            data = await tv_get("/users", params or None)
            return ok(data)

        elif name == "create_user":
            payload = {k: v for k, v in args.items() if v is not None}
            data = await tv_post("/users", payload)
            return ok(data)

        elif name == "get_user":
            data = await tv_get(f"/users/{args['user_id']}")
            return ok(data)

        elif name == "update_user":
            user_id = args.pop("user_id")
            payload = {k: v for k, v in args.items() if v is not None}
            data = await tv_put(f"/users/{user_id}", payload)
            return ok(data)

        # ── Sessions ─────────────────────────────────────────────────────────
        elif name == "list_sessions":
            params = {}
            if args.get("groupid"):
                params["groupid"] = args["groupid"]
            if args.get("state"):
                params["state"] = args["state"]
            data = await tv_get("/sessions", params or None)
            return ok(data)

        elif name == "create_session":
            payload = {k: v for k, v in args.items() if v is not None}
            data = await tv_post("/sessions", payload)
            return ok(data)

        elif name == "get_session":
            data = await tv_get(f"/sessions/{args['session_code']}")
            return ok(data)

        elif name == "update_session":
            session_code = args.pop("session_code")
            payload = {k: v for k, v in args.items() if v is not None}
            data = await tv_put(f"/sessions/{session_code}", payload)
            return ok(data)

        elif name == "close_session":
            data = await tv_put(
                f"/sessions/{args['session_code']}",
                {"state": "closed"},
            )
            return ok(data)

        # ── Connection Reports ───────────────────────────────────────────────
        elif name == "get_connection_reports":
            params = {}
            field_map = {
                "from_date": "from",
                "to_date": "to",
                "device_id": "deviceid",
                "user_id": "userid",
                "session_code": "sessioncode",
                "limit": "limit",
                "offset": "offset",
            }
            for arg_key, param_key in field_map.items():
                if args.get(arg_key) is not None:
                    params[param_key] = args[arg_key]
            data = await tv_get("/reports/connections", params or None)
            return ok(data)

        # ── Meetings ─────────────────────────────────────────────────────────
        elif name == "list_meetings":
            data = await tv_get("/meetings")
            return ok(data)

        elif name == "create_meeting":
            payload = {k: v for k, v in args.items() if v is not None}
            data = await tv_post("/meetings", payload)
            return ok(data)

        elif name == "get_meeting":
            data = await tv_get(f"/meetings/{args['meeting_id']}")
            return ok(data)

        elif name == "update_meeting":
            meeting_id = args.pop("meeting_id")
            payload = {k: v for k, v in args.items() if v is not None}
            data = await tv_put(f"/meetings/{meeting_id}", payload)
            return ok(data)

        elif name == "delete_meeting":
            data = await tv_delete(f"/meetings/{args['meeting_id']}")
            return ok(data)

        # ── Policies ─────────────────────────────────────────────────────────
        elif name == "list_policies":
            data = await tv_get("/teamviewerpolicies")
            return ok(data)

        elif name == "get_policy":
            data = await tv_get(f"/teamviewerpolicies/{args['policy_id']}")
            return ok(data)

        else:
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps({"error": f"Unknown tool: {name}"}),
                )
            ]

    except httpx.HTTPStatusError as exc:
        error_body = exc.response.text
        return [
            types.TextContent(
                type="text",
                text=json.dumps(
                    {
                        "error": f"TeamViewer API error {exc.response.status_code}",
                        "detail": error_body,
                    },
                    indent=2,
                ),
            )
        ]
    except ValueError as exc:
        return [
            types.TextContent(
                type="text",
                text=json.dumps({"error": str(exc)}, indent=2),
            )
        ]


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

async def run():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mcp-teamviewer",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


def main():
    import asyncio
    asyncio.run(run())


if __name__ == "__main__":
    main()
