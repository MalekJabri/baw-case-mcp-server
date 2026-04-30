# Quick Start Guide - BAW Case MCP Server

This guide will help you get the BAW Case MCP Server up and running quickly.

## Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.10+ installed
- ✅ Git installed
- ✅ Access to a BAW server with Case Management
- ✅ Valid BAW credentials (username/password)

## 5-Minute Setup

### Step 1: Verify Submodule (Already Done)

The `aicoe-agent-utils` submodule should already be initialized. Verify:

```bash
git submodule status
# Should show the aicoe-agent-utils submodule
```

If not initialized, run:
```bash
git submodule update --init --recursive
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `python-dotenv` - Environment variable management
- `httpx` - HTTP client for API calls
- `aiofiles` - Async file operations
- `aicoe-agent-utils[mcp]` - MCP server framework

### Step 4: Configure Environment

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your editor
nano .env  # or vim, code, etc.
```

**Minimum required configuration:**
```env
MCP_TRANSPORT=stdio
BAW_CASE_MCP_PORT=8001
BAW_BASE_URL=https://your-baw-server.com/bas/CaseManager/CASEREST/v2
BAW_USERNAME=your_username
BAW_PASSWORD=your_password
```

**Example for local development:**
```env
MCP_TRANSPORT=stdio
BAW_CASE_MCP_PORT=8001
BAW_BASE_URL=https://localhost:9443/bas/CaseManager/CASEREST/v2
BAW_USERNAME=admin
BAW_PASSWORD=admin
LOG_LEVEL=INFO
```

### Step 5: Test the Server

```bash
# Run the built-in test
python3 baw_case_mcp_server.py test
```

Expected output:
```
Testing BAW Case MCP Server...
Base URL: https://your-baw-server.com/bas/CaseManager/CASEREST/v2
Username: your_username

1. Testing login...
Login result: {'success': True, 'csrf_token': '...', 'message': 'Successfully obtained CSRF token'}

2. Testing list_solutions...
Solutions: {...}

Test completed!
```

### Step 6: Start the Server

```bash
python3 baw_case_mcp_server.py
```

The server will start in stdio mode for Bob/Claude Desktop integration.

## Verify Installation

### Check Files Created

```bash
ls -la
```

You should see:
- ✅ `aicoe-agent-utils/` - Submodule directory
- ✅ `baw_case_mcp_server.py` - Main server file (835 lines)
- ✅ `requirements.txt` - Dependencies
- ✅ `.env` - Your configuration (not in git)
- ✅ `.env.example` - Template
- ✅ `.gitignore` - Git ignore rules
- ✅ `README.md` - Full documentation
- ✅ `BOB_INTEGRATION.md` - Bob integration guide
- ✅ `bob-mcp-config.json` - Bob configuration template
- ✅ `__init__.py` - Package file

### Check Virtual Environment

```bash
which python3  # Should show path in venv/
pip list | grep -E "httpx|dotenv|aicoe"
```

## Common Issues & Solutions

### Issue: Submodule not found

**Solution:**
```bash
git submodule add https://github.ibm.com/AI-CoE/aicoe-agent-utils.git
git submodule update --init --recursive
```

### Issue: Import errors when running

