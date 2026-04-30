# Project Comparison: BAW-Admin vs BAW-Case

This document compares the BAW-Admin and BAW-Case MCP servers to highlight their differences and similarities.

## Overview

| Aspect | BAW-Admin | BAW-Case |
|--------|-----------|----------|
| **Purpose** | System and Container operations | Case Management operations |
| **API Base Path** | `/bas/ops` | `/bas/CaseManager/CASEREST/v2` |
| **Number of Tools** | 11 tools | 32 tools |
| **Default Port** | 8000 | 8001 |
| **Transport Mode** | stdio | stdio |

## Configuration Comparison

### Environment Variables

Both projects use identical configuration structure:

**BAW-Admin (.env):**
```env
MCP_TRANSPORT=stdio
BAW_MCP_PORT=8000
BAW_BASE_URL=https://your-baw-server.com/bas/ops
BAW_USERNAME=your_username
BAW_PASSWORD=your_password
LOG_LEVEL=INFO
```

**BAW-Case (.env):**
```env
MCP_TRANSPORT=stdio
BAW_CASE_MCP_PORT=8001
BAW_BASE_URL=https://your-baw-server.com/bas/CaseManager/CASEREST/v2
BAW_USERNAME=your_username
BAW_PASSWORD=your_password
LOG_LEVEL=INFO
```

**Key Differences:**
- Port variable name: `BAW_MCP_PORT` vs `BAW_CASE_MCP_PORT`
- Default port: 8000 vs 8001
- Base URL path: `/bas/ops` vs `/bas/CaseManager/CASEREST/v2`

### Bob Configuration

Both use identical Bob integration structure:

**BAW-Admin (bob-mcp-config.json):**
```json
{
  "mcpServers": {
    "baw-admin": {
      "command": "python3",
      "args": ["baw_mcp_server.py"],
      "cwd": "/path/to/BAW-Admin",
      "env": {
        "MCP_TRANSPORT": "stdio"
      }
    }
  }
}
```

**BAW-Case (bob-mcp-config.json):**
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

**Key Differences:**
- Server name: `baw-admin` vs `baw-case`
- Script name: `baw_mcp_server.py` vs `baw_case_mcp_server.py`
- Working directory path

## Tool Comparison

### BAW-Admin Tools (11 total)

**System Operations (3):**
1. login
2. get_queue_status
3. validate_database

**Container Operations (8):**
4. list_containers
5. get_container
6. create_container
7. count_containers
8. archive_container
9. restore_container
10. delete_container
11. check_orphaned_containers
12. migrate_container_instances

### BAW-Case Tools (32 total)

**System Operations (1):**
1. login

**Solution Management (12):**
2. list_solutions
3. create_solution
4. get_solution_deployment_status
5. get_solution_object_stores
6. import_solution_manifest
7. apply_solution_manifest
8. upgrade_solution
9. import_solution
10. export_solution
11. get_solution_pages
12. get_my_roles
13. configure_custom_widget_extension

**Case Type Operations (2):**
14. get_case_type_properties
15. get_discretionary_activity_types

**Case Management (4):**
16. create_case
17. get_case_properties
18. update_case_properties
19. search_cases

**Case Comments (2):**
20. get_case_comments
21. add_case_comment

**Case Activities (3):**
22. get_case_activities
23. get_discretionary_activities
24. create_discretionary_activity

**Quick Tasks (2):**
25. create_quick_task
26. get_quick_task

**Case Stages (6):**
27. get_all_case_stages
28. get_current_case_stage
29. complete_current_stage
30. restart_previous_stage
31. place_stage_on_hold
32. release_stage_from_hold

## Code Structure Comparison

### Similarities

Both projects share:
- ✅ Same base class: `BaseMCP` from `aicoe_agent_utils.mcp.base_mcp`
- ✅ Same decorator: `@tool` for marking MCP tools
- ✅ Same async pattern: All tools are async methods
- ✅ Same context parameter: `ctx: Context` required for all tools
- ✅ Same authentication: CSRF token management
- ✅ Same HTTP client: `httpx.AsyncClient`
- ✅ Same error handling pattern
- ✅ Same test mode: `python3 script.py test`
- ✅ Same transport mode: stdio for Bob integration

