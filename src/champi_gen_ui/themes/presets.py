"""Preset themes for common use cases."""

from champi_gen_ui.themes.manager import Theme, ThemeColors, ThemeStyle


def create_dark_theme() -> Theme:
    """Create a dark theme (default ImGui dark)."""
    return Theme(
        name="Dark",
        colors=ThemeColors(
            window_bg=(0.1, 0.1, 0.1, 1.0),
            frame_bg=(0.16, 0.16, 0.16, 1.0),
            button=(0.26, 0.59, 0.98, 0.4),
            button_hovered=(0.26, 0.59, 0.98, 1.0),
            button_active=(0.06, 0.53, 0.98, 1.0),
        ),
        style=ThemeStyle(
            window_rounding=0.0,
            frame_rounding=0.0,
        ),
    )


def create_light_theme() -> Theme:
    """Create a light theme."""
    return Theme(
        name="Light",
        colors=ThemeColors(
            window_bg=(0.94, 0.94, 0.94, 1.0),
            child_bg=(0.0, 0.0, 0.0, 0.0),
            popup_bg=(1.0, 1.0, 1.0, 0.98),
            frame_bg=(1.0, 1.0, 1.0, 1.0),
            frame_bg_hovered=(0.26, 0.59, 0.98, 0.4),
            frame_bg_active=(0.26, 0.59, 0.98, 0.67),
            title_bg=(0.96, 0.96, 0.96, 1.0),
            title_bg_active=(0.82, 0.82, 0.82, 1.0),
            title_bg_collapsed=(1.0, 1.0, 1.0, 0.51),
            menu_bar_bg=(0.86, 0.86, 0.86, 1.0),
            scrollbar_bg=(0.98, 0.98, 0.98, 0.53),
            scrollbar_grab=(0.69, 0.69, 0.69, 0.8),
            scrollbar_grab_hovered=(0.49, 0.49, 0.49, 0.8),
            scrollbar_grab_active=(0.49, 0.49, 0.49, 1.0),
            check_mark=(0.26, 0.59, 0.98, 1.0),
            slider_grab=(0.26, 0.59, 0.98, 0.78),
            slider_grab_active=(0.46, 0.54, 0.8, 0.6),
            button=(0.26, 0.59, 0.98, 0.4),
            button_hovered=(0.26, 0.59, 0.98, 1.0),
            button_active=(0.06, 0.53, 0.98, 1.0),
            header=(0.26, 0.59, 0.98, 0.31),
            header_hovered=(0.26, 0.59, 0.98, 0.8),
            header_active=(0.26, 0.59, 0.98, 1.0),
            separator=(0.39, 0.39, 0.39, 0.62),
            separator_hovered=(0.14, 0.44, 0.8, 0.78),
            separator_active=(0.14, 0.44, 0.8, 1.0),
            resize_grip=(0.35, 0.35, 0.35, 0.17),
            resize_grip_hovered=(0.26, 0.59, 0.98, 0.67),
            resize_grip_active=(0.26, 0.59, 0.98, 0.95),
            tab=(0.76, 0.8, 0.84, 0.93),
            tab_hovered=(0.26, 0.59, 0.98, 0.8),
            tab_active=(0.6, 0.73, 0.88, 1.0),
            tab_unfocused=(0.92, 0.93, 0.94, 0.98),
            tab_unfocused_active=(0.74, 0.82, 0.91, 1.0),
            text=(0.0, 0.0, 0.0, 1.0),
            text_disabled=(0.6, 0.6, 0.6, 1.0),
            text_selected_bg=(0.26, 0.59, 0.98, 0.35),
        ),
        style=ThemeStyle(
            window_rounding=0.0,
            frame_rounding=0.0,
        ),
    )


def create_cherry_theme() -> Theme:
    """Create a cherry-inspired dark theme with red accents."""
    return Theme(
        name="Cherry",
        colors=ThemeColors(
            window_bg=(0.1, 0.05, 0.08, 1.0),
            frame_bg=(0.15, 0.08, 0.1, 1.0),
            frame_bg_hovered=(0.25, 0.1, 0.15, 1.0),
            frame_bg_active=(0.3, 0.12, 0.18, 1.0),
            button=(0.86, 0.2, 0.39, 0.6),
            button_hovered=(0.86, 0.2, 0.39, 1.0),
            button_active=(0.76, 0.1, 0.29, 1.0),
            header=(0.86, 0.2, 0.39, 0.4),
            header_hovered=(0.86, 0.2, 0.39, 0.8),
            header_active=(0.86, 0.2, 0.39, 1.0),
            slider_grab=(0.86, 0.2, 0.39, 0.8),
            slider_grab_active=(0.96, 0.3, 0.49, 1.0),
            check_mark=(0.86, 0.2, 0.39, 1.0),
            tab=(0.66, 0.15, 0.29, 0.86),
            tab_hovered=(0.86, 0.2, 0.39, 0.8),
            tab_active=(0.76, 0.18, 0.34, 1.0),
        ),
        style=ThemeStyle(
            window_rounding=4.0,
            frame_rounding=2.0,
            grab_rounding=2.0,
            tab_rounding=2.0,
        ),
    )


