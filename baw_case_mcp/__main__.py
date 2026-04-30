"""Entry point for running the BAW Case MCP Server as a module."""

import sys
import asyncio
from .server import BAWCaseMCP


def main():
    """Main entry point for the BAW Case MCP Server."""
    mcp = BAWCaseMCP()
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Run test mode
        asyncio.run(mcp.test())
    else:
        # Run MCP server - BaseMCP.run() handles stdio communication
        try:
            mcp.run()
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"Error starting MCP server: {e}", file=sys.stderr)
            raise


if __name__ == "__main__":
    main()

# Made with Bob
