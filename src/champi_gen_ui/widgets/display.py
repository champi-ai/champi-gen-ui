"""Display and visualization widgets."""

from imgui_bundle import imgui

from champi_gen_ui.core.widget import Widget


class ImageWidget(Widget):
    """Image display widget."""

    def __init__(
        self,
        widget_id: str,
        texture_id: int = 0,
        size: tuple[float, float] = (100, 100),
        **props,
    ):
        """Initialize image widget."""
        props["texture_id"] = texture_id
        props["size"] = size
        super().__init__(widget_id, **props)

    def render(self) -> None:
        """Render the image."""
        texture_id = self.state.properties.get("texture_id", 0)
        size = self.state.properties.get("size", (100, 100))
        uv0 = self.state.properties.get("uv0", (0, 0))
        uv1 = self.state.properties.get("uv1", (1, 1))
        tint_col = self.state.properties.get("tint_col", (1, 1, 1, 1))
        border_col = self.state.properties.get("border_col", (0, 0, 0, 0))

        imgui.image(
            texture_id,
            imgui.ImVec2(*size),
            imgui.ImVec2(*uv0),
            imgui.ImVec2(*uv1),
            imgui.ImVec4(*tint_col),
            imgui.ImVec4(*border_col),
        )


class ImageButtonWidget(Widget):
    """Clickable image button widget."""

    def __init__(
        self,
        widget_id: str,
        texture_id: int = 0,
        size: tuple[float, float] = (50, 50),
        **props,
    ):
        """Initialize image button widget."""
        props["texture_id"] = texture_id
        props["size"] = size
        super().__init__(widget_id, **props)

    def render(self) -> bool:
        """Render the image button."""
        texture_id = self.state.properties.get("texture_id", 0)
        size = self.state.properties.get("size", (50, 50))
        uv0 = self.state.properties.get("uv0", (0, 0))
        uv1 = self.state.properties.get("uv1", (1, 1))
        bg_col = self.state.properties.get("bg_col", (0, 0, 0, 0))
        tint_col = self.state.properties.get("tint_col", (1, 1, 1, 1))

        clicked = imgui.image_button(
            self.widget_id,
            texture_id,
            imgui.ImVec2(*size),
            imgui.ImVec2(*uv0),
            imgui.ImVec2(*uv1),
            imgui.ImVec4(*bg_col),
            imgui.ImVec4(*tint_col),
        )

        if clicked:
            self.trigger_callback("on_click")

        return clicked


class BulletWidget(Widget):
    """Bullet point widget."""

    def __init__(self, widget_id: str, **props):
        """Initialize bullet widget."""
        super().__init__(widget_id, **props)

    def render(self) -> None:
        """Render the bullet."""
        imgui.bullet()


class BulletTextWidget(Widget):
    """Bullet text widget."""

    def __init__(self, widget_id: str, text: str = "", **props):
        """Initialize bullet text widget."""
        props["text"] = text
        super().__init__(widget_id, **props)

    def render(self) -> None:
        """Render the bullet text."""
        text = self.state.properties.get("text", "")
        imgui.bullet_text(text)


class ProgressBarWidget(Widget):
    """Progress bar widget."""

    def __init__(
        self,
        widget_id: str,
        fraction: float = 0.0,
        size: tuple[float, float] = (-1, 0),
        overlay: str | None = None,
        **props,
    ):
        """Initialize progress bar widget."""
        props["fraction"] = fraction
        props["size"] = size
        props["overlay"] = overlay
        super().__init__(widget_id, **props)

    def render(self) -> None:
        """Render the progress bar."""
        fraction = self.state.properties.get("fraction", 0.0)
        size = self.state.properties.get("size", (-1, 0))
        overlay = self.state.properties.get("overlay")

        imgui.progress_bar(fraction, imgui.ImVec2(*size), overlay)


class PlotLinesWidget(Widget):
    """Line plot widget."""

    def __init__(
        self,
        widget_id: str,
        label: str = "Plot",
        values: list[float] | None = None,
        **props,
    ):
        """Initialize plot lines widget."""
        props["label"] = label
        props["values"] = values or []
        super().__init__(widget_id, **props)

    def render(self) -> None:
        """Render the plot lines."""
        label = self.state.properties.get("label", "Plot")
        values = self.state.properties.get("values", [])
        values_offset = self.state.properties.get("values_offset", 0)
        overlay_text = self.state.properties.get("overlay_text")
        scale_min = self.state.properties.get("scale_min")
        scale_max = self.state.properties.get("scale_max")
        graph_size = self.state.properties.get("graph_size", (0, 0))

        if values:
            imgui.plot_lines(
                label,
                values,
                values_offset,
                overlay_text,
                scale_min,
                scale_max,
                imgui.ImVec2(*graph_size),
            )


