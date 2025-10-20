"""CLI entry point for champi-gen-ui."""

import atexit
import signal
import sys

from loguru import logger

from champi_gen_ui.server.main import canvas_manager, mcp


def cleanup():
    """Cleanup function called on exit."""
    logger.info("Cleaning up...")
    try:
        canvas_manager.stop_all()
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")


def signal_handler(signum, frame):
    """Handle shutdown signals."""
    logger.info(f"Received signal {signum}, shutting down...")
    cleanup()
    sys.exit(0)


def main():
    """Main CLI entry point."""
    # Configure logger
    logger.remove()
    logger.add(sys.stderr, level="INFO")

    logger.info("Starting Champi-Gen-UI MCP server...")

    # Register cleanup handlers
    atexit.register(cleanup)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        # Run the FastMCP server
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Server interrupted by user")
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
    finally:
        cleanup()


if __name__ == "__main__":
    main()