def create_nord_theme() -> Theme:
    """Create a Nord-inspired theme."""
    return Theme(
        name="Nord",
        colors=ThemeColors(
            # Nord Polar Night
            window_bg=(0.18, 0.2, 0.25, 1.0),  # nord0
            child_bg=(0.16, 0.17, 0.21, 1.0),  # nord1
            popup_bg=(0.18, 0.2, 0.25, 0.95),
            frame_bg=(0.16, 0.17, 0.21, 1.0),
            frame_bg_hovered=(0.23, 0.26, 0.32, 1.0),  # nord2
            frame_bg_active=(0.26, 0.3, 0.37, 1.0),  # nord3
            title_bg=(0.16, 0.17, 0.21, 1.0),
            title_bg_active=(0.18, 0.2, 0.25, 1.0),
            title_bg_collapsed=(0.16, 0.17, 0.21, 0.75),
            menu_bar_bg=(0.18, 0.2, 0.25, 1.0),
            # Nord Frost - for interactive elements
            button=(0.53, 0.75, 0.82, 0.4),  # nord8
            button_hovered=(0.53, 0.75, 0.82, 1.0),
            button_active=(0.5, 0.63, 0.76, 1.0),  # nord9
            slider_grab=(0.53, 0.75, 0.82, 0.8),
            slider_grab_active=(0.5, 0.63, 0.76, 1.0),
            check_mark=(0.64, 0.75, 0.54, 1.0),  # nord14
            header=(0.53, 0.75, 0.82, 0.31),
            header_hovered=(0.53, 0.75, 0.82, 0.8),
            header_active=(0.53, 0.75, 0.82, 1.0),
            tab=(0.37, 0.51, 0.71, 0.86),  # nord10
            tab_hovered=(0.53, 0.75, 0.82, 0.8),
            tab_active=(0.5, 0.63, 0.76, 1.0),
            # Nord Snow Storm - for text
            text=(0.93, 0.94, 0.95, 1.0),  # nord6
            text_disabled=(0.6, 0.63, 0.69, 1.0),  # nord4
        ),
        style=ThemeStyle(
            window_rounding=3.0,
            frame_rounding=2.0,
            grab_rounding=2.0,
            tab_rounding=2.0,
        ),
    )


def create_dracula_theme() -> Theme:
    """Create a Dracula-inspired theme."""
    return Theme(
        name="Dracula",
        colors=ThemeColors(
            # Dracula background
            window_bg=(0.16, 0.17, 0.21, 1.0),  # #282a36
            child_bg=(0.15, 0.15, 0.19, 1.0),
            popup_bg=(0.16, 0.17, 0.21, 0.95),
            frame_bg=(0.27, 0.28, 0.35, 1.0),  # #44475a
            frame_bg_hovered=(0.33, 0.34, 0.42, 1.0),
            frame_bg_active=(0.38, 0.4, 0.49, 1.0),
            # Dracula purple for interactive elements
            button=(0.74, 0.58, 0.98, 0.4),  # #bd93f9
            button_hovered=(0.74, 0.58, 0.98, 1.0),
            button_active=(0.68, 0.51, 0.93, 1.0),
            slider_grab=(0.74, 0.58, 0.98, 0.8),
            slider_grab_active=(0.68, 0.51, 0.93, 1.0),
            header=(0.74, 0.58, 0.98, 0.31),
            header_hovered=(0.74, 0.58, 0.98, 0.8),
            header_active=(0.74, 0.58, 0.98, 1.0),
            # Dracula pink for accents
            check_mark=(1.0, 0.47, 0.78, 1.0),  # #ff79c6
            tab=(0.74, 0.58, 0.98, 0.86),
            tab_hovered=(0.74, 0.58, 0.98, 0.8),
            tab_active=(0.68, 0.51, 0.93, 1.0),
            # Dracula foreground
            text=(0.95, 0.96, 0.97, 1.0),  # #f8f8f2
            text_disabled=(0.62, 0.63, 0.64, 1.0),
        ),
        style=ThemeStyle(
            window_rounding=4.0,
            frame_rounding=3.0,
            grab_rounding=3.0,
            tab_rounding=3.0,
        ),
    )


