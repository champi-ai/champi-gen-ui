"""Canvas system for rendering UI."""

import threading
import time
from collections.abc import Callable
from queue import Queue
from typing import Any

from imgui_bundle import hello_imgui, imgui, immapp
from loguru import logger

from champi_gen_ui.core.state import CanvasMode, CanvasState, canvas_updated
from champi_gen_ui.core.widget import Widget, WidgetRegistry


class Canvas:
    """Canvas for rendering ImGui UI."""

    def __init__(
        self,
        canvas_id: str,
        width: int = 1280,
        height: int = 720,
        mode: CanvasMode = CanvasMode.STANDARD,
        title: str = "ImGui Canvas",
        **kwargs,
    ):
        """Initialize canvas."""
        self.state = CanvasState(
            canvas_id=canvas_id,
            size=(width, height),
            mode=mode,
            title=title,
        )
        self.widget_registry = WidgetRegistry()
        self._running = False
        self._render_thread: threading.Thread | None = None
        self._command_queue: Queue = Queue()
        self._needs_render = False

        logger.info(
            f"Created canvas {canvas_id} ({width}x{height}) in {mode.value} mode"
        )

    def add_widget(self, widget: Widget) -> None:
        """Add a widget to the canvas."""
        self.widget_registry.add(widget)
        self.state.widgets[widget.widget_id] = widget.state
        self._needs_render = True  # Signal that render is needed
        logger.debug(
            f"Added widget {widget.widget_id} to canvas {self.state.canvas_id}"
        )

    def remove_widget(self, widget_id: str) -> bool:
        """Remove a widget from the canvas."""
        if widget_id in self.state.widgets:
            del self.state.widgets[widget_id]
            return self.widget_registry.remove(widget_id)
        return False

    def get_widget(self, widget_id: str) -> Widget | None:
        """Get a widget by ID."""
        return self.widget_registry.get(widget_id)

    def clear(self) -> None:
        """Clear all widgets from the canvas."""
        self.widget_registry.clear()
        self.state.widgets.clear()
        self._needs_render = True
        logger.info(f"Cleared canvas {self.state.canvas_id}")

    def queue_command(self, command: Callable[[], Any]) -> None:
        """Queue a command for execution on the render thread."""
        self._command_queue.put(command)
        self._needs_render = True

    def process_commands(self) -> None:
        """Process queued commands (called from render thread)."""
        while not self._command_queue.empty():
            try:
                command = self._command_queue.get_nowait()
                command()
            except Exception as e:
                logger.error(f"Error processing command: {e}", exc_info=True)

    def render(self) -> None:
        """Render all widgets on the canvas."""
        if not self.state.active:
            return

        # Render in a window
        imgui.begin(self.state.title, None, imgui.WindowFlags_.no_collapse.value)

        # Render all visible widgets
        for widget in self.widget_registry.get_all().values():
            if widget.state.visible:
                try:
                    # Set position if specified
                    if widget.state.position:
                        imgui.set_cursor_pos(imgui.ImVec2(*widget.state.position))

                    # Render the widget
                    widget.render()

                except Exception as e:
                    logger.error(
                        f"Error rendering widget {widget.widget_id}: {e}", exc_info=True
                    )

        imgui.end()

    def run(self) -> None:
        """Run the canvas in standalone mode (blocking)."""
        self._running = True

        def gui_func():
            if self._running:
                # Process any queued commands first
                self.process_commands()
                self.render()

        # Configure runner params
        runner_params = hello_imgui.RunnerParams()
        runner_params.app_window_params.window_title = self.state.title
        runner_params.app_window_params.window_geometry.size = (
            self.state.size[0],
            self.state.size[1],
        )
        runner_params.fps_idling.fps_idle = self.state.fps_idle

        # Set docking if needed
        if self.state.mode == CanvasMode.DOCKING:
            runner_params.imgui_window_params.enable_viewports = True
            runner_params.imgui_window_params.default_imgui_window_type = (
                hello_imgui.DefaultImGuiWindowType.provide_full_screen_dock_space
            )

        immapp.run(
            gui_function=gui_func,
            window_title=self.state.title,
            window_size=self.state.size,
            fps_idle=self.state.fps_idle,
        )

    def run_async(self) -> None:
        """Run the canvas in non-blocking mode (for MCP server use)."""
        if self._running:
            logger.warning(f"Canvas {self.state.canvas_id} is already running")
            return

        self._running = True
        self.state.active = True

        def render_loop():
            """Background rendering loop."""
            logger.info(f"Starting async render loop for canvas {self.state.canvas_id}")

            def gui_func():
                if self._running:
                    # Process any queued commands
                    self.process_commands()
                    # Render widgets
                    self.render()

            try:
                # Configure runner params
                runner_params = hello_imgui.RunnerParams()
                runner_params.app_window_params.window_title = self.state.title
                runner_params.app_window_params.window_geometry.size = (
                    self.state.size[0],
                    self.state.size[1],
                )
                runner_params.fps_idling.fps_idle = self.state.fps_idle

                # Set docking if needed
                if self.state.mode == CanvasMode.DOCKING:
                    runner_params.imgui_window_params.enable_viewports = True
                    runner_params.imgui_window_params.default_imgui_window_type = hello_imgui.DefaultImGuiWindowType.provide_full_screen_dock_space

                # Run ImGui loop (this blocks until window closed)
                immapp.run(
                    gui_function=gui_func,
                    window_title=self.state.title,
                    window_size=self.state.size,
                    fps_idle=self.state.fps_idle,
                )

            except Exception as e:
                logger.error(f"Error in render loop: {e}", exc_info=True)
            finally:
                self._running = False
                self.state.active = False
                logger.info(f"Render loop stopped for canvas {self.state.canvas_id}")

        # Start render thread
        self._render_thread = threading.Thread(
            target=render_loop, name=f"Canvas-{self.state.canvas_id}", daemon=True
        )
        self._render_thread.start()
        logger.info(f"Started async canvas {self.state.canvas_id}")

        # Give the thread a moment to initialize
        time.sleep(0.1)

    def stop(self) -> None:
        """Stop the canvas."""
        self._running = False
        logger.info(f"Stopped canvas {self.state.canvas_id}")

    def update_properties(self, **props) -> None:
        """Update canvas properties."""
        if "size" in props:
            self.state.size = tuple(props["size"])
        if "mode" in props:
            mode_str = props["mode"]
            self.state.mode = CanvasMode(mode_str)
        if "theme" in props:
            self.state.theme = props["theme"]
        if "title" in props:
            self.state.title = props["title"]

        canvas_updated.send(self, canvas=self)
        logger.debug(f"Updated canvas {self.state.canvas_id} with {props}")

    def serialize(self) -> dict:
        """Serialize canvas state to dictionary."""
        return self.state.to_dict()


