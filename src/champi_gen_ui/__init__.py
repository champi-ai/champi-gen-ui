"""
Champi-Gen-UI: MCP server for generative UI through ImGui and Python.

This package provides a Model Context Protocol (MCP) server that enables
Large Language Models to create sophisticated user interfaces using ImGui
through natural language commands.
"""

__version__ = "1.0.0"
__author__ = "Divagnz"

from champi_gen_ui.core.canvas import Canvas, CanvasManager
from champi_gen_ui.core.state import CanvasState, WidgetState
from champi_gen_ui.core.widget import Widget, WidgetRegistry

__all__ = [
    "Canvas",
    "CanvasManager",
    "CanvasState",
    "Widget",
    "WidgetRegistry",
    "WidgetState",
    "__version__",
]
