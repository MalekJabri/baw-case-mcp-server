# Bob Integration Guide - BAW Case MCP Server

This guide explains how to integrate the BAW Case MCP Server with Bob.

## Quick Integration

### Option 1: Using bob-mcp-config.json

1. **Copy the configuration file** to your Bob MCP servers directory:

```bash
# Copy the config file to Bob's MCP directory
cp bob-mcp-config.json ~/.bob/mcp-servers/baw-case.json
```

2. **Configure your credentials** in the `.env` file:

```bash
# Copy the example file if you haven't already
cp .env.example .env

# Edit with your BAW credentials
nano .env
```

Update these values in `.env`:
```env
MCP_TRANSPORT=stdio
BAW_CASE_MCP_PORT=8001
BAW_BASE_URL=https://your-baw-server.com/bas/CaseManager/CASEREST/v2
BAW_USERNAME=your_username
BAW_PASSWORD=your_password
LOG_LEVEL=INFO
```

3. **Restart Bob** to load the new MCP server

**Note:** The configuration uses the `.env` file in the project directory for credentials, keeping them secure and out of Bob's config files.

### Option 2: Manual Configuration

Add this to your Bob MCP configuration file (usually `~/.bob/config.json` or similar):

```json
{
  "mcpServers": {
    "baw-case": {
      "command": "python3",
      "args": ["baw_case_mcp_server.py"],
      "cwd": "/Users/jabrimalek/development/workspace/bob/BusinessAutomationModes/BAW-Case",
      "env": {
        "MCP_TRANSPORT": "stdio"
      },
      "disabled": false,
      "alwaysAllow": []
    }
  }
}
```

**Note:** Credentials are read from the `.env` file in the project directory (`cwd`), not from Bob's config.

## Configuration Options

### Required Settings

| Setting | Description | Example |
|---------|-------------|---------|
| `command` | Python executable | `python3` or `/path/to/python3` |
| `args` | Server script | `["baw_case_mcp_server.py"]` |
| `cwd` | Project directory | `/full/path/to/BAW-Case` |
| `MCP_TRANSPORT` | Transport mode | `stdio` |

### Optional Settings

| Setting | Description | Default | Location |
|---------|-------------|---------|----------|
| `BAW_CASE_MCP_PORT` | MCP server port | `8001` | `.env` file |
| `BAW_BASE_URL` | BAW server URL | - | `.env` file |
| `BAW_USERNAME` | BAW username | - | `.env` file |
| `BAW_PASSWORD` | BAW password | - | `.env` file |
| `LOG_LEVEL` | Logging level | `INFO` | `.env` file |
| `disabled` | Disable server | `false` | Bob config |
| `alwaysAllow` | Auto-approve tools | `[]` | Bob config |

**Important:** All BAW connection settings (URL, username, password) are configured in the `.env` file in the project directory, not in Bob's configuration. This keeps credentials secure and separate from Bob's config files.

## Using with Bob

Once configured, you can use the BAW Case tools in Bob conversations:

### Example Conversations

**List all solutions:**
```
User: Show me all case solutions in BAW
Bob: [Uses list_solutions tool]
```

**Create a new case:**
```
User: Create a new CustomerComplaint case with high priority
Bob: [Uses create_case tool with appropriate parameters]
```

**Get case details:**
```
User: Show me the properties of case CASE-12345
Bob: [Uses get_case_properties tool]
```

**Add a comment:**
```
User: Add a comment to case CASE-12345 saying "Investigation completed"
Bob: [Uses add_case_comment tool]
```

**Manage stages:**
```
User: Complete the current stage for case CASE-12345
Bob: [Uses complete_current_stage tool]
```

## Available Tools in Bob

When the MCP server is loaded, Bob will have access to these 32 tools:

### System Tools
1. **login** - Get CSRF token

