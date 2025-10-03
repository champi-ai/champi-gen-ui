"""Canvas system for rendering UI."""

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

        logger.info(
            f"Created canvas {canvas_id} ({width}x{height}) in {mode.value} mode"
        )

    def add_widget(self, widget: Widget) -> None:
        """Add a widget to the canvas."""
        self.widget_registry.add(widget)
        self.state.widgets[widget.widget_id] = widget.state
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
        logger.info(f"Cleared canvas {self.state.canvas_id}")

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
        """Run the canvas in standalone mode."""
        self._running = True

        def gui_func():
            if self._running:
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
        logger.info("Initialized CanvasManager")

    def create_canvas(self, canvas_id: str, **props) -> Canvas:
        """Create a new canvas."""
        if canvas_id in self.canvases:
            raise ValueError(f"Canvas {canvas_id} already exists")

        canvas = Canvas(canvas_id, **props)
        self.canvases[canvas_id] = canvas

        # Set as active if first canvas
        if self.active_canvas is None:
            self.active_canvas = canvas_id

        logger.info(f"Created canvas {canvas_id}")
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
