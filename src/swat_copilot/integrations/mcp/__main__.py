"""Entry point for MCP server."""

import asyncio
import logging

from swat_copilot.integrations.mcp.server import SWATMCPServer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def main() -> None:
    """Run the SWAT MCP server."""
    server = SWATMCPServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