### Solution Management Tools
2. **list_solutions** - List all case solutions
3. **create_solution** - Create a new solution
4. **get_solution_deployment_status** - Get deployment status
5. **get_solution_object_stores** - Get associated object stores
6. **import_solution_manifest** - Import solution manifest
7. **apply_solution_manifest** - Apply manifest to solution
8. **upgrade_solution** - Upgrade a solution
9. **import_solution** - Import a solution
10. **export_solution** - Export a solution
11. **get_solution_pages** - Get solution pages
12. **get_my_roles** - Get current user's roles
13. **configure_custom_widget_extension** - Configure custom widget

### Case Type Tools
14. **get_case_type_properties** - Get case type properties
15. **get_discretionary_activity_types** - Get discretionary activity types

### Case Management Tools
16. **create_case** - Create a new case
17. **get_case_properties** - Get case properties
18. **update_case_properties** - Update case properties
19. **search_cases** - Search for cases

### Case Comment Tools
20. **get_case_comments** - Get case comments
21. **add_case_comment** - Add a comment

### Case Activity Tools
22. **get_case_activities** - Get case activities
23. **get_discretionary_activities** - Get discretionary activities
24. **create_discretionary_activity** - Create discretionary activity

### Quick Task Tools
25. **create_quick_task** - Create a quick task
26. **get_quick_task** - Get quick task details

### Case Stage Tools
27. **get_all_case_stages** - Get all case stages
28. **get_current_case_stage** - Get current stage
29. **complete_current_stage** - Complete current stage
30. **restart_previous_stage** - Restart previous stage
31. **place_stage_on_hold** - Place stage on hold
32. **release_stage_from_hold** - Release stage from hold

## Tool Permissions

### Auto-Approve Tools (Optional)

You can configure Bob to automatically approve certain tools without asking:

```json
{
  "mcpServers": {
    "baw-case": {
      "alwaysAllow": [
        "list_solutions",
        "get_case_properties",
        "get_case_comments",
        "get_case_activities",
        "get_all_case_stages",
        "get_current_case_stage",
        "get_discretionary_activities",
        "get_case_type_properties",
        "get_my_roles"
      ]
    }
  }
}
```

**Recommended for auto-approval:**
- Read-only operations (list, get)

**NOT recommended for auto-approval:**
- Write operations (create, update, delete, complete, restart)

## Security Best Practices

### 1. Credential Management

**Using .env file (Default and Recommended)**

The server automatically reads credentials from the `.env` file in the project directory:

```json
{
  "mcpServers": {
    "baw-case": {
      "command": "python3",
      "args": ["baw_case_mcp_server.py"],
      "cwd": "/path/to/BAW-Case",
      "env": {
        "MCP_TRANSPORT": "stdio"
      }
    }
  }
}
```

Then configure credentials in `.env` file:
```env
MCP_TRANSPORT=stdio
BAW_BASE_URL=https://your-baw-server.com/bas/CaseManager/CASEREST/v2
BAW_USERNAME=your_username
BAW_PASSWORD=your_password
```

**Benefits:**
- ✅ Credentials not in Bob's config files
- ✅ Easy to update without restarting Bob
- ✅ Follows security best practices
- ✅ `.env` file is gitignored by default
- ✅ Uses stdio transport for direct communication

### 2. Restrict Tool Access

Only enable tools you need:
```json
{
  "mcpServers": {
    "baw-case": {
      "disabled": false,
      "alwaysAllow": ["list_solutions", "get_case_properties"],
      "neverAllow": ["delete_case", "update_case_properties"]
    }
  }
}
```

### 3. Use Read-Only Accounts

For non-admin tasks, use BAW accounts with read-only permissions.

## Troubleshooting

### Server Not Starting

**Check Python path:**
```bash
which python3
# Update "command" in config with full path
```

**Check working directory:**
```bash
ls /path/to/BAW-Case/baw_case_mcp_server.py
# Verify file exists
```

**Check dependencies:**
```bash
cd /path/to/BAW-Case
source venv/bin/activate
pip list | grep -E "httpx|dotenv|aicoe"
```

### Authentication Issues