def create_gruvbox_theme() -> Theme:
    """Create a Gruvbox-inspired dark theme."""
    return Theme(
        name="Gruvbox",
        colors=ThemeColors(
            # Gruvbox dark background
            window_bg=(0.16, 0.15, 0.13, 1.0),  # #282828
            child_bg=(0.11, 0.11, 0.09, 1.0),  # #1d2021
            popup_bg=(0.16, 0.15, 0.13, 0.95),
            frame_bg=(0.2, 0.19, 0.17, 1.0),  # #32302f
            frame_bg_hovered=(0.25, 0.24, 0.21, 1.0),
            frame_bg_active=(0.3, 0.28, 0.25, 1.0),
            # Gruvbox orange for interactive elements
            button=(0.83, 0.6, 0.28, 0.4),  # #d3869b
            button_hovered=(0.83, 0.6, 0.28, 1.0),
            button_active=(0.93, 0.66, 0.27, 1.0),  # #fe8019
            slider_grab=(0.83, 0.6, 0.28, 0.8),
            slider_grab_active=(0.93, 0.66, 0.27, 1.0),
            # Gruvbox green for checks
            check_mark=(0.72, 0.73, 0.39, 1.0),  # #b8bb26
            # Gruvbox aqua for headers
            header=(0.55, 0.75, 0.64, 0.31),  # #8ec07c
            header_hovered=(0.55, 0.75, 0.64, 0.8),
            header_active=(0.55, 0.75, 0.64, 1.0),
            tab=(0.83, 0.6, 0.28, 0.86),
            tab_hovered=(0.83, 0.6, 0.28, 0.8),
            tab_active=(0.93, 0.66, 0.27, 1.0),
            # Gruvbox foreground
            text=(0.92, 0.86, 0.7, 1.0),  # #ebdbb2
            text_disabled=(0.66, 0.6, 0.52, 1.0),  # #a89984
        ),
        style=ThemeStyle(
            window_rounding=2.0,
            frame_rounding=1.0,
            grab_rounding=1.0,
            tab_rounding=1.0,
        ),
    )


def create_solarized_dark_theme() -> Theme:
    """Create a Solarized Dark theme."""
    return Theme(
        name="Solarized Dark",
        colors=ThemeColors(
            # Solarized base03 (darkest)
            window_bg=(0.0, 0.17, 0.21, 1.0),  # #002b36
            child_bg=(0.03, 0.21, 0.26, 1.0),  # #073642
            popup_bg=(0.0, 0.17, 0.21, 0.95),
            frame_bg=(0.03, 0.21, 0.26, 1.0),
            frame_bg_hovered=(0.05, 0.24, 0.3, 1.0),
            frame_bg_active=(0.07, 0.27, 0.33, 1.0),
            # Solarized blue for interactive elements
            button=(0.15, 0.55, 0.82, 0.4),  # #268bd2
            button_hovered=(0.15, 0.55, 0.82, 1.0),
            button_active=(0.13, 0.47, 0.71, 1.0),
            slider_grab=(0.15, 0.55, 0.82, 0.8),
            slider_grab_active=(0.13, 0.47, 0.71, 1.0),
            # Solarized green for checks
            check_mark=(0.52, 0.6, 0.0, 1.0),  # #859900
            # Solarized cyan for headers
            header=(0.16, 0.63, 0.6, 0.31),  # #2aa198
            header_hovered=(0.16, 0.63, 0.6, 0.8),
            header_active=(0.16, 0.63, 0.6, 1.0),
            tab=(0.15, 0.55, 0.82, 0.86),
            tab_hovered=(0.15, 0.55, 0.82, 0.8),
            tab_active=(0.13, 0.47, 0.71, 1.0),
            # Solarized base0 (lightest content tone)
            text=(0.51, 0.58, 0.59, 1.0),  # #839496
            text_disabled=(0.36, 0.43, 0.44, 1.0),  # #586e75
        ),
        style=ThemeStyle(
            window_rounding=3.0,
            frame_rounding=2.0,
            grab_rounding=2.0,
            tab_rounding=2.0,
        ),
    )


