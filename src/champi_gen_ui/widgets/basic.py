"""Basic widgets: buttons, text, inputs, checkboxes."""

from imgui_bundle import imgui

from champi_gen_ui.core.widget import Widget


class ButtonWidget(Widget):
    """Button widget."""

    def __init__(self, widget_id: str, label: str = "Button", **props):
        """Initialize button."""
        props["label"] = label
        super().__init__(widget_id, **props)

    def render(self) -> bool:
        """Render the button."""
        label = self.state.properties.get("label", "Button")
        size = self.state.properties.get("size")

        if size:
            clicked = imgui.button(label, imgui.ImVec2(size[0], size[1]))
        else:
            clicked = imgui.button(label)

        if clicked:
            self.trigger_callback("on_click")

        return clicked


class TextWidget(Widget):
    """Static text label widget."""

    def __init__(self, widget_id: str, text: str = "", **props):
        """Initialize text widget."""
        props["text"] = text
        super().__init__(widget_id, **props)

    def render(self) -> None:
        """Render the text."""
        text = self.state.properties.get("text", "")
        color = self.state.properties.get("color")
        wrapped = self.state.properties.get("wrapped", False)
        disabled = self.state.properties.get("disabled", False)

        if color:
            imgui.text_colored(imgui.ImVec4(*color), text)
        elif disabled:
            imgui.text_disabled(text)
        elif wrapped:
            imgui.text_wrapped(text)
        else:
            imgui.text(text)


class InputTextWidget(Widget):
    """Text input widget."""

    def __init__(self, widget_id: str, label: str = "Input", value: str = "", **props):
        """Initialize input text widget."""
        props["label"] = label
        props["value"] = value
        super().__init__(widget_id, **props)
        self._value = value

    def render(self) -> str:
        """Render the input field."""
        label = self.state.properties.get("label", "Input")
        hint = self.state.properties.get("hint")
        multiline = self.state.properties.get("multiline", False)
        size = self.state.properties.get("size")

        if multiline and size:
            changed, self._value = imgui.input_text_multiline(
                label, self._value, imgui.ImVec2(size[0], size[1])
            )
        elif hint:
            changed, self._value = imgui.input_text_with_hint(label, hint, self._value)
        else:
            changed, self._value = imgui.input_text(label, self._value)

        if changed:
            self.state.properties["value"] = self._value
            self.trigger_callback("on_change", self._value)

        return self._value

    def get_value(self) -> str:
        """Get current value."""
        return self._value

    def set_value(self, value: str) -> None:
        """Set value."""
        self._value = value
        self.state.properties["value"] = value


class CheckboxWidget(Widget):
    """Checkbox widget."""

    def __init__(
        self, widget_id: str, label: str = "Checkbox", checked: bool = False, **props
    ):
        """Initialize checkbox."""
        props["label"] = label
        props["checked"] = checked
        super().__init__(widget_id, **props)
        self._checked = checked

    def render(self) -> bool:
        """Render the checkbox."""
        label = self.state.properties.get("label", "Checkbox")
        changed, self._checked = imgui.checkbox(label, self._checked)

        if changed:
            self.state.properties["checked"] = self._checked
            self.trigger_callback("on_change", self._checked)

        return self._checked

    def get_checked(self) -> bool:
        """Get checked state."""
        return self._checked

    def set_checked(self, checked: bool) -> None:
        """Set checked state."""
        self._checked = checked
        self.state.properties["checked"] = checked


class RadioButtonWidget(Widget):
    """Radio button widget."""

    def __init__(
        self, widget_id: str, label: str = "Radio", active: bool = False, **props
    ):
        """Initialize radio button."""
        props["label"] = label
        props["active"] = active
        super().__init__(widget_id, **props)
        self._active = active

    def render(self) -> bool:
        """Render the radio button."""
        label = self.state.properties.get("label", "Radio")
        clicked = imgui.radio_button(label, self._active)

        if clicked:
            self._active = not self._active
            self.state.properties["active"] = self._active
            self.trigger_callback("on_click", self._active)

        return clicked


class ComboWidget(Widget):
    """Combo box (dropdown) widget."""

    def __init__(
        self,
        widget_id: str,
        label: str = "Combo",
        items: list[str] | None = None,
        current_item: int = 0,
        **props,
    ):
        """Initialize combo box."""
        props["label"] = label
        props["items"] = items or []
        props["current_item"] = current_item
        super().__init__(widget_id, **props)
        self._current_item = current_item

    def render(self) -> int:
        """Render the combo box."""
        label = self.state.properties.get("label", "Combo")
        items = self.state.properties.get("items", [])

        if not items:
            return self._current_item

        changed, self._current_item = imgui.combo(label, self._current_item, items)

        if changed:
            self.state.properties["current_item"] = self._current_item
            self.trigger_callback(
                "on_change", self._current_item, items[self._current_item]
            )

        return self._current_item

    def get_current_item(self) -> int:
        """Get current selected item index."""
        return self._current_item

    def get_current_value(self) -> str | None:
        """Get current selected item value."""
        items = self.state.properties.get("items", [])
        if 0 <= self._current_item < len(items):
            return items[self._current_item]
        return None


class ListBoxWidget(Widget):
    """List box widget."""

    def __init__(
        self,
        widget_id: str,
        label: str = "ListBox",
        items: list[str] | None = None,
        current_item: int = 0,
        **props,
    ):
        """Initialize list box."""
        props["label"] = label
        props["items"] = items or []
        props["current_item"] = current_item
        super().__init__(widget_id, **props)
        self._current_item = current_item

    def render(self) -> int:
        """Render the list box."""
        label = self.state.properties.get("label", "ListBox")
        items = self.state.properties.get("items", [])
        height_in_items = self.state.properties.get("height_in_items", -1)

        if not items:
            return self._current_item

        changed, self._current_item = imgui.list_box(
            label, self._current_item, items, height_in_items
        )

        if changed:
            self.state.properties["current_item"] = self._current_item
            self.trigger_callback(
                "on_change", self._current_item, items[self._current_item]
            )

        return self._current_item


class ColorPickerWidget(Widget):
    """Color picker widget."""

    def __init__(
        self,
        widget_id: str,
        label: str = "Color",
        color: tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0),
        **props,
    ):
        """Initialize color picker."""
        props["label"] = label
        props["color"] = color
        super().__init__(widget_id, **props)
        self._color = list(color)

    def render(self) -> tuple:
        """Render the color picker."""
        label = self.state.properties.get("label", "Color")
        alpha = self.state.properties.get("alpha", True)

        if alpha:
            changed, self._color = imgui.color_edit4(label, self._color)
        else:
            changed, color3 = imgui.color_edit3(label, self._color[:3])
            if changed:
                self._color = [*list(color3), self._color[3]]

        if changed:
            self.state.properties["color"] = tuple(self._color)
            self.trigger_callback("on_change", tuple(self._color))

        return tuple(self._color)

    def get_color(self) -> tuple:
        """Get current color."""
        return tuple(self._color)
