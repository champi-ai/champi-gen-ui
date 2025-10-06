"""Theme manager for styling and appearance."""

from dataclasses import dataclass, field
from enum import Enum

from imgui_bundle import imgui
from loguru import logger


class ColorScheme(Enum):
    """Built-in color schemes."""

    DARK = "dark"
    LIGHT = "light"
    CLASSIC = "classic"
    CHERRY = "cherry"
    CUSTOM = "custom"


@dataclass
class ThemeColors:
    """Theme color configuration."""

    # Window colors
    window_bg: tuple[float, float, float, float] = (0.1, 0.1, 0.1, 1.0)
    child_bg: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)
    popup_bg: tuple[float, float, float, float] = (0.08, 0.08, 0.08, 0.94)

    # Frame colors
    frame_bg: tuple[float, float, float, float] = (0.16, 0.16, 0.16, 1.0)
    frame_bg_hovered: tuple[float, float, float, float] = (0.26, 0.26, 0.26, 1.0)
    frame_bg_active: tuple[float, float, float, float] = (0.28, 0.28, 0.28, 1.0)

    # Title bar
    title_bg: tuple[float, float, float, float] = (0.04, 0.04, 0.04, 1.0)
    title_bg_active: tuple[float, float, float, float] = (0.16, 0.16, 0.16, 1.0)
    title_bg_collapsed: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.51)

    # Menu bar
    menu_bar_bg: tuple[float, float, float, float] = (0.14, 0.14, 0.14, 1.0)

    # Scrollbar
    scrollbar_bg: tuple[float, float, float, float] = (0.02, 0.02, 0.02, 0.53)
    scrollbar_grab: tuple[float, float, float, float] = (0.31, 0.31, 0.31, 1.0)
    scrollbar_grab_hovered: tuple[float, float, float, float] = (0.41, 0.41, 0.41, 1.0)
    scrollbar_grab_active: tuple[float, float, float, float] = (0.51, 0.51, 0.51, 1.0)

    # Check mark
    check_mark: tuple[float, float, float, float] = (0.26, 0.59, 0.98, 1.0)

    # Slider
    slider_grab: tuple[float, float, float, float] = (0.24, 0.52, 0.88, 1.0)
    slider_grab_active: tuple[float, float, float, float] = (0.26, 0.59, 0.98, 1.0)

    # Button
    button: tuple[float, float, float, float] = (0.26, 0.59, 0.98, 0.4)
    button_hovered: tuple[float, float, float, float] = (0.26, 0.59, 0.98, 1.0)
    button_active: tuple[float, float, float, float] = (0.06, 0.53, 0.98, 1.0)

    # Header
    header: tuple[float, float, float, float] = (0.26, 0.59, 0.98, 0.31)
    header_hovered: tuple[float, float, float, float] = (0.26, 0.59, 0.98, 0.8)
    header_active: tuple[float, float, float, float] = (0.26, 0.59, 0.98, 1.0)

    # Separator
    separator: tuple[float, float, float, float] = (0.43, 0.43, 0.5, 0.5)
    separator_hovered: tuple[float, float, float, float] = (0.1, 0.4, 0.75, 0.78)
    separator_active: tuple[float, float, float, float] = (0.1, 0.4, 0.75, 1.0)

    # Resize grip
    resize_grip: tuple[float, float, float, float] = (0.26, 0.59, 0.98, 0.2)
    resize_grip_hovered: tuple[float, float, float, float] = (0.26, 0.59, 0.98, 0.67)
    resize_grip_active: tuple[float, float, float, float] = (0.26, 0.59, 0.98, 0.95)

    # Tab
    tab: tuple[float, float, float, float] = (0.18, 0.35, 0.58, 0.86)
    tab_hovered: tuple[float, float, float, float] = (0.26, 0.59, 0.98, 0.8)
    tab_active: tuple[float, float, float, float] = (0.2, 0.41, 0.68, 1.0)
    tab_unfocused: tuple[float, float, float, float] = (0.07, 0.1, 0.15, 0.97)
    tab_unfocused_active: tuple[float, float, float, float] = (0.14, 0.26, 0.42, 1.0)

    # Docking
    docking_preview: tuple[float, float, float, float] = (0.26, 0.59, 0.98, 0.7)
    docking_empty_bg: tuple[float, float, float, float] = (0.2, 0.2, 0.2, 1.0)

    # Plot
    plot_lines: tuple[float, float, float, float] = (0.61, 0.61, 0.61, 1.0)
    plot_lines_hovered: tuple[float, float, float, float] = (1.0, 0.43, 0.35, 1.0)
    plot_histogram: tuple[float, float, float, float] = (0.9, 0.7, 0.0, 1.0)
    plot_histogram_hovered: tuple[float, float, float, float] = (1.0, 0.6, 0.0, 1.0)

    # Text
    text: tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0)
    text_disabled: tuple[float, float, float, float] = (0.5, 0.5, 0.5, 1.0)
    text_selected_bg: tuple[float, float, float, float] = (0.26, 0.59, 0.98, 0.35)

    # Drag drop
    drag_drop_target: tuple[float, float, float, float] = (1.0, 1.0, 0.0, 0.9)

    # Nav
    nav_highlight: tuple[float, float, float, float] = (0.26, 0.59, 0.98, 1.0)
    nav_windowing_highlight: tuple[float, float, float, float] = (1.0, 1.0, 1.0, 0.7)
    nav_windowing_dim_bg: tuple[float, float, float, float] = (0.8, 0.8, 0.8, 0.2)

    # Modal
    modal_window_dim_bg: tuple[float, float, float, float] = (0.8, 0.8, 0.8, 0.35)


