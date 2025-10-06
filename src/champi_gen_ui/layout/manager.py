"""Layout manager for arranging widgets."""

from enum import Enum

from imgui_bundle import imgui
from loguru import logger


class LayoutMode(Enum):
    """Layout modes for widget arrangement."""

    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
    GRID = "grid"
    STACK = "stack"
    FREE = "free"  # Manual positioning


class LayoutManager:
    """Manager for widget layout."""

    def __init__(self):
        """Initialize layout manager."""
        self.mode = LayoutMode.FREE
        self.spacing = 5.0
        self.padding = 10.0
        self.grid_columns = 3
        self._current_row = 0
        self._current_col = 0
        logger.debug("Initialized LayoutManager")

    def set_mode(self, mode: LayoutMode) -> None:
        """Set the layout mode."""
        self.mode = mode
        self._current_row = 0
        self._current_col = 0
        logger.debug(f"Set layout mode to {mode.value}")

    def set_spacing(self, spacing: float) -> None:
        """Set spacing between widgets."""
        self.spacing = spacing

    def set_padding(self, padding: float) -> None:
        """Set padding around widgets."""
        self.padding = padding

    def set_grid_columns(self, columns: int) -> None:
        """Set number of columns for grid layout."""
        self.grid_columns = max(1, columns)

    def begin_layout(self) -> None:
        """Begin layout section."""
        if self.mode == LayoutMode.HORIZONTAL:
            # Horizontal layout uses same_line after each widget
            pass
        elif self.mode == LayoutMode.VERTICAL:
            # Vertical layout is default ImGui behavior
            imgui.spacing()
        elif self.mode == LayoutMode.GRID:
            self._current_row = 0
            self._current_col = 0
        elif self.mode == LayoutMode.STACK:
            imgui.begin_group()

    def end_layout(self) -> None:
        """End layout section."""
        if self.mode == LayoutMode.STACK:
            imgui.end_group()

    def next_widget_position(self) -> None:
        """Position for next widget based on layout mode."""
        if self.mode == LayoutMode.HORIZONTAL:
            imgui.same_line(0, self.spacing)

        elif self.mode == LayoutMode.VERTICAL:
            imgui.dummy(imgui.ImVec2(0, self.spacing))

        elif self.mode == LayoutMode.GRID:
            self._current_col += 1
            if self._current_col >= self.grid_columns:
                self._current_col = 0
                self._current_row += 1
                imgui.dummy(imgui.ImVec2(0, self.spacing))
            else:
                imgui.same_line(0, self.spacing)

        elif self.mode == LayoutMode.FREE:
            # Free positioning - no automatic layout
            pass

    def add_spacing(self, count: int = 1) -> None:
        """Add vertical spacing."""
        for _ in range(count):
            imgui.spacing()

    def add_separator(self, vertical: bool = False) -> None:
        """Add a separator line."""
        if vertical:
            imgui.separator_text("")
        else:
            imgui.separator()

    def add_newline(self) -> None:
        """Force a new line."""
        imgui.new_line()

    def same_line(self, offset: float = 0.0, spacing: float = -1.0) -> None:
        """Place next item on same line."""
        imgui.same_line(offset, spacing if spacing >= 0 else self.spacing)

    def indent(self, width: float = 0.0) -> None:
        """Add indentation."""
        imgui.indent(width)

    def unindent(self, width: float = 0.0) -> None:
        """Remove indentation."""
        imgui.unindent(width)

    def center_next_widget(self, widget_width: float) -> None:
        """Center the next widget horizontally."""
        region_width = imgui.get_content_region_avail().x
        cursor_pos = (region_width - widget_width) * 0.5
        imgui.set_cursor_pos_x(imgui.get_cursor_pos_x() + cursor_pos)

    def align_text_to_frame_padding(self) -> None:
        """Align text baseline to frame padding."""
        imgui.align_text_to_frame_padding()

    def get_cursor_pos(self) -> tuple[float, float]:
        """Get current cursor position."""
        pos = imgui.get_cursor_pos()
        return (pos.x, pos.y)

    def set_cursor_pos(self, x: float, y: float) -> None:
        """Set cursor position."""
        imgui.set_cursor_pos(imgui.ImVec2(x, y))

    def get_content_region_avail(self) -> tuple[float, float]:
        """Get available content region size."""
        region = imgui.get_content_region_avail()
        return (region.x, region.y)

    def push_item_width(self, width: float) -> None:
        """Push item width onto stack."""
        imgui.push_item_width(width)

    def pop_item_width(self) -> None:
        """Pop item width from stack."""
        imgui.pop_item_width()

    def set_next_item_width(self, width: float) -> None:
        """Set width for next item only."""
        imgui.set_next_item_width(width)

    def calc_item_width(self) -> float:
        """Calculate default item width."""
        return imgui.calc_item_width()


class AutoLayout:
    """Context manager for automatic layout."""

    def __init__(self, manager: LayoutManager, mode: LayoutMode):
        """Initialize auto layout."""
        self.manager = manager
        self.mode = mode
        self.previous_mode = manager.mode

    def __enter__(self):
        """Enter layout context."""
        self.manager.set_mode(self.mode)
        self.manager.begin_layout()
        return self.manager

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit layout context."""
        self.manager.end_layout()
        self.manager.set_mode(self.previous_mode)