def create_monokai_theme() -> Theme:
    """Create a Monokai-inspired theme."""
    return Theme(
        name="Monokai",
        colors=ThemeColors(
            # Monokai background
            window_bg=(0.16, 0.16, 0.14, 1.0),  # #272822
            child_bg=(0.14, 0.14, 0.12, 1.0),
            popup_bg=(0.16, 0.16, 0.14, 0.95),
            frame_bg=(0.2, 0.2, 0.18, 1.0),
            frame_bg_hovered=(0.24, 0.24, 0.22, 1.0),
            frame_bg_active=(0.28, 0.28, 0.25, 1.0),
            # Monokai magenta for interactive elements
            button=(0.98, 0.15, 0.45, 0.4),  # #f92672
            button_hovered=(0.98, 0.15, 0.45, 1.0),
            button_active=(0.88, 0.13, 0.4, 1.0),
            slider_grab=(0.98, 0.15, 0.45, 0.8),
            slider_grab_active=(0.88, 0.13, 0.4, 1.0),
            # Monokai green for checks
            check_mark=(0.65, 0.89, 0.18, 1.0),  # #a6e22e
            # Monokai cyan for headers
            header=(0.4, 0.85, 0.94, 0.31),  # #66d9ef
            header_hovered=(0.4, 0.85, 0.94, 0.8),
            header_active=(0.4, 0.85, 0.94, 1.0),
            tab=(0.98, 0.15, 0.45, 0.86),
            tab_hovered=(0.98, 0.15, 0.45, 0.8),
            tab_active=(0.88, 0.13, 0.4, 1.0),
            # Monokai foreground
            text=(0.97, 0.96, 0.94, 1.0),  # #f8f8f2
            text_disabled=(0.46, 0.45, 0.43, 1.0),  # #75715e
        ),
        style=ThemeStyle(
            window_rounding=4.0,
            frame_rounding=3.0,
            grab_rounding=3.0,
            tab_rounding=3.0,
        ),
    )


def create_material_theme() -> Theme:
    """Create a Material Design-inspired dark theme."""
    return Theme(
        name="Material",
        colors=ThemeColors(
            # Material dark background
            window_bg=(0.12, 0.12, 0.12, 1.0),  # #1e1e1e
            child_bg=(0.09, 0.09, 0.09, 1.0),
            popup_bg=(0.15, 0.15, 0.15, 0.95),
            frame_bg=(0.18, 0.18, 0.18, 1.0),
            frame_bg_hovered=(0.22, 0.22, 0.22, 1.0),
            frame_bg_active=(0.26, 0.26, 0.26, 1.0),
            # Material blue for interactive elements
            button=(0.13, 0.59, 0.95, 0.4),  # #2196f3
            button_hovered=(0.13, 0.59, 0.95, 1.0),
            button_active=(0.1, 0.46, 0.82, 1.0),  # #1976d2
            slider_grab=(0.13, 0.59, 0.95, 0.8),
            slider_grab_active=(0.1, 0.46, 0.82, 1.0),
            # Material teal for checks
            check_mark=(0.0, 0.59, 0.53, 1.0),  # #009688
            # Material indigo for headers
            header=(0.25, 0.32, 0.71, 0.31),  # #3f51b5
            header_hovered=(0.25, 0.32, 0.71, 0.8),
            header_active=(0.25, 0.32, 0.71, 1.0),
            tab=(0.13, 0.59, 0.95, 0.86),
            tab_hovered=(0.13, 0.59, 0.95, 0.8),
            tab_active=(0.1, 0.46, 0.82, 1.0),
            # Material text
            text=(1.0, 1.0, 1.0, 0.87),
            text_disabled=(1.0, 1.0, 1.0, 0.38),
        ),
        style=ThemeStyle(
            window_rounding=2.0,
            frame_rounding=2.0,
            grab_rounding=2.0,
            tab_rounding=2.0,
        ),
    )


# Preset themes dictionary
THEME_PRESETS: dict[str, Theme] = {
    "dark": create_dark_theme(),
    "light": create_light_theme(),
    "cherry": create_cherry_theme(),
    "nord": create_nord_theme(),
    "dracula": create_dracula_theme(),
    "gruvbox": create_gruvbox_theme(),
    "solarized_dark": create_solarized_dark_theme(),
    "monokai": create_monokai_theme(),
    "material": create_material_theme(),
}
