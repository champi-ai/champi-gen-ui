"""Main FastMCP server implementation."""

from typing import Any

from fastmcp import FastMCP
from loguru import logger

from champi_gen_ui.core.binding import BindingManager, DataStore, ValidationManager
from champi_gen_ui.core.canvas import CanvasManager
from champi_gen_ui.core.codegen import (
    CodeGenerator,
    TemplateCodeGenerator,
)
from champi_gen_ui.core.serialization import (
    TemplateManager,
    UIExporter,
    UIImporter,
)
from champi_gen_ui.core.state import CanvasMode
from champi_gen_ui.extensions.animation import (
    AnimationManager,
    EasingFunction,
)
from champi_gen_ui.extensions.file_dialog import (
    FileDialogWidget,
    MessageDialog,
)
from champi_gen_ui.extensions.notification import (
    NotificationManager,
    NotificationType,
)
from champi_gen_ui.layout.manager import LayoutManager, LayoutMode
from champi_gen_ui.themes.manager import ThemeManager
from champi_gen_ui.themes.presets import THEME_PRESETS
from champi_gen_ui.widgets.basic import (
    ButtonWidget,
    CheckboxWidget,
    ColorPickerWidget,
    ComboWidget,
    InputTextWidget,
    ListBoxWidget,
    RadioButtonWidget,
    TextWidget,
)
from champi_gen_ui.widgets.container import (
    CollapsingHeaderWidget,
    SeparatorWidget,
    WindowWidget,
)
from champi_gen_ui.widgets.display import (
    BulletTextWidget,
    HelpMarkerWidget,
    PlotLinesWidget,
    TextColoredWidget,
)
from champi_gen_ui.widgets.display import (
    ProgressBarWidget as DisplayProgressBarWidget,
)
from champi_gen_ui.widgets.menu import (
    MenuBarWidget,
    MenuItemWidget,
    MenuWidget,
    SelectableWidget,
    TreeNodeWidget,
)
from champi_gen_ui.widgets.plotting import (
    BarChartWidget,
    HeatmapWidget,
    LineChartWidget,
    PieChartWidget,
    ScatterPlotWidget,
)
from champi_gen_ui.widgets.slider import (
    DragFloatWidget,
    DragIntWidget,
    ProgressBarWidget,
    SliderFloatWidget,
    SliderIntWidget,
)

# Initialize FastMCP server
mcp = FastMCP("champi-gen-ui", dependencies=["imgui-bundle", "pyglm"])

# Global managers
canvas_manager = CanvasManager()
theme_manager = ThemeManager()
layout_manager = LayoutManager()
notification_manager = NotificationManager()
animation_manager = AnimationManager()
data_store = DataStore()
binding_manager = BindingManager(data_store)
validation_manager = ValidationManager()
template_manager = TemplateManager()

# Initialize theme presets
for _name, theme in THEME_PRESETS.items():
    theme_manager.register_theme(theme)


# Register widget types
def register_widgets():
    """Register all widget types with factories."""
    for canvas in canvas_manager.canvases.values():
        registry = canvas.widget_registry
        registry.factory.register("button", ButtonWidget)
        registry.factory.register("text", TextWidget)
        registry.factory.register("input_text", InputTextWidget)
        registry.factory.register("checkbox", CheckboxWidget)
        registry.factory.register("radio_button", RadioButtonWidget)
        registry.factory.register("combo", ComboWidget)
        registry.factory.register("list_box", ListBoxWidget)
        registry.factory.register("color_picker", ColorPickerWidget)
        registry.factory.register("slider_int", SliderIntWidget)
        registry.factory.register("slider_float", SliderFloatWidget)
        registry.factory.register("drag_int", DragIntWidget)
        registry.factory.register("drag_float", DragFloatWidget)
        registry.factory.register("progress_bar", ProgressBarWidget)


# Canvas Management Tools


