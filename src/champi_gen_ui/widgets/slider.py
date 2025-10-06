"""Slider and drag control widgets."""

from imgui_bundle import imgui

from champi_gen_ui.core.widget import Widget


class SliderIntWidget(Widget):
    """Integer slider widget."""

    def __init__(
        self,
        widget_id: str,
        label: str = "Slider",
        value: int = 0,
        v_min: int = 0,
        v_max: int = 100,
        **props,
    ):
        """Initialize integer slider."""
        props["label"] = label
        props["value"] = value
        props["v_min"] = v_min
        props["v_max"] = v_max
        super().__init__(widget_id, **props)
        self._value = value

    def render(self) -> int:
        """Render the slider."""
        label = self.state.properties.get("label", "Slider")
        v_min = self.state.properties.get("v_min", 0)
        v_max = self.state.properties.get("v_max", 100)
        format_str = self.state.properties.get("format", "%d")

        changed, self._value = imgui.slider_int(
            label, self._value, v_min, v_max, format_str
        )

        if changed:
            self.state.properties["value"] = self._value
            self.trigger_callback("on_change", self._value)

        return self._value

    def get_value(self) -> int:
        """Get current value."""
        return self._value

    def set_value(self, value: int) -> None:
        """Set value."""
        self._value = value
        self.state.properties["value"] = value


class SliderFloatWidget(Widget):
    """Float slider widget."""

    def __init__(
        self,
        widget_id: str,
        label: str = "Slider",
        value: float = 0.0,
        v_min: float = 0.0,
        v_max: float = 1.0,
        **props,
    ):
        """Initialize float slider."""
        props["label"] = label
        props["value"] = value
        props["v_min"] = v_min
        props["v_max"] = v_max
        super().__init__(widget_id, **props)
        self._value = value

    def render(self) -> float:
        """Render the slider."""
        label = self.state.properties.get("label", "Slider")
        v_min = self.state.properties.get("v_min", 0.0)
        v_max = self.state.properties.get("v_max", 1.0)
        format_str = self.state.properties.get("format", "%.3f")

        changed, self._value = imgui.slider_float(
            label, self._value, v_min, v_max, format_str
        )

        if changed:
            self.state.properties["value"] = self._value
            self.trigger_callback("on_change", self._value)

        return self._value

    def get_value(self) -> float:
        """Get current value."""
        return self._value

    def set_value(self, value: float) -> None:
        """Set value."""
        self._value = value
        self.state.properties["value"] = value


class DragIntWidget(Widget):
    """Integer drag control widget."""

    def __init__(
        self,
        widget_id: str,
        label: str = "Drag",
        value: int = 0,
        v_speed: float = 1.0,
        v_min: int = 0,
        v_max: int = 0,
        **props,
    ):
        """Initialize integer drag."""
        props["label"] = label
        props["value"] = value
        props["v_speed"] = v_speed
        props["v_min"] = v_min
        props["v_max"] = v_max
        super().__init__(widget_id, **props)
        self._value = value

    def render(self) -> int:
        """Render the drag control."""
        label = self.state.properties.get("label", "Drag")
        v_speed = self.state.properties.get("v_speed", 1.0)
        v_min = self.state.properties.get("v_min", 0)
        v_max = self.state.properties.get("v_max", 0)
        format_str = self.state.properties.get("format", "%d")

        changed, self._value = imgui.drag_int(
            label, self._value, v_speed, v_min, v_max, format_str
        )

        if changed:
            self.state.properties["value"] = self._value
            self.trigger_callback("on_change", self._value)

        return self._value


class DragFloatWidget(Widget):
    """Float drag control widget."""

    def __init__(
        self,
        widget_id: str,
        label: str = "Drag",
        value: float = 0.0,
        v_speed: float = 0.01,
        v_min: float = 0.0,
        v_max: float = 0.0,
        **props,
    ):
        """Initialize float drag."""
        props["label"] = label
        props["value"] = value
        props["v_speed"] = v_speed
        props["v_min"] = v_min
        props["v_max"] = v_max
        super().__init__(widget_id, **props)
        self._value = value

    def render(self) -> float:
        """Render the drag control."""
        label = self.state.properties.get("label", "Drag")
        v_speed = self.state.properties.get("v_speed", 0.01)
        v_min = self.state.properties.get("v_min", 0.0)
        v_max = self.state.properties.get("v_max", 0.0)
        format_str = self.state.properties.get("format", "%.3f")

        changed, self._value = imgui.drag_float(
            label, self._value, v_speed, v_min, v_max, format_str
        )

        if changed:
            self.state.properties["value"] = self._value
            self.trigger_callback("on_change", self._value)

        return self._value


class ProgressBarWidget(Widget):
    """Progress bar widget."""

    def __init__(
        self,
        widget_id: str,
        fraction: float = 0.0,
        size: tuple[float, float] = (-1.0, 0.0),
        **props,
    ):
        """Initialize progress bar."""
        props["fraction"] = fraction
        props["size"] = size
        super().__init__(widget_id, **props)

    def render(self) -> None:
        """Render the progress bar."""
        fraction = self.state.properties.get("fraction", 0.0)
        size = self.state.properties.get("size", (-1.0, 0.0))
        overlay = self.state.properties.get("overlay")

        imgui.progress_bar(fraction, imgui.ImVec2(*size), overlay)

    def set_progress(self, fraction: float) -> None:
        """Set progress value (0.0 to 1.0)."""
        self.state.properties["fraction"] = max(0.0, min(1.0, fraction))