**Test credentials manually:**
```bash
cd /path/to/BAW-Case
python3 baw_case_mcp_server.py test
```

**Check BAW server connectivity:**
```bash
curl -k https://your-baw-server.com/bas/CaseManager/CASEREST/v2/system/login
```

### Bob Integration Issues

**Check Bob logs:**
```bash
# Look for MCP server startup messages
tail -f ~/.bob/logs/mcp-servers.log
```

**Verify server registration:**
```bash
# In Bob, ask: "What MCP servers are available?"
```

**Test individual tools:**
```bash
# In Bob, ask: "Use the login tool from baw-case"
```

### Transport Mode Issues

**Ensure stdio transport is set:**
```env
MCP_TRANSPORT=stdio
```

**Verify in Bob config:**
```json
{
  "env": {
    "MCP_TRANSPORT": "stdio"
  }
}
```

## Advanced Configuration

### Custom Port

If port 8001 is in use:
```env
BAW_CASE_MCP_PORT=8002
```

### Multiple BAW Environments

Configure multiple servers for different environments by using separate project directories:

```json
{
  "mcpServers": {
    "baw-case-dev": {
      "command": "python3",
      "args": ["baw_case_mcp_server.py"],
      "cwd": "/path/to/BAW-Case-Dev",
      "env": {
        "MCP_TRANSPORT": "stdio"
      }
    },
    "baw-case-prod": {
      "command": "python3",
      "args": ["baw_case_mcp_server.py"],
      "cwd": "/path/to/BAW-Case-Prod",
      "env": {
        "MCP_TRANSPORT": "stdio"
      }
    }
  }
}
```

Each directory has its own `.env` file with environment-specific credentials.

### Logging Configuration

Enable detailed logging in the `.env` file:
```env
LOG_LEVEL=DEBUG
```

## Example Use Cases

### 1. Case Management
```
User: "Create a new customer complaint case for John Doe"
Bob: Uses create_case(case_type="CustomerComplaint", properties={...})

User: "Show me all comments on case CASE-12345"
Bob: Uses get_case_comments(case_id="CASE-12345")
```

### 2. Case Workflow
```
User: "What stage is case CASE-12345 in?"
Bob: Uses get_current_case_stage(case_id="CASE-12345")

User: "Complete the current stage for case CASE-12345"
Bob: Uses complete_current_stage(case_id="CASE-12345")
```

### 3. Solution Management
```
User: "List all available case solutions"
Bob: Uses list_solutions()

User: "What are my roles in the CustomerService solution?"
Bob: Uses get_my_roles(solution_name="CustomerService")
```

## Configuration Templates

### Development Environment
```json
{
  "mcpServers": {
    "baw-case": {
      "command": "python3",
      "args": ["baw_case_mcp_server.py"],
      "cwd": "/Users/jabrimalek/development/workspace/bob/BusinessAutomationModes/BAW-Case",
      "env": {
        "MCP_TRANSPORT": "stdio"
      },
      "disabled": false,
      "alwaysAllow": ["list_solutions", "get_case_properties", "get_case_comments"]
    }
  }
}
```

### Production Environment
```json
{
  "mcpServers": {
    "baw-case": {
      "command": "/usr/bin/python3",
      "args": ["baw_case_mcp_server.py"],
      "cwd": "/opt/baw-case",
      "env": {
        "MCP_TRANSPORT": "stdio"
      },
      "disabled": false,
      "alwaysAllow": []
    }
  }
}
```

## Next Steps

1. **Configure the MCP server** using one of the methods above
2. **Test the integration** by asking Bob to list solutions
3. **Explore the tools** by asking Bob what BAW Case operations are available
4. **Extend functionality** by adding more operations from the BAW Case API

## Support

For issues with:
- **MCP Server**: Check the main README.md and QUICKSTART.md
- **Bob Integration**: Check Bob's MCP documentation
- **BAW Case API**: Consult IBM BAW documentation

---

**Made with Bob** 🤖