**Solution:**
```bash
# Ensure venv is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Connection refused to BAW server

**Solutions:**
1. Check `BAW_BASE_URL` is correct (should include `/bas/CaseManager/CASEREST/v2`)
2. Verify network connectivity: `ping your-baw-server.com`
3. Check if BAW server is running
4. Verify port and protocol (http vs https)

### Issue: Authentication failed

**Solutions:**
1. Verify credentials in `.env`
2. Check if user has proper BAW Case Management permissions
3. Try logging into BAW web interface with same credentials

### Issue: CSRF token error

**Solution:**
```bash
# Test login explicitly
python3 baw_case_mcp_server.py test
```

### Issue: Transport mode not working

**Solution:**
Ensure `MCP_TRANSPORT=stdio` is set in `.env`:
```env
MCP_TRANSPORT=stdio
```

## Next Steps

Once the server is running:

1. **Explore Available Tools**: See README.md for full list of 32 operations
2. **Connect to Bob**: Follow BOB_INTEGRATION.md for Bob setup
3. **Test Operations**: Try creating cases, adding comments, managing stages
4. **Add More Operations**: Extend the server with additional BAW Case operations

## Available Operations

### System Operations (1 tool)
- `login` - Get CSRF token

### Solution Management (12 tools)
- `list_solutions` - List all solutions
- `create_solution` - Create new solution
- `get_solution_deployment_status` - Get deployment status
- `get_solution_object_stores` - Get object stores
- `import_solution_manifest` - Import manifest
- `apply_solution_manifest` - Apply manifest
- `upgrade_solution` - Upgrade solution
- `import_solution` - Import solution
- `export_solution` - Export solution
- `get_solution_pages` - Get solution pages
- `get_my_roles` - Get user roles
- `configure_custom_widget_extension` - Configure widget

### Case Type Operations (2 tools)
- `get_case_type_properties` - Get case type properties
- `get_discretionary_activity_types` - Get activity types

### Case Management (4 tools)
- `create_case` - Create new case
- `get_case_properties` - Get case properties
- `update_case_properties` - Update properties
- `search_cases` - Search cases

### Case Comments (2 tools)
- `get_case_comments` - Get comments
- `add_case_comment` - Add comment

### Case Activities (3 tools)
- `get_case_activities` - Get activities
- `get_discretionary_activities` - Get discretionary activities
- `create_discretionary_activity` - Create activity

### Quick Tasks (2 tools)
- `create_quick_task` - Create task
- `get_quick_task` - Get task details

### Case Stages (6 tools)
- `get_all_case_stages` - Get all stages
- `get_current_case_stage` - Get current stage
- `complete_current_stage` - Complete stage
- `restart_previous_stage` - Restart stage
- `place_stage_on_hold` - Place on hold
- `release_stage_from_hold` - Release from hold

## Testing Individual Operations

You can test operations using Python:

```python
import asyncio
from baw_case_mcp_server import BAWCaseMCP

async def test_operation():
    mcp = BAWCaseMCP()
    
    class MockContext:
        pass
    
    ctx = MockContext()
    
    # Test login
    result = await mcp.login(ctx)
    print(result)
    
    # Test list solutions
    solutions = await mcp.list_solutions(ctx)
    print(solutions)
    
    # Test get case properties
    case_props = await mcp.get_case_properties(ctx, case_id="CASE-12345")
    print(case_props)
    
    await mcp.client.aclose()

asyncio.run(test_operation())
```

## Integration with Bob

### Quick Bob Setup

1. Copy the Bob configuration:
```bash
cp bob-mcp-config.json ~/.bob/mcp-servers/baw-case.json
```

2. Update the `cwd` path in the config to match your installation

3. Restart Bob

4. Test in Bob:
```
User: List all case solutions
Bob: [Uses list_solutions tool]
```

See `BOB_INTEGRATION.md` for detailed integration instructions.

## Production Deployment

For production use:

1. **Enable SSL Verification**: In `baw_case_mcp_server.py`, change `verify=False` to `verify=True`
2. **Use Strong Passwords**: Never use default credentials
3. **Restrict Access**: Use firewall rules to limit MCP server access
4. **Enable Logging**: Set `LOG_LEVEL=INFO` or `DEBUG` in `.env`
5. **Monitor Server**: Set up health checks and monitoring
6. **Rotate Credentials**: Regularly update BAW passwords
7. **Use stdio Transport**: Keep `MCP_TRANSPORT=stdio` for Bob integration

## Getting Help

- 📖 Full documentation: See `README.md`
- 🔧 Bob integration: See `BOB_INTEGRATION.md`
- 🐛 Issues: Check troubleshooting section in README
- 💬 Questions: Contact your BAW administrator

## Summary

You now have a working BAW Case MCP Server with:
- ✅ 32 Case Management operations
- ✅ System operations (login, CSRF)
- ✅ Solution management (12 tools)
- ✅ Case operations (create, update, search)
- ✅ Comment and activity management
- ✅ Stage management (complete, restart, hold)
- ✅ Proper authentication handling
- ✅ Error handling and logging
- ✅ Test mode for validation
- ✅ stdio transport for Bob integration

Ready to manage your BAW cases! 🚀

---

**Made with Bob** 🤖