class CanvasManager:
    """Manager for multiple canvases."""

    def __init__(self):
        """Initialize canvas manager."""
        self.canvases: dict[str, Canvas] = {}
        self.active_canvas: str | None = None
        self._auto_start = True  # Auto-start canvases for MCP use
        logger.info("Initialized CanvasManager")

    def create_canvas(
        self, canvas_id: str, auto_start: bool | None = None, **props
    ) -> Canvas:
        """Create a new canvas.

        Args:
            canvas_id: Unique canvas identifier
            auto_start: Whether to auto-start the canvas (defaults to self._auto_start)
            **props: Canvas properties (width, height, mode, title, etc.)
        """
        if canvas_id in self.canvases:
            raise ValueError(f"Canvas {canvas_id} already exists")

        canvas = Canvas(canvas_id, **props)
        self.canvases[canvas_id] = canvas

        # Set as active if first canvas
        if self.active_canvas is None:
            self.active_canvas = canvas_id

        # Auto-start canvas if enabled
        should_auto_start = auto_start if auto_start is not None else self._auto_start
        if should_auto_start:
            canvas.run_async()

        logger.info(f"Created canvas {canvas_id} (auto_start={should_auto_start})")
        return canvas

    def get_canvas(self, canvas_id: str) -> Canvas | None:
        """Get a canvas by ID."""
        return self.canvases.get(canvas_id)

    def remove_canvas(self, canvas_id: str) -> bool:
        """Remove a canvas."""
        if canvas_id in self.canvases:
            canvas = self.canvases[canvas_id]
            canvas.stop()
            del self.canvases[canvas_id]

            # Update active canvas
            if self.active_canvas == canvas_id:
                self.active_canvas = (
                    next(iter(self.canvases.keys())) if self.canvases else None
                )

            logger.info(f"Removed canvas {canvas_id}")
            return True
        return False

    def list_canvases(self) -> list[str]:
        """List all canvas IDs."""
        return list(self.canvases.keys())

    def set_active_canvas(self, canvas_id: str) -> bool:
        """Set the active canvas."""
        if canvas_id in self.canvases:
            self.active_canvas = canvas_id
            logger.debug(f"Set active canvas to {canvas_id}")
            return True
        return False

    def get_active_canvas(self) -> Canvas | None:
        """Get the active canvas."""
        if self.active_canvas:
            return self.canvases.get(self.active_canvas)
        return None

    def render_all(self) -> None:
        """Render all active canvases."""
        for canvas in self.canvases.values():
            if canvas.state.active:
                canvas.render()

    def ensure_canvas_running(self, canvas_id: str) -> bool:
        """Ensure a canvas is running, start it if not.

        Args:
            canvas_id: Canvas identifier

        Returns:
            True if canvas is running, False if canvas doesn't exist
        """
        canvas = self.get_canvas(canvas_id)
        if not canvas:
            return False

        if not canvas._running:
            logger.info(f"Auto-starting canvas {canvas_id}")
            canvas.run_async()

        return True

    def stop_all(self) -> None:
        """Stop all running canvases."""
        for canvas in self.canvases.values():
            if canvas._running:
                canvas.stop()
        logger.info("Stopped all canvases")