@mcp.tool()
def create_canvas(
    canvas_id: str,
    width: int = 1280,
    height: int = 720,
    mode: str = "standard",
    title: str = "ImGui Canvas",
) -> dict[str, Any]:
    """
    Create a new canvas for rendering ImGui UI.

    Args:
        canvas_id: Unique identifier for the canvas
        width: Canvas width in pixels
        height: Canvas height in pixels
        mode: Rendering mode (standard, docking, multi_viewport, fullscreen, overlay)
        title: Window title

    Returns:
        Canvas state dictionary
    """
    try:
        canvas_mode = CanvasMode(mode)
        canvas = canvas_manager.create_canvas(
            canvas_id=canvas_id,
            width=width,
            height=height,
            mode=canvas_mode,
            title=title,
        )
        register_widgets()
        logger.info(f"Created canvas: {canvas_id}")
        return {"success": True, "data": canvas.serialize()}
    except Exception as e:
        logger.error(f"Error creating canvas: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def get_canvas_state(canvas_id: str) -> dict[str, Any]:
    """
    Get the current state of a canvas.

    Args:
        canvas_id: Canvas identifier

    Returns:
        Canvas state dictionary
    """
    try:
        canvas = canvas_manager.get_canvas(canvas_id)
        if not canvas:
            return {"success": False, "error": f"Canvas {canvas_id} not found"}
        return {"success": True, "data": canvas.serialize()}
    except Exception as e:
        logger.error(f"Error getting canvas state: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def clear_canvas(canvas_id: str) -> dict[str, Any]:
    """
    Clear all widgets from a canvas.

    Args:
        canvas_id: Canvas identifier

    Returns:
        Success status
    """
    try:
        canvas = canvas_manager.get_canvas(canvas_id)
        if not canvas:
            return {"success": False, "error": f"Canvas {canvas_id} not found"}
        canvas.clear()
        return {"success": True, "data": {"message": f"Canvas {canvas_id} cleared"}}
    except Exception as e:
        logger.error(f"Error clearing canvas: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def list_canvases() -> dict[str, Any]:
    """
    List all available canvases.

    Returns:
        List of canvas IDs
    """
    try:
        canvases = canvas_manager.list_canvases()
        return {"success": True, "data": {"canvases": canvases}}
    except Exception as e:
        logger.error(f"Error listing canvases: {e}")
        return {"success": False, "error": str(e)}


# Widget Management Tools


@mcp.tool()
def add_button(
    canvas_id: str,
    widget_id: str,
    label: str = "Button",
    position: list[float] | None = None,
    size: list[float] | None = None,
) -> dict[str, Any]:
    """
    Add a button widget to the canvas.

    Args:
        canvas_id: Canvas identifier
        widget_id: Unique widget identifier
        label: Button text
        position: [x, y] position
        size: [width, height] size

    Returns:
        Widget state dictionary
    """
    try:
        canvas = canvas_manager.get_canvas(canvas_id)
        if not canvas:
            return {"success": False, "error": f"Canvas {canvas_id} not found"}

        widget = canvas.widget_registry.factory.create(
            "button", widget_id, label=label, size=size
        )
        if position:
            widget.set_position(*position)
        canvas.add_widget(widget)

        return {"success": True, "data": widget.serialize()}
    except Exception as e:
        logger.error(f"Error adding button: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def add_text(
    canvas_id: str,
    widget_id: str,
    text: str = "",
    color: list[float] | None = None,
    wrapped: bool = False,
    position: list[float] | None = None,
) -> dict[str, Any]:
    """
    Add a text widget to the canvas.

    Args:
        canvas_id: Canvas identifier
        widget_id: Unique widget identifier
        text: Text content
        color: [R, G, B, A] color values (0-1)
        wrapped: Enable text wrapping
        position: [x, y] position

    Returns:
        Widget state dictionary
    """
    try:
        canvas = canvas_manager.get_canvas(canvas_id)
        if not canvas:
            return {"success": False, "error": f"Canvas {canvas_id} not found"}

        widget = canvas.widget_registry.factory.create(
            "text", widget_id, text=text, color=color, wrapped=wrapped
        )
        if position:
            widget.set_position(*position)
        canvas.add_widget(widget)

        return {"success": True, "data": widget.serialize()}
    except Exception as e:
        logger.error(f"Error adding text: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def add_input_text(
    canvas_id: str,
    widget_id: str,
    label: str = "Input",
    value: str = "",
    hint: str | None = None,
    multiline: bool = False,
    position: list[float] | None = None,
) -> dict[str, Any]:
    """
    Add an input text widget to the canvas.

    Args:
        canvas_id: Canvas identifier
        widget_id: Unique widget identifier
        label: Input label
        value: Initial value
        hint: Placeholder hint text
        multiline: Enable multiline input
        position: [x, y] position

    Returns:
        Widget state dictionary
    """
    try:
        canvas = canvas_manager.get_canvas(canvas_id)
        if not canvas:
            return {"success": False, "error": f"Canvas {canvas_id} not found"}

        widget = canvas.widget_registry.factory.create(
            "input_text",
            widget_id,
            label=label,
            value=value,
            hint=hint,
            multiline=multiline,
        )
        if position:
            widget.set_position(*position)
        canvas.add_widget(widget)

        return {"success": True, "data": widget.serialize()}
    except Exception as e:
        logger.error(f"Error adding input text: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def add_checkbox(
    canvas_id: str,
    widget_id: str,
    label: str = "Checkbox",
    checked: bool = False,
    position: list[float] | None = None,
) -> dict[str, Any]:
    """
    Add a checkbox widget to the canvas.

    Args:
        canvas_id: Canvas identifier
        widget_id: Unique widget identifier
        label: Checkbox label
        checked: Initial checked state
        position: [x, y] position

    Returns:
        Widget state dictionary
    """
    try:
        canvas = canvas_manager.get_canvas(canvas_id)
        if not canvas:
            return {"success": False, "error": f"Canvas {canvas_id} not found"}

        widget = canvas.widget_registry.factory.create(
            "checkbox", widget_id, label=label, checked=checked
        )
        if position:
            widget.set_position(*position)
        canvas.add_widget(widget)

        return {"success": True, "data": widget.serialize()}
    except Exception as e:
        logger.error(f"Error adding checkbox: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def add_slider_float(
    canvas_id: str,
    widget_id: str,
    label: str = "Slider",
    value: float = 0.0,
    v_min: float = 0.0,
    v_max: float = 1.0,
    position: list[float] | None = None,
) -> dict[str, Any]:
    """
    Add a float slider widget to the canvas.

    Args:
        canvas_id: Canvas identifier
        widget_id: Unique widget identifier
        label: Slider label
        value: Initial value
        v_min: Minimum value
        v_max: Maximum value
        position: [x, y] position

    Returns:
        Widget state dictionary
    """
    try:
        canvas = canvas_manager.get_canvas(canvas_id)
        if not canvas:
            return {"success": False, "error": f"Canvas {canvas_id} not found"}

        widget = canvas.widget_registry.factory.create(
            "slider_float",
            widget_id,
            label=label,
            value=value,
            v_min=v_min,
            v_max=v_max,
        )
        if position:
            widget.set_position(*position)
        canvas.add_widget(widget)

        return {"success": True, "data": widget.serialize()}
    except Exception as e:
        logger.error(f"Error adding slider: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def add_slider_int(
    canvas_id: str,
    widget_id: str,
    label: str = "Slider",
    value: int = 0,
    v_min: int = 0,
    v_max: int = 100,
    position: list[float] | None = None,
) -> dict[str, Any]:
    """
    Add an integer slider widget to the canvas.

    Args:
        canvas_id: Canvas identifier
        widget_id: Unique widget identifier
        label: Slider label
        value: Initial value
        v_min: Minimum value
        v_max: Maximum value
        position: [x, y] position

    Returns:
        Widget state dictionary
    """
    try:
        canvas = canvas_manager.get_canvas(canvas_id)
        if not canvas:
            return {"success": False, "error": f"Canvas {canvas_id} not found"}

        widget = canvas.widget_registry.factory.create(
            "slider_int",
            widget_id,
            label=label,
            value=value,
            v_min=v_min,
            v_max=v_max,
        )
        if position:
            widget.set_position(*position)
        canvas.add_widget(widget)

        return {"success": True, "data": widget.serialize()}
    except Exception as e:
        logger.error(f"Error adding slider: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def add_color_picker(
    canvas_id: str,
    widget_id: str,
    label: str = "Color",
    color: list[float] | None = None,
    position: list[float] | None = None,
) -> dict[str, Any]:
    """
    Add a color picker widget to the canvas.

    Args:
        canvas_id: Canvas identifier
        widget_id: Unique widget identifier
        label: Picker label
        color: [R, G, B, A] initial color (0-1)
        position: [x, y] position

    Returns:
        Widget state dictionary
    """
    try:
        canvas = canvas_manager.get_canvas(canvas_id)
        if not canvas:
            return {"success": False, "error": f"Canvas {canvas_id} not found"}

        initial_color = color or [1.0, 1.0, 1.0, 1.0]
        widget = canvas.widget_registry.factory.create(
            "color_picker", widget_id, label=label, color=tuple(initial_color)
        )
        if position:
            widget.set_position(*position)
        canvas.add_widget(widget)

        return {"success": True, "data": widget.serialize()}
    except Exception as e:
        logger.error(f"Error adding color picker: {e}")
        return {"success": False, "error": str(e)}


# Theme Management Tools


@mcp.tool()
def apply_theme(theme_name: str) -> dict[str, Any]:
    """
    Apply a theme to ImGui.

    Args:
        theme_name: Theme name (dark, light, cherry, nord, dracula, gruvbox, solarized_dark, monokai, material)

    Returns:
        Success status
    """
    try:
        theme_manager.apply_theme_by_name(theme_name)
        return {"success": True, "data": {"message": f"Applied theme: {theme_name}"}}
    except Exception as e:
        logger.error(f"Error applying theme: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def list_themes() -> dict[str, Any]:
    """
    List all available themes.

    Returns:
        List of theme names
    """
    try:
        themes = theme_manager.list_themes()
        return {"success": True, "data": {"themes": themes}}
    except Exception as e:
        logger.error(f"Error listing themes: {e}")
        return {"success": False, "error": str(e)}


# Layout Management Tools


@mcp.tool()
def set_layout_mode(mode: str) -> dict[str, Any]:
    """
    Set the layout mode.

    Args:
        mode: Layout mode (horizontal, vertical, grid, stack, free)

    Returns:
        Success status
    """
    try:
        layout_mode = LayoutMode(mode)
        layout_manager.set_mode(layout_mode)
        return {"success": True, "data": {"message": f"Set layout mode: {mode}"}}
    except Exception as e:
        logger.error(f"Error setting layout mode: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def set_layout_spacing(spacing: float) -> dict[str, Any]:
    """
    Set spacing between widgets.

    Args:
        spacing: Spacing value in pixels

    Returns:
        Success status
    """
    try:
        layout_manager.set_spacing(spacing)
        return {"success": True, "data": {"message": f"Set spacing: {spacing}"}}
    except Exception as e:
        logger.error(f"Error setting spacing: {e}")
        return {"success": False, "error": str(e)}


# Additional Widget Tools


@mcp.tool()
def add_window(
    canvas_id: str,
    widget_id: str,
    title: str = "Window",
    closable: bool = True,
    position: list[float] | None = None,
) -> dict[str, Any]:
    """
    Add a window container widget.

    Args:
        canvas_id: Canvas identifier
        widget_id: Unique widget identifier
        title: Window title
        closable: Allow window to be closed
        position: [x, y] position

    Returns:
        Widget state dictionary
    """
    try:
        canvas = canvas_manager.get_canvas(canvas_id)
        if not canvas:
            return {"success": False, "error": f"Canvas {canvas_id} not found"}

        widget = WindowWidget(widget_id, title=title, closable=closable)
        if position:
            widget.set_position(*position)
        canvas.add_widget(widget)

        return {"success": True, "data": widget.serialize()}
    except Exception as e:
        logger.error(f"Error adding window: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def add_menu_bar(
    canvas_id: str,
    widget_id: str,
) -> dict[str, Any]:
    """
    Add a menu bar widget.

    Args:
        canvas_id: Canvas identifier
        widget_id: Unique widget identifier

    Returns:
        Widget state dictionary
    """
    try:
        canvas = canvas_manager.get_canvas(canvas_id)
        if not canvas:
            return {"success": False, "error": f"Canvas {canvas_id} not found"}

        widget = MenuBarWidget(widget_id)
        canvas.add_widget(widget)

        return {"success": True, "data": widget.serialize()}
    except Exception as e:
        logger.error(f"Error adding menu bar: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def add_menu(
    canvas_id: str,
    widget_id: str,
    label: str = "Menu",
    enabled: bool = True,
) -> dict[str, Any]:
    """
    Add a menu widget.

    Args:
        canvas_id: Canvas identifier
        widget_id: Unique widget identifier
        label: Menu label
        enabled: Enable/disable menu

    Returns:
        Widget state dictionary
    """
    try:
        canvas = canvas_manager.get_canvas(canvas_id)
        if not canvas:
            return {"success": False, "error": f"Canvas {canvas_id} not found"}

        widget = MenuWidget(widget_id, label=label, enabled=enabled)
        canvas.add_widget(widget)

        return {"success": True, "data": widget.serialize()}
    except Exception as e:
        logger.error(f"Error adding menu: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def add_menu_item(
    canvas_id: str,
    widget_id: str,
    label: str = "Item",
    shortcut: str | None = None,
    selected: bool = False,
) -> dict[str, Any]:
    """
    Add a menu item widget.

    Args:
        canvas_id: Canvas identifier
        widget_id: Unique widget identifier
        label: Item label
        shortcut: Keyboard shortcut text
        selected: Initial selected state

    Returns:
        Widget state dictionary
    """
    try:
        canvas = canvas_manager.get_canvas(canvas_id)
        if not canvas:
            return {"success": False, "error": f"Canvas {canvas_id} not found"}

        widget = MenuItemWidget(
            widget_id, label=label, shortcut=shortcut, selected=selected
        )
        canvas.add_widget(widget)

        return {"success": True, "data": widget.serialize()}
    except Exception as e:
        logger.error(f"Error adding menu item: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def add_separator(
    canvas_id: str,
    widget_id: str,
    vertical: bool = False,
) -> dict[str, Any]:
    """
    Add a separator widget.

    Args:
        canvas_id: Canvas identifier
        widget_id: Unique widget identifier
        vertical: Vertical separator

    Returns:
        Widget state dictionary
    """
    try:
        canvas = canvas_manager.get_canvas(canvas_id)
        if not canvas:
            return {"success": False, "error": f"Canvas {canvas_id} not found"}

        widget = SeparatorWidget(widget_id, vertical=vertical)
        canvas.add_widget(widget)

        return {"success": True, "data": widget.serialize()}
    except Exception as e:
        logger.error(f"Error adding separator: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def add_collapsing_header(
    canvas_id: str,
    widget_id: str,
    label: str = "Header",
    default_open: bool = False,
) -> dict[str, Any]:
    """
    Add a collapsing header widget.

    Args:
        canvas_id: Canvas identifier
        widget_id: Unique widget identifier
        label: Header label
        default_open: Start in open state

    Returns:
        Widget state dictionary
    """
    try:
        canvas = canvas_manager.get_canvas(canvas_id)
        if not canvas:
            return {"success": False, "error": f"Canvas {canvas_id} not found"}

        widget = CollapsingHeaderWidget(
            widget_id, label=label, default_open=default_open
        )
        canvas.add_widget(widget)

        return {"success": True, "data": widget.serialize()}
    except Exception as e:
        logger.error(f"Error adding collapsing header: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def add_tree_node(
    canvas_id: str,
    widget_id: str,
    label: str = "Node",
    default_open: bool = False,
) -> dict[str, Any]:
    """
    Add a tree node widget.

    Args:
        canvas_id: Canvas identifier
        widget_id: Unique widget identifier
        label: Node label
        default_open: Start in open state

    Returns:
        Widget state dictionary
    """
    try:
        canvas = canvas_manager.get_canvas(canvas_id)
        if not canvas:
            return {"success": False, "error": f"Canvas {canvas_id} not found"}

        widget = TreeNodeWidget(widget_id, label=label, default_open=default_open)
        canvas.add_widget(widget)

        return {"success": True, "data": widget.serialize()}
    except Exception as e:
        logger.error(f"Error adding tree node: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def add_selectable(
    canvas_id: str,
    widget_id: str,
    label: str = "Selectable",
    selected: bool = False,
) -> dict[str, Any]:
    """
    Add a selectable widget.

    Args:
        canvas_id: Canvas identifier
        widget_id: Unique widget identifier
        label: Selectable label
        selected: Initial selected state

    Returns:
        Widget state dictionary
    """
    try:
        canvas = canvas_manager.get_canvas(canvas_id)
        if not canvas:
            return {"success": False, "error": f"Canvas {canvas_id} not found"}

        widget = SelectableWidget(widget_id, label=label, selected=selected)
        canvas.add_widget(widget)

        return {"success": True, "data": widget.serialize()}
    except Exception as e:
        logger.error(f"Error adding selectable: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def add_progress_bar(
    canvas_id: str,
    widget_id: str,
    fraction: float = 0.0,
    overlay: str | None = None,
) -> dict[str, Any]:
    """
    Add a progress bar widget.

    Args:
        canvas_id: Canvas identifier
        widget_id: Unique widget identifier
        fraction: Progress value (0.0 to 1.0)
        overlay: Overlay text

    Returns:
        Widget state dictionary
    """
    try:
        canvas = canvas_manager.get_canvas(canvas_id)
        if not canvas:
            return {"success": False, "error": f"Canvas {canvas_id} not found"}

        widget = DisplayProgressBarWidget(widget_id, fraction=fraction, overlay=overlay)
        canvas.add_widget(widget)

        return {"success": True, "data": widget.serialize()}
    except Exception as e:
        logger.error(f"Error adding progress bar: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def add_plot_lines(
    canvas_id: str,
    widget_id: str,
    label: str = "Plot",
    values: list[float] | None = None,
) -> dict[str, Any]:
    """
    Add a line plot widget.

    Args:
        canvas_id: Canvas identifier
        widget_id: Unique widget identifier
        label: Plot label
        values: List of data values

    Returns:
        Widget state dictionary
    """
    try:
        canvas = canvas_manager.get_canvas(canvas_id)
        if not canvas:
            return {"success": False, "error": f"Canvas {canvas_id} not found"}

        widget = PlotLinesWidget(widget_id, label=label, values=values or [])
        canvas.add_widget(widget)

        return {"success": True, "data": widget.serialize()}
    except Exception as e:
        logger.error(f"Error adding plot lines: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def add_colored_text(
    canvas_id: str,
    widget_id: str,
    text: str = "",
    color: list[float] | None = None,
) -> dict[str, Any]:
    """
    Add a colored text widget.

    Args:
        canvas_id: Canvas identifier
        widget_id: Unique widget identifier
        text: Text content
        color: [R, G, B, A] color (0-1)

    Returns:
        Widget state dictionary
    """
    try:
        canvas = canvas_manager.get_canvas(canvas_id)
        if not canvas:
            return {"success": False, "error": f"Canvas {canvas_id} not found"}

        color_tuple = tuple(color) if color else (1.0, 1.0, 1.0, 1.0)
        widget = TextColoredWidget(widget_id, text=text, color=color_tuple)
        canvas.add_widget(widget)

        return {"success": True, "data": widget.serialize()}
    except Exception as e:
        logger.error(f"Error adding colored text: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def add_bullet_text(
    canvas_id: str,
    widget_id: str,
    text: str = "",
) -> dict[str, Any]:
    """
    Add a bullet text widget.

    Args:
        canvas_id: Canvas identifier
        widget_id: Unique widget identifier
        text: Text content

    Returns:
        Widget state dictionary
    """
    try:
        canvas = canvas_manager.get_canvas(canvas_id)
        if not canvas:
            return {"success": False, "error": f"Canvas {canvas_id} not found"}

        widget = BulletTextWidget(widget_id, text=text)
        canvas.add_widget(widget)

        return {"success": True, "data": widget.serialize()}
    except Exception as e:
        logger.error(f"Error adding bullet text: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def add_help_marker(
    canvas_id: str,
    widget_id: str,
    text: str = "",
    marker: str = "(?)",
) -> dict[str, Any]:
    """
    Add a help marker widget with tooltip.

    Args:
        canvas_id: Canvas identifier
        widget_id: Unique widget identifier
        text: Tooltip text
        marker: Marker text

    Returns:
        Widget state dictionary
    """
    try:
        canvas = canvas_manager.get_canvas(canvas_id)
        if not canvas:
            return {"success": False, "error": f"Canvas {canvas_id} not found"}

        widget = HelpMarkerWidget(widget_id, text=text, marker=marker)
        canvas.add_widget(widget)

        return {"success": True, "data": widget.serialize()}
    except Exception as e:
        logger.error(f"Error adding help marker: {e}")
        return {"success": False, "error": str(e)}


# Extension Tools - File Dialogs


@mcp.tool()
def add_file_dialog(
    canvas_id: str,
    widget_id: str,
    button_label: str = "Browse...",
    mode: str = "open_file",
    title: str = "Select File",
    filters: list[str] | None = None,
) -> dict[str, Any]:
    """
    Add a file dialog widget.

    Args:
        canvas_id: Canvas identifier
        widget_id: Unique widget identifier
        button_label: Browse button label
        mode: Dialog mode (open_file, open_folder, save_file)
        title: Dialog title
        filters: File filters (e.g., ["*.txt", "*.py"])

    Returns:
        Widget state dictionary
    """
    try:
        canvas = canvas_manager.get_canvas(canvas_id)
        if not canvas:
            return {"success": False, "error": f"Canvas {canvas_id} not found"}

        widget = FileDialogWidget(
            widget_id,
            button_label=button_label,
            mode=mode,
            title=title,
            filters=filters or [],
        )
        canvas.add_widget(widget)

        return {"success": True, "data": widget.serialize()}
    except Exception as e:
        logger.error(f"Error adding file dialog: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def show_message_dialog(
    title: str,
    message: str,
    type: str = "info",
) -> dict[str, Any]:
    """
    Show a message dialog.

    Args:
        title: Dialog title
        message: Dialog message
        type: Message type (info, warning, error)

    Returns:
        Success status
    """
    try:
        if type == "info":
            MessageDialog.info(title, message)
        elif type == "warning":
            MessageDialog.warning(title, message)
        elif type == "error":
            MessageDialog.error(title, message)
        else:
            MessageDialog.info(title, message)

        return {"success": True, "data": {"message": "Dialog shown"}}
    except Exception as e:
        logger.error(f"Error showing message dialog: {e}")
        return {"success": False, "error": str(e)}


# Extension Tools - Notifications


@mcp.tool()
def show_notification(
    title: str,
    message: str,
    type: str = "info",
    duration: float = 3.0,
) -> dict[str, Any]:
    """
    Show a toast notification.

    Args:
        title: Notification title
        message: Notification message
        type: Notification type (info, success, warning, error)
        duration: Display duration in seconds

    Returns:
        Success status
    """
    try:
        notification_type = NotificationType(type)
        notification_manager.add(title, message, notification_type, duration)
        return {"success": True, "data": {"message": "Notification added"}}
    except Exception as e:
        logger.error(f"Error showing notification: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def clear_notifications() -> dict[str, Any]:
    """
    Clear all notifications.

    Returns:
        Success status
    """
    try:
        notification_manager.clear_all()
        return {"success": True, "data": {"message": "Notifications cleared"}}
    except Exception as e:
        logger.error(f"Error clearing notifications: {e}")
        return {"success": False, "error": str(e)}


# Extension Tools - Animations


@mcp.tool()
def create_animation(
    name: str,
    start_value: float,
    end_value: float,
    duration: float,
    easing: str = "linear",
    loop: bool = False,
) -> dict[str, Any]:
    """
    Create an animation.

    Args:
        name: Unique animation name
        start_value: Starting value
        end_value: Ending value
        duration: Duration in seconds
        easing: Easing function (linear, ease_in_quad, ease_out_quad, etc.)
        loop: Loop the animation

    Returns:
        Success status
    """
    try:
        easing_func = EasingFunction(easing)
        animation_manager.create(
            name=name,
            start_value=start_value,
            end_value=end_value,
            duration=duration,
            easing=easing_func,
            loop=loop,
        )
        return {"success": True, "data": {"message": f"Animation created: {name}"}}
    except Exception as e:
        logger.error(f"Error creating animation: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def start_animation(name: str) -> dict[str, Any]:
    """
    Start an animation.

    Args:
        name: Animation name

    Returns:
        Success status
    """
    try:
        result = animation_manager.start(name)
        if result:
            return {"success": True, "data": {"message": f"Animation started: {name}"}}
        return {"success": False, "error": f"Animation not found: {name}"}
    except Exception as e:
        logger.error(f"Error starting animation: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def stop_animation(name: str) -> dict[str, Any]:
    """
    Stop an animation.

    Args:
        name: Animation name

    Returns:
        Success status
    """
    try:
        result = animation_manager.stop(name)
        if result:
            return {"success": True, "data": {"message": f"Animation stopped: {name}"}}
        return {"success": False, "error": f"Animation not found: {name}"}
    except Exception as e:
        logger.error(f"Error stopping animation: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def get_animation_value(name: str) -> dict[str, Any]:
    """
    Get current animation value.

    Args:
        name: Animation name

    Returns:
        Animation value
    """
    try:
        value = animation_manager.get_value(name)
        if value is not None:
            return {"success": True, "data": {"value": value}}
        return {"success": False, "error": f"Animation not found: {name}"}
    except Exception as e:
        logger.error(f"Error getting animation value: {e}")
        return {"success": False, "error": str(e)}


# Data Binding Tools


@mcp.tool()
def set_data(path: str, value: Any) -> dict[str, Any]:
    """
    Set a value in the data store.

    Args:
        path: Data path (e.g., "user.name")
        value: Value to set

    Returns:
        Success status
    """
    try:
        data_store.set(path, value)
        return {"success": True, "data": {"message": f"Set {path}"}}
    except Exception as e:
        logger.error(f"Error setting data: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def get_data(path: str, default: Any = None) -> dict[str, Any]:
    """
    Get a value from the data store.

    Args:
        path: Data path
        default: Default value if not found

    Returns:
        Data value
    """
    try:
        value = data_store.get(path, default)
        return {"success": True, "data": {"value": value}}
    except Exception as e:
        logger.error(f"Error getting data: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def bind_data(
    source_path: str,
    target_widget: str,
    target_property: str,
    bidirectional: bool = False,
) -> dict[str, Any]:
    """
    Create a data binding between store and widget.

    Args:
        source_path: Path in data store
        target_widget: Widget ID
        target_property: Widget property to bind
        bidirectional: Enable two-way binding

    Returns:
        Success status
    """
    try:
        binding_manager.bind(
            source_path, target_widget, target_property, bidirectional=bidirectional
        )
        return {
            "success": True,
            "data": {
                "message": f"Bound {source_path} to {target_widget}.{target_property}"
            },
        }
    except Exception as e:
        logger.error(f"Error binding data: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def unbind_data(source_path: str, target_widget: str | None = None) -> dict[str, Any]:
    """
    Remove data bindings.

    Args:
        source_path: Data path
        target_widget: Optional widget ID (removes all if None)

    Returns:
        Success status
    """
    try:
        binding_manager.unbind(source_path, target_widget)
        return {"success": True, "data": {"message": f"Unbound {source_path}"}}
    except Exception as e:
        logger.error(f"Error unbinding data: {e}")
        return {"success": False, "error": str(e)}


# Plotting Tools


@mcp.tool()
def add_line_chart(
    canvas_id: str,
    widget_id: str,
    title: str = "Line Chart",
    x_data: list[float] | None = None,
    y_data: list[float] | None = None,
) -> dict[str, Any]:
    """
    Add a line chart widget.

    Args:
        canvas_id: Canvas identifier
        widget_id: Unique widget identifier
        title: Chart title
        x_data: X-axis data
        y_data: Y-axis data

    Returns:
        Widget state dictionary
    """
    try:
        canvas = canvas_manager.get_canvas(canvas_id)
        if not canvas:
            return {"success": False, "error": f"Canvas {canvas_id} not found"}

        widget = LineChartWidget(
            widget_id, title=title, x_data=x_data or [], y_data=y_data or []
        )
        canvas.add_widget(widget)

        return {"success": True, "data": widget.serialize()}
    except Exception as e:
        logger.error(f"Error adding line chart: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def add_bar_chart(
    canvas_id: str,
    widget_id: str,
    title: str = "Bar Chart",
    values: list[float] | None = None,
    labels: list[str] | None = None,
) -> dict[str, Any]:
    """
    Add a bar chart widget.

    Args:
        canvas_id: Canvas identifier
        widget_id: Unique widget identifier
        title: Chart title
        values: Bar values
        labels: Bar labels

    Returns:
        Widget state dictionary
    """
    try:
        canvas = canvas_manager.get_canvas(canvas_id)
        if not canvas:
            return {"success": False, "error": f"Canvas {canvas_id} not found"}

        widget = BarChartWidget(
            widget_id, title=title, values=values or [], labels=labels or []
        )
        canvas.add_widget(widget)

        return {"success": True, "data": widget.serialize()}
    except Exception as e:
        logger.error(f"Error adding bar chart: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def add_scatter_plot(
    canvas_id: str,
    widget_id: str,
    title: str = "Scatter Plot",
    x_data: list[float] | None = None,
    y_data: list[float] | None = None,
) -> dict[str, Any]:
    """
    Add a scatter plot widget.

    Args:
        canvas_id: Canvas identifier
        widget_id: Unique widget identifier
        title: Plot title
        x_data: X-axis data
        y_data: Y-axis data

    Returns:
        Widget state dictionary
    """
    try:
        canvas = canvas_manager.get_canvas(canvas_id)
        if not canvas:
            return {"success": False, "error": f"Canvas {canvas_id} not found"}

        widget = ScatterPlotWidget(
            widget_id, title=title, x_data=x_data or [], y_data=y_data or []
        )
        canvas.add_widget(widget)

        return {"success": True, "data": widget.serialize()}
    except Exception as e:
        logger.error(f"Error adding scatter plot: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def add_pie_chart(
    canvas_id: str,
    widget_id: str,
    values: list[float] | None = None,
    labels: list[str] | None = None,
) -> dict[str, Any]:
    """
    Add a pie chart widget.

    Args:
        canvas_id: Canvas identifier
        widget_id: Unique widget identifier
        values: Slice values
        labels: Slice labels

    Returns:
        Widget state dictionary
    """
    try:
        canvas = canvas_manager.get_canvas(canvas_id)
        if not canvas:
            return {"success": False, "error": f"Canvas {canvas_id} not found"}

        widget = PieChartWidget(widget_id, values=values or [], labels=labels or [])
        canvas.add_widget(widget)

        return {"success": True, "data": widget.serialize()}
    except Exception as e:
        logger.error(f"Error adding pie chart: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def add_heatmap(
    canvas_id: str,
    widget_id: str,
    title: str = "Heatmap",
    values: list[list[float]] | None = None,
) -> dict[str, Any]:
    """
    Add a heatmap widget.

    Args:
        canvas_id: Canvas identifier
        widget_id: Unique widget identifier
        title: Heatmap title
        values: 2D array of values

    Returns:
        Widget state dictionary
    """
    try:
        canvas = canvas_manager.get_canvas(canvas_id)
        if not canvas:
            return {"success": False, "error": f"Canvas {canvas_id} not found"}

        widget = HeatmapWidget(widget_id, title=title, values=values or [])
        canvas.add_widget(widget)

        return {"success": True, "data": widget.serialize()}
    except Exception as e:
        logger.error(f"Error adding heatmap: {e}")
        return {"success": False, "error": str(e)}


# Serialization and Export Tools


@mcp.tool()
def export_canvas_json(canvas_id: str, filepath: str) -> dict[str, Any]:
    """
    Export canvas to JSON file.

    Args:
        canvas_id: Canvas identifier
        filepath: Output file path

    Returns:
        Success status
    """
    try:
        canvas = canvas_manager.get_canvas(canvas_id)
        if not canvas:
            return {"success": False, "error": f"Canvas {canvas_id} not found"}

        success = UIExporter.export_to_json(canvas, filepath)
        if success:
            return {"success": True, "data": {"message": f"Exported to {filepath}"}}
        return {"success": False, "error": "Export failed"}
    except Exception as e:
        logger.error(f"Error exporting canvas: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def export_canvas_python(canvas_id: str, filepath: str) -> dict[str, Any]:
    """
    Export canvas to Python code file.

    Args:
        canvas_id: Canvas identifier
        filepath: Output file path

    Returns:
        Success status
    """
    try:
        canvas = canvas_manager.get_canvas(canvas_id)
        if not canvas:
            return {"success": False, "error": f"Canvas {canvas_id} not found"}

        success = UIExporter.export_to_python(canvas, filepath)
        if success:
            return {"success": True, "data": {"message": f"Exported to {filepath}"}}
        return {"success": False, "error": "Export failed"}
    except Exception as e:
        logger.error(f"Error exporting canvas: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def import_canvas_json(filepath: str) -> dict[str, Any]:
    """
    Import canvas from JSON file.

    Args:
        filepath: Input file path

    Returns:
        Canvas data
    """
    try:
        canvas = UIImporter.import_from_json(filepath, canvas_manager)
        if canvas:
            return {"success": True, "data": canvas.serialize()}
        return {"success": False, "error": "Import failed"}
    except Exception as e:
        logger.error(f"Error importing canvas: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def get_canvas_json(canvas_id: str) -> dict[str, Any]:
    """
    Get canvas as JSON string.

    Args:
        canvas_id: Canvas identifier

    Returns:
        JSON representation
    """
    try:
        canvas = canvas_manager.get_canvas(canvas_id)
        if not canvas:
            return {"success": False, "error": f"Canvas {canvas_id} not found"}

        json_str = UIExporter.export_canvas_state(canvas)
        return {"success": True, "data": {"json": json_str}}
    except Exception as e:
        logger.error(f"Error getting canvas JSON: {e}")
        return {"success": False, "error": str(e)}


# Code Generation Tools


@mcp.tool()
def generate_canvas_code(canvas_id: str) -> dict[str, Any]:
    """
    Generate Python code for canvas.

    Args:
        canvas_id: Canvas identifier

    Returns:
        Generated code
    """
    try:
        canvas = canvas_manager.get_canvas(canvas_id)
        if not canvas:
            return {"success": False, "error": f"Canvas {canvas_id} not found"}

        code = CodeGenerator.generate_canvas_code(canvas)
        return {"success": True, "data": {"code": code}}
    except Exception as e:
        logger.error(f"Error generating code: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def generate_widget_snippet(
    widget_type: str, widget_id: str, properties: dict[str, Any] | None = None
) -> dict[str, Any]:
    """
    Generate code snippet for a widget.

    Args:
        widget_type: Widget class name
        widget_id: Widget identifier
        properties: Widget properties

    Returns:
        Code snippet
    """
    try:
        snippet = CodeGenerator.generate_widget_code_snippet(
            widget_type, widget_id, **(properties or {})
        )
        return {"success": True, "data": {"snippet": snippet}}
    except Exception as e:
        logger.error(f"Error generating snippet: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def generate_component_template(name: str, widgets: list[str]) -> dict[str, Any]:
    """
    Generate reusable component template.

    Args:
        name: Component name
        widgets: List of widget types

    Returns:
        Component code
    """
    try:
        code = TemplateCodeGenerator.generate_component_template(name, widgets)
        return {"success": True, "data": {"code": code}}
    except Exception as e:
        logger.error(f"Error generating component: {e}")
        return {"success": False, "error": str(e)}


# Template Management Tools


@mcp.tool()
def save_template(name: str, canvas_id: str, description: str = "") -> dict[str, Any]:
    """
    Save canvas as a template.

    Args:
        name: Template name
        canvas_id: Canvas identifier
        description: Template description

    Returns:
        Success status
    """
    try:
        canvas = canvas_manager.get_canvas(canvas_id)
        if not canvas:
            return {"success": False, "error": f"Canvas {canvas_id} not found"}

        success = template_manager.save_template(name, canvas, description)
        if success:
            return {"success": True, "data": {"message": f"Saved template: {name}"}}
        return {"success": False, "error": "Save failed"}
    except Exception as e:
        logger.error(f"Error saving template: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def load_template(name: str) -> dict[str, Any]:
    """
    Load a template.

    Args:
        name: Template name

    Returns:
        Canvas data
    """
    try:
        canvas = template_manager.load_template(name, canvas_manager)
        if canvas:
            return {"success": True, "data": canvas.serialize()}
        return {"success": False, "error": f"Template not found: {name}"}
    except Exception as e:
        logger.error(f"Error loading template: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def list_templates() -> dict[str, Any]:
    """
    List available templates.

    Returns:
        List of templates
    """
    try:
        templates = template_manager.list_templates()
        return {"success": True, "data": {"templates": templates}}
    except Exception as e:
        logger.error(f"Error listing templates: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def delete_template(name: str) -> dict[str, Any]:
    """
    Delete a template.

    Args:
        name: Template name

    Returns:
        Success status
    """
    try:
        success = template_manager.delete_template(name)
        if success:
            return {"success": True, "data": {"message": f"Deleted template: {name}"}}
        return {"success": False, "error": "Delete failed"}
    except Exception as e:
        logger.error(f"Error deleting template: {e}")
        return {"success": False, "error": str(e)}


def create_server() -> FastMCP:
    """Create and return the FastMCP server instance."""
    return mcp


if __name__ == "__main__":
    mcp.run()