@dataclass
class ThemeStyle:
    """Theme style configuration."""

    # Main
    alpha: float = 1.0
    disabled_alpha: float = 0.6

    # Window
    window_padding: tuple[float, float] = (8.0, 8.0)
    window_rounding: float = 0.0
    window_border_size: float = 1.0
    window_min_size: tuple[float, float] = (32.0, 32.0)
    window_title_align: tuple[float, float] = (0.0, 0.5)
    window_menu_button_position: int = 0  # 0=left, 1=right

    # Child windows
    child_rounding: float = 0.0
    child_border_size: float = 1.0

    # Popups
    popup_rounding: float = 0.0
    popup_border_size: float = 1.0

    # Frames
    frame_padding: tuple[float, float] = (4.0, 3.0)
    frame_rounding: float = 0.0
    frame_border_size: float = 0.0

    # Items
    item_spacing: tuple[float, float] = (8.0, 4.0)
    item_inner_spacing: tuple[float, float] = (4.0, 4.0)

    # Touch
    touch_extra_padding: tuple[float, float] = (0.0, 0.0)

    # Indent
    indent_spacing: float = 21.0

    # Columns
    columns_min_spacing: float = 6.0

    # Scrollbar
    scrollbar_size: float = 14.0
    scrollbar_rounding: float = 9.0

    # Grab
    grab_min_size: float = 12.0
    grab_rounding: float = 0.0

    # Tabs
    tab_rounding: float = 4.0
    tab_border_size: float = 0.0
    tab_min_width_for_close_button: float = 0.0

    # Color buttons
    color_button_position: int = 1  # 0=left, 1=right

    # Buttons
    button_text_align: tuple[float, float] = (0.5, 0.5)

    # Selectable
    selectable_text_align: tuple[float, float] = (0.0, 0.0)

    # Display
    display_window_padding: tuple[float, float] = (19.0, 19.0)
    display_safe_area_padding: tuple[float, float] = (3.0, 3.0)

    # Curves
    curve_tessellation_tol: float = 1.25
    circle_tessellation_max_error: float = 0.3

    # Docking
    separator_text_border_size: float = 3.0
    separator_text_align: tuple[float, float] = (0.0, 0.5)
    separator_text_padding: tuple[float, float] = (20.0, 3.0)


@dataclass
class Theme:
    """Complete theme configuration."""

    name: str
    colors: ThemeColors = field(default_factory=ThemeColors)
    style: ThemeStyle = field(default_factory=ThemeStyle)


