# BAW Case MCP Server

A Model Context Protocol (MCP) server for IBM Business Automation Workflow (BAW) Case Management. This server provides comprehensive tools for managing cases, solutions, activities, and stages through the BAW Case REST API.

## Features

This MCP server exposes **32 tools** organized into the following categories:

### System Operations
- `login` - Obtain CSRF prevention token

### Solution Management
- `list_solutions` - List all case solutions
- `create_solution` - Create a new case solution
- `get_solution_deployment_status` - Get deployment status
- `get_solution_object_stores` - Get associated object stores
- `import_solution_manifest` - Import a solution manifest
- `apply_solution_manifest` - Apply manifest to a solution
- `upgrade_solution` - Upgrade a solution
- `import_solution` - Import a solution
- `export_solution` - Export a solution
- `get_solution_pages` - Get solution pages
- `get_my_roles` - Get current user's roles
- `configure_custom_widget_extension` - Configure custom widget

### Case Type Operations
- `get_case_type_properties` - Get case type properties
- `get_discretionary_activity_types` - Get discretionary activity types

### Case Management
- `create_case` - Create a new case instance
- `get_case_properties` - Get case properties
- `update_case_properties` - Update case properties
- `search_cases` - Search for case instances

### Case Comments
- `get_case_comments` - Get case comments
- `add_case_comment` - Add a comment to a case

### Case Activities
- `get_case_activities` - Get case activities
- `get_discretionary_activities` - Get discretionary activities
- `create_discretionary_activity` - Create a discretionary activity

### Quick Tasks
- `create_quick_task` - Create a quick task
- `get_quick_task` - Get quick task details

### Case Stages
- `get_all_case_stages` - Retrieve all case stages
- `get_current_case_stage` - Get current stage
- `complete_current_stage` - Complete current stage
- `restart_previous_stage` - Restart previous stage
- `place_stage_on_hold` - Place stage on hold
- `release_stage_from_hold` - Release stage from hold

## Installation

### Prerequisites
- Python 3.10 or higher
- Git
- Access to IBM Business Automation Workflow server

### Setup

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd BAW-Case
```

2. **Initialize submodules:**
```bash
git submodule update --init --recursive
```

3. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

5. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your BAW server details
```

### Configuration

Edit the `.env` file with your BAW server configuration:

```env
# Transport mode: "stdio" for Bob/Claude Desktop, "streamable-http" for HTTP server
MCP_TRANSPORT=stdio
BAW_CASE_MCP_PORT=8001

# BAW Server Configuration
BAW_BASE_URL=https://your-baw-server.com/bas/CaseManager/CASEREST/v2
BAW_USERNAME=your_username
BAW_PASSWORD=your_password

# Optional: Logging Configuration
LOG_LEVEL=INFO
```

## Usage

### Running the Server

**Standard mode (MCP server):**
```bash
python3 baw_case_mcp_server.py
```

**Test mode (verify connectivity):**
```bash
python3 baw_case_mcp_server.py test
```

### Integration with Bob/Claude Desktop

Add to your MCP configuration file:

**For Bob:**
```json
{
  "mcpServers": {
    "baw-case": {
      "command": "python3",
      "args": [
        "/path/to/BAW-Case/baw_case_mcp_server.py"
      ],
      "env": {
        "BAW_BASE_URL": "https://your-baw-server.com/bas/CaseManager/CASEREST/v2",
        "BAW_USERNAME": "your_username",
        "BAW_PASSWORD": "your_password"
      }
    }
  }
}
```

**For Claude Desktop:**
```json
{
  "mcpServers": {
    "baw-case": {
      "command": "python3",
      "args": [
        "/path/to/BAW-Case/baw_case_mcp_server.py"
      ],
      "env": {
        "BAW_BASE_URL": "https://your-baw-server.com/bas/CaseManager/CASEREST/v2",
        "BAW_USERNAME": "your_username",
        "BAW_PASSWORD": "your_password"
      }
    }
  }
}
```

## API Reference

### Example: Creating a Case

```python
# Using the MCP tool
result = await create_case(
    ctx=context,
    case_type="CustomerComplaint",
    properties={
        "CustomerName": "John Doe",
        "Priority": "High",
        "Description": "Product quality issue"
    }
)
```

### Example: Adding a Comment

```python
result = await add_case_comment(
    ctx=context,
    case_id="CASE-12345",
    comment_text="Investigation completed. Moving to resolution."
)
```

### Example: Managing Stages

```python
# Get current stage
current_stage = await get_current_case_stage(ctx=context, case_id="CASE-12345")

# Complete current stage
result = await complete_current_stage(ctx=context, case_id="CASE-12345")
```

## Architecture

This server is built using the `aicoe-agent-utils` library and follows the BaseMCP pattern:

- **BaseMCP**: Provides the foundation for MCP server functionality
- **@tool decorator**: Marks methods as MCP tools
- **Context parameter**: Required for all tool methods
- **Async methods**: All tools are asynchronous for better performance

## Development

### Project Structure

```
BAW-Case/
├── aicoe-agent-utils/      # Git submodule
├── baw_case_mcp_server.py  # Main server implementation
├── __init__.py             # Package initialization
├── requirements.txt        # Python dependencies
├── .env.example            # Environment template
├── .gitignore              # Git ignore rules
├── .gitmodules             # Submodule configuration
└── README.md               # This file
```

### Adding New Tools

To add a new tool:

1. Add the `@tool` decorator
2. Make the method async
3. Include `ctx: Context` as the first parameter
4. Add comprehensive docstring with Args and Returns sections
5. Use `self._make_request()` for API calls

Example:
```python
@tool
async def my_new_tool(
    self,
    ctx: Context,
    param1: str,
    param2: Optional[int] = None
) -> Dict[str, Any]:
    """
    Description of what the tool does.
    
    Args:
        ctx: MCP context
        param1: Description of param1
        param2: Optional description of param2
        
    Returns:
        Dict containing the result
    """
    return await self._make_request("GET", f"/endpoint/{param1}")
```

## Troubleshooting

### Common Issues

**Import errors:**
```bash
# Verify submodules are initialized
git submodule update --init --recursive
```

**Connection errors:**
- Verify BAW server URL is correct
- Check username and password
- Ensure network connectivity to BAW server
- Verify SSL certificate settings (set `verify=True` in production)

**Port already in use:**
- Change `BAW_CASE_MCP_PORT` in `.env` file
- Or kill the process using the port

### Debug Mode

Enable debug logging:
```env
LOG_LEVEL=DEBUG
```

## Security Considerations

- **Never commit `.env` file** - Contains sensitive credentials
- **Use HTTPS in production** - Set `verify=True` in httpx client
- **Rotate credentials regularly** - Update BAW username/password
- **Limit access** - Use appropriate BAW user permissions

## Related Projects

- [BAW Admin MCP Server](../BAW-Admin) - Administration and container management
- [aicoe-agent-utils](https://github.ibm.com/AI-CoE/aicoe-agent-utils) - MCP server framework

## License

[Your License Here]

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions:
- Open an issue in the repository
- Contact the development team
- Check IBM BAW documentation

## Changelog

### Version 0.1.0 (Initial Release)
- 32 tools covering all BAW Case REST API endpoints
- System operations (login, CSRF token)
- Solution management (create, import, export, upgrade)
- Case management (create, update, search)
- Case comments and activities
- Quick tasks
- Stage management (complete, restart, hold/release)
- Full integration with aicoe-agent-utils

---

**Made with Bob** 🤖