class PlotHistogramWidget(Widget):
    """Histogram plot widget."""

    def __init__(
        self,
        widget_id: str,
        label: str = "Histogram",
        values: list[float] | None = None,
        **props,
    ):
        """Initialize plot histogram widget."""
        props["label"] = label
        props["values"] = values or []
        super().__init__(widget_id, **props)

    def render(self) -> None:
        """Render the histogram."""
        label = self.state.properties.get("label", "Histogram")
        values = self.state.properties.get("values", [])
        values_offset = self.state.properties.get("values_offset", 0)
        overlay_text = self.state.properties.get("overlay_text")
        scale_min = self.state.properties.get("scale_min")
        scale_max = self.state.properties.get("scale_max")
        graph_size = self.state.properties.get("graph_size", (0, 0))

        if values:
            imgui.plot_histogram(
                label,
                values,
                values_offset,
                overlay_text,
                scale_min,
                scale_max,
                imgui.ImVec2(*graph_size),
            )


class TextColoredWidget(Widget):
    """Colored text widget."""

    def __init__(
        self,
        widget_id: str,
        text: str = "",
        color: tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0),
        **props,
    ):
        """Initialize colored text widget."""
        props["text"] = text
        props["color"] = color
        super().__init__(widget_id, **props)

    def render(self) -> None:
        """Render the colored text."""
        text = self.state.properties.get("text", "")
        color = self.state.properties.get("color", (1.0, 1.0, 1.0, 1.0))
        imgui.text_colored(imgui.ImVec4(*color), text)


class TextDisabledWidget(Widget):
    """Disabled (grayed out) text widget."""

    def __init__(self, widget_id: str, text: str = "", **props):
        """Initialize disabled text widget."""
        props["text"] = text
        super().__init__(widget_id, **props)

    def render(self) -> None:
        """Render the disabled text."""
        text = self.state.properties.get("text", "")
        imgui.text_disabled(text)


class TextWrappedWidget(Widget):
    """Wrapped text widget."""

    def __init__(self, widget_id: str, text: str = "", **props):
        """Initialize wrapped text widget."""
        props["text"] = text
        super().__init__(widget_id, **props)

    def render(self) -> None:
        """Render the wrapped text."""
        text = self.state.properties.get("text", "")
        imgui.text_wrapped(text)


class LabelTextWidget(Widget):
    """Label with text value widget."""

    def __init__(
        self,
        widget_id: str,
        label: str = "Label",
        text: str = "",
        **props,
    ):
        """Initialize label text widget."""
        props["label"] = label
        props["text"] = text
        super().__init__(widget_id, **props)

    def render(self) -> None:
        """Render the label text."""
        label = self.state.properties.get("label", "Label")
        text = self.state.properties.get("text", "")
        imgui.label_text(label, text)


class HelpMarkerWidget(Widget):
    """Help marker (?) with tooltip widget."""

    def __init__(
        self,
        widget_id: str,
        text: str = "",
        marker: str = "(?)",
        **props,
    ):
        """Initialize help marker widget."""
        props["text"] = text
        props["marker"] = marker
        super().__init__(widget_id, **props)

    def render(self) -> None:
        """Render the help marker."""
        text = self.state.properties.get("text", "")
        marker = self.state.properties.get("marker", "(?)")

        imgui.text_disabled(marker)
        if imgui.is_item_hovered():
            imgui.set_tooltip(text)


class LoadingIndicatorWidget(Widget):
    """Loading indicator (spinner) widget."""

    def __init__(
        self,
        widget_id: str,
        label: str = "Loading",
        radius: float = 10.0,
        **props,
    ):
        """Initialize loading indicator widget."""
        props["label"] = label
        props["radius"] = radius
        super().__init__(widget_id, **props)

    def render(self) -> None:
        """Render the loading indicator."""
        label = self.state.properties.get("label", "Loading")
        radius = self.state.properties.get("radius", 10.0)
        thickness = self.state.properties.get("thickness", 3.0)
        color = self.state.properties.get("color", (1.0, 1.0, 1.0, 1.0))

        # Custom spinner using draw list
        draw_list = imgui.get_window_draw_list()
        pos = imgui.get_cursor_screen_pos()
        center = imgui.ImVec2(pos.x + radius, pos.y + radius)

        # Simple rotating arc
        num_segments = 12
        start = imgui.get_time() * 6.0
        imgui.dummy(imgui.ImVec2(radius * 2, radius * 2))

        for i in range(num_segments):
            angle = start + (i / num_segments) * 3.14159 * 2
            alpha = 1.0 - (i / num_segments)
            col = imgui.get_color_u32(
                imgui.ImVec4(color[0], color[1], color[2], color[3] * alpha)
            )
            draw_list.add_circle_filled(
                imgui.ImVec2(
                    center.x + radius * 0.7 * imgui.math.cos(angle),
                    center.y + radius * 0.7 * imgui.math.sin(angle),
                ),
                thickness,
                col,
            )

        if label:
            imgui.same_line()
            imgui.text(label)