class ThemeManager:
    """Manager for themes and styling."""

    def __init__(self):
        """Initialize theme manager."""
        self.current_theme: Theme | None = None
        self.themes: dict[str, Theme] = {}
        logger.debug("Initialized ThemeManager")

    def register_theme(self, theme: Theme) -> None:
        """Register a theme."""
        self.themes[theme.name] = theme
        logger.debug(f"Registered theme: {theme.name}")

    def apply_theme(self, theme: Theme) -> None:
        """Apply a theme to ImGui."""
        self.current_theme = theme
        self._apply_colors(theme.colors)
        self._apply_style(theme.style)
        logger.info(f"Applied theme: {theme.name}")

    def apply_theme_by_name(self, name: str) -> None:
        """Apply a theme by name."""
        if name not in self.themes:
            logger.error(f"Theme not found: {name}")
            return
        self.apply_theme(self.themes[name])

    def apply_color_scheme(self, scheme: ColorScheme) -> None:
        """Apply a built-in color scheme."""
        if scheme == ColorScheme.DARK:
            imgui.style_colors_dark()
        elif scheme == ColorScheme.LIGHT:
            imgui.style_colors_light()
        elif scheme == ColorScheme.CLASSIC:
            imgui.style_colors_classic()
        logger.info(f"Applied color scheme: {scheme.value}")

    def _apply_colors(self, colors: ThemeColors) -> None:
        """Apply color configuration to ImGui."""
        style = imgui.get_style()

        # Window
        style.colors[imgui.Col_.window_bg.value] = colors.window_bg
        style.colors[imgui.Col_.child_bg.value] = colors.child_bg
        style.colors[imgui.Col_.popup_bg.value] = colors.popup_bg

        # Frame
        style.colors[imgui.Col_.frame_bg.value] = colors.frame_bg
        style.colors[imgui.Col_.frame_bg_hovered.value] = colors.frame_bg_hovered
        style.colors[imgui.Col_.frame_bg_active.value] = colors.frame_bg_active

        # Title
        style.colors[imgui.Col_.title_bg.value] = colors.title_bg
        style.colors[imgui.Col_.title_bg_active.value] = colors.title_bg_active
        style.colors[imgui.Col_.title_bg_collapsed.value] = colors.title_bg_collapsed

        # Menu
        style.colors[imgui.Col_.menu_bar_bg.value] = colors.menu_bar_bg

        # Scrollbar
        style.colors[imgui.Col_.scrollbar_bg.value] = colors.scrollbar_bg
        style.colors[imgui.Col_.scrollbar_grab.value] = colors.scrollbar_grab
        style.colors[imgui.Col_.scrollbar_grab_hovered.value] = (
            colors.scrollbar_grab_hovered
        )
        style.colors[imgui.Col_.scrollbar_grab_active.value] = (
            colors.scrollbar_grab_active
        )

        # Check mark
        style.colors[imgui.Col_.check_mark.value] = colors.check_mark

        # Slider
        style.colors[imgui.Col_.slider_grab.value] = colors.slider_grab
        style.colors[imgui.Col_.slider_grab_active.value] = colors.slider_grab_active

        # Button
        style.colors[imgui.Col_.button.value] = colors.button
        style.colors[imgui.Col_.button_hovered.value] = colors.button_hovered
        style.colors[imgui.Col_.button_active.value] = colors.button_active

        # Header
        style.colors[imgui.Col_.header.value] = colors.header
        style.colors[imgui.Col_.header_hovered.value] = colors.header_hovered
        style.colors[imgui.Col_.header_active.value] = colors.header_active

        # Separator
        style.colors[imgui.Col_.separator.value] = colors.separator
        style.colors[imgui.Col_.separator_hovered.value] = colors.separator_hovered
        style.colors[imgui.Col_.separator_active.value] = colors.separator_active

        # Resize grip
        style.colors[imgui.Col_.resize_grip.value] = colors.resize_grip
        style.colors[imgui.Col_.resize_grip_hovered.value] = colors.resize_grip_hovered
        style.colors[imgui.Col_.resize_grip_active.value] = colors.resize_grip_active

        # Tab
        style.colors[imgui.Col_.tab.value] = colors.tab
        style.colors[imgui.Col_.tab_hovered.value] = colors.tab_hovered
        style.colors[imgui.Col_.tab_active.value] = colors.tab_active
        style.colors[imgui.Col_.tab_unfocused.value] = colors.tab_unfocused
        style.colors[imgui.Col_.tab_unfocused_active.value] = (
            colors.tab_unfocused_active
        )

        # Docking
        style.colors[imgui.Col_.docking_preview.value] = colors.docking_preview
        style.colors[imgui.Col_.docking_empty_bg.value] = colors.docking_empty_bg

        # Plot
        style.colors[imgui.Col_.plot_lines.value] = colors.plot_lines
        style.colors[imgui.Col_.plot_lines_hovered.value] = colors.plot_lines_hovered
        style.colors[imgui.Col_.plot_histogram.value] = colors.plot_histogram
        style.colors[imgui.Col_.plot_histogram_hovered.value] = (
            colors.plot_histogram_hovered
        )

        # Text
        style.colors[imgui.Col_.text.value] = colors.text
        style.colors[imgui.Col_.text_disabled.value] = colors.text_disabled
        style.colors[imgui.Col_.text_selected_bg.value] = colors.text_selected_bg

        # Drag drop
        style.colors[imgui.Col_.drag_drop_target.value] = colors.drag_drop_target

        # Nav
        style.colors[imgui.Col_.nav_highlight.value] = colors.nav_highlight
        style.colors[imgui.Col_.nav_windowing_highlight.value] = (
            colors.nav_windowing_highlight
        )
        style.colors[imgui.Col_.nav_windowing_dim_bg.value] = (
            colors.nav_windowing_dim_bg
        )

        # Modal
        style.colors[imgui.Col_.modal_window_dim_bg.value] = colors.modal_window_dim_bg

    def _apply_style(self, theme_style: ThemeStyle) -> None:
        """Apply style configuration to ImGui."""
        style = imgui.get_style()

        # Main
        style.alpha = theme_style.alpha
        style.disabled_alpha = theme_style.disabled_alpha

        # Window
        style.window_padding = imgui.ImVec2(*theme_style.window_padding)
        style.window_rounding = theme_style.window_rounding
        style.window_border_size = theme_style.window_border_size
        style.window_min_size = imgui.ImVec2(*theme_style.window_min_size)
        style.window_title_align = imgui.ImVec2(*theme_style.window_title_align)

        # Child
        style.child_rounding = theme_style.child_rounding
        style.child_border_size = theme_style.child_border_size

        # Popup
        style.popup_rounding = theme_style.popup_rounding
        style.popup_border_size = theme_style.popup_border_size

        # Frame
        style.frame_padding = imgui.ImVec2(*theme_style.frame_padding)
        style.frame_rounding = theme_style.frame_rounding
        style.frame_border_size = theme_style.frame_border_size

        # Items
        style.item_spacing = imgui.ImVec2(*theme_style.item_spacing)
        style.item_inner_spacing = imgui.ImVec2(*theme_style.item_inner_spacing)

        # Touch
        style.touch_extra_padding = imgui.ImVec2(*theme_style.touch_extra_padding)

        # Indent
        style.indent_spacing = theme_style.indent_spacing

        # Columns
        style.columns_min_spacing = theme_style.columns_min_spacing

        # Scrollbar
        style.scrollbar_size = theme_style.scrollbar_size
        style.scrollbar_rounding = theme_style.scrollbar_rounding

        # Grab
        style.grab_min_size = theme_style.grab_min_size
        style.grab_rounding = theme_style.grab_rounding

        # Tab
        style.tab_rounding = theme_style.tab_rounding
        style.tab_border_size = theme_style.tab_border_size
        style.tab_min_width_for_close_button = (
            theme_style.tab_min_width_for_close_button
        )

        # Button
        style.button_text_align = imgui.ImVec2(*theme_style.button_text_align)

        # Selectable
        style.selectable_text_align = imgui.ImVec2(*theme_style.selectable_text_align)

        # Display
        style.display_window_padding = imgui.ImVec2(*theme_style.display_window_padding)
        style.display_safe_area_padding = imgui.ImVec2(
            *theme_style.display_safe_area_padding
        )

        # Curves
        style.curve_tessellation_tol = theme_style.curve_tessellation_tol
        style.circle_tessellation_max_error = theme_style.circle_tessellation_max_error

        # Docking
        style.separator_text_border_size = theme_style.separator_text_border_size
        style.separator_text_align = imgui.ImVec2(*theme_style.separator_text_align)
        style.separator_text_padding = imgui.ImVec2(*theme_style.separator_text_padding)

    def get_current_theme(self) -> Theme | None:
        """Get the currently applied theme."""
        return self.current_theme

    def list_themes(self) -> list[str]:
        """List all registered theme names."""
        return list(self.themes.keys())

    def export_current_colors(self) -> ThemeColors:
        """Export current ImGui colors as ThemeColors."""
        style = imgui.get_style()
        return ThemeColors(
            window_bg=tuple(style.colors[imgui.Col_.window_bg.value]),
            child_bg=tuple(style.colors[imgui.Col_.child_bg.value]),
            popup_bg=tuple(style.colors[imgui.Col_.popup_bg.value]),
            frame_bg=tuple(style.colors[imgui.Col_.frame_bg.value]),
            frame_bg_hovered=tuple(style.colors[imgui.Col_.frame_bg_hovered.value]),
            frame_bg_active=tuple(style.colors[imgui.Col_.frame_bg_active.value]),
            title_bg=tuple(style.colors[imgui.Col_.title_bg.value]),
            title_bg_active=tuple(style.colors[imgui.Col_.title_bg_active.value]),
            title_bg_collapsed=tuple(style.colors[imgui.Col_.title_bg_collapsed.value]),
            menu_bar_bg=tuple(style.colors[imgui.Col_.menu_bar_bg.value]),
            scrollbar_bg=tuple(style.colors[imgui.Col_.scrollbar_bg.value]),
            scrollbar_grab=tuple(style.colors[imgui.Col_.scrollbar_grab.value]),
            scrollbar_grab_hovered=tuple(
                style.colors[imgui.Col_.scrollbar_grab_hovered.value]
            ),
            scrollbar_grab_active=tuple(
                style.colors[imgui.Col_.scrollbar_grab_active.value]
            ),
            check_mark=tuple(style.colors[imgui.Col_.check_mark.value]),
            slider_grab=tuple(style.colors[imgui.Col_.slider_grab.value]),
            slider_grab_active=tuple(style.colors[imgui.Col_.slider_grab_active.value]),
            button=tuple(style.colors[imgui.Col_.button.value]),
            button_hovered=tuple(style.colors[imgui.Col_.button_hovered.value]),
            button_active=tuple(style.colors[imgui.Col_.button_active.value]),
            header=tuple(style.colors[imgui.Col_.header.value]),
            header_hovered=tuple(style.colors[imgui.Col_.header_hovered.value]),
            header_active=tuple(style.colors[imgui.Col_.header_active.value]),
            separator=tuple(style.colors[imgui.Col_.separator.value]),
            separator_hovered=tuple(style.colors[imgui.Col_.separator_hovered.value]),
            separator_active=tuple(style.colors[imgui.Col_.separator_active.value]),
            resize_grip=tuple(style.colors[imgui.Col_.resize_grip.value]),
            resize_grip_hovered=tuple(
                style.colors[imgui.Col_.resize_grip_hovered.value]
            ),
            resize_grip_active=tuple(style.colors[imgui.Col_.resize_grip_active.value]),
            tab=tuple(style.colors[imgui.Col_.tab.value]),
            tab_hovered=tuple(style.colors[imgui.Col_.tab_hovered.value]),
            tab_active=tuple(style.colors[imgui.Col_.tab_active.value]),
            tab_unfocused=tuple(style.colors[imgui.Col_.tab_unfocused.value]),
            tab_unfocused_active=tuple(
                style.colors[imgui.Col_.tab_unfocused_active.value]
            ),
            docking_preview=tuple(style.colors[imgui.Col_.docking_preview.value]),
            docking_empty_bg=tuple(style.colors[imgui.Col_.docking_empty_bg.value]),
            plot_lines=tuple(style.colors[imgui.Col_.plot_lines.value]),
            plot_lines_hovered=tuple(style.colors[imgui.Col_.plot_lines_hovered.value]),
            plot_histogram=tuple(style.colors[imgui.Col_.plot_histogram.value]),
            plot_histogram_hovered=tuple(
                style.colors[imgui.Col_.plot_histogram_hovered.value]
            ),
            text=tuple(style.colors[imgui.Col_.text.value]),
            text_disabled=tuple(style.colors[imgui.Col_.text_disabled.value]),
            text_selected_bg=tuple(style.colors[imgui.Col_.text_selected_bg.value]),
            drag_drop_target=tuple(style.colors[imgui.Col_.drag_drop_target.value]),
            nav_highlight=tuple(style.colors[imgui.Col_.nav_highlight.value]),
            nav_windowing_highlight=tuple(
                style.colors[imgui.Col_.nav_windowing_highlight.value]
            ),
            nav_windowing_dim_bg=tuple(
                style.colors[imgui.Col_.nav_windowing_dim_bg.value]
            ),
            modal_window_dim_bg=tuple(
                style.colors[imgui.Col_.modal_window_dim_bg.value]
            ),
        )
