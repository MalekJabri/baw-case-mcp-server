"""
Backward compatibility wrapper for BAW Case MCP Server.

This file maintains backward compatibility with the old structure.
The actual implementation is now in the baw_case_mcp package.
"""

import sys
import asyncio
from baw_case_mcp import BAWCaseMCP


if __name__ == "__main__":
    mcp = BAWCaseMCP()
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Run test mode
        asyncio.run(mcp.test())
    else:
        # Run MCP server
        mcp.run()

# Made with Bob