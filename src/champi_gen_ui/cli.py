"""CLI entry point for champi-gen-ui."""

import sys

from loguru import logger

from champi_gen_ui.server.main import mcp


def main():
    """Main CLI entry point."""
    # Configure logger
    logger.remove()
    logger.add(sys.stderr, level="INFO")

    logger.info("Starting Champi-Gen-UI MCP server...")

    # Run the FastMCP server
    mcp.run()


if __name__ == "__main__":
    main()