### Differences

**Class Names:**
- BAW-Admin: `class BAWAdminMCP(BaseMCP)`
- BAW-Case: `class BAWCaseMCP(BaseMCP)`

**API Endpoints:**
- BAW-Admin: Uses `/std/bpm/containers/*` and `/system/*`
- BAW-Case: Uses `/case/*`, `/solution/*`, `/casetype/*`

**Tool Complexity:**
- BAW-Admin: Simpler operations (list, get, create, delete)
- BAW-Case: More complex workflows (stages, activities, comments)

## File Structure Comparison

### Common Files

Both projects have:
```
├── aicoe-agent-utils/          # Git submodule
├── __init__.py                 # Package init
├── requirements.txt            # Dependencies (identical)
├── .env.example                # Environment template
├── .env                        # Local configuration
├── .gitignore                  # Git ignore (identical)
├── .gitmodules                 # Submodule config (identical)
├── README.md                   # Main documentation
├── BOB_INTEGRATION.md          # Bob integration guide
├── QUICKSTART.md               # Quick start guide
└── bob-mcp-config.json         # Bob configuration
```

### Unique Files

**BAW-Admin only:**
- `baw-ops.json` - API specification
- Additional documentation files

**BAW-Case only:**
- `baw-case.json` - API specification
- `PROJECT_COMPARISON.md` - This file

## Use Cases

### When to Use BAW-Admin

Use BAW-Admin for:
- Managing process applications and toolkits
- Container lifecycle operations (create, archive, delete)
- Migrating process instances between snapshots
- Checking for orphaned toolkits
- System administration tasks
- Database validation

### When to Use BAW-Case

Use BAW-Case for:
- Creating and managing case instances
- Adding comments to cases
- Managing case activities and tasks
- Controlling case stages (complete, restart, hold)
- Solution deployment and configuration
- Case type management
- Discretionary activity management
- Quick task operations

## Integration Strategy

### Running Both Servers

You can run both servers simultaneously in Bob:

```json
{
  "mcpServers": {
    "baw-admin": {
      "command": "python3",
      "args": ["baw_mcp_server.py"],
      "cwd": "/path/to/BAW-Admin",
      "env": {
        "MCP_TRANSPORT": "stdio"
      }
    },
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

### Complementary Operations

The two servers complement each other:

1. **BAW-Admin** manages the infrastructure (containers, applications)
2. **BAW-Case** manages the business operations (cases, activities, stages)

Example workflow:
```
1. Use BAW-Admin to list available process applications
2. Use BAW-Case to create cases based on those applications
3. Use BAW-Case to manage case lifecycle
4. Use BAW-Admin to migrate instances when upgrading applications
```

## Dependencies

Both projects use identical dependencies:

```txt
python-dotenv>=1.0.0
httpx>=0.28.1
aiofiles>=24.1.0
-e ./aicoe-agent-utils[mcp]
```

## Security Considerations

Both projects follow the same security practices:

- ✅ Credentials stored in `.env` file (gitignored)
- ✅ CSRF token management
- ✅ HTTPS support (configurable)
- ✅ Basic authentication
- ✅ stdio transport for secure communication with Bob

## Performance Considerations

**BAW-Admin:**
- Fewer tools = faster initialization
- Simpler operations = lower latency
- Suitable for frequent administrative tasks

**BAW-Case:**
- More tools = slightly longer initialization
- Complex operations = may take longer
- Suitable for business process management

## Maintenance

Both projects require:
- Regular credential rotation
- Dependency updates
- Submodule updates
- BAW server compatibility checks

## Summary

| Feature | BAW-Admin | BAW-Case |
|---------|-----------|----------|
| **Focus** | Infrastructure | Business Operations |
| **Complexity** | Lower | Higher |
| **Tool Count** | 11 | 32 |
| **Use Case** | Administration | Case Management |
| **Port** | 8000 | 8001 |
| **API Path** | `/bas/ops` | `/bas/CaseManager/CASEREST/v2` |
| **Transport** | stdio | stdio |
| **Framework** | aicoe-agent-utils | aicoe-agent-utils |

Both servers are production-ready and can be used independently or together for comprehensive BAW management.

---

**Made with Bob** 🤖