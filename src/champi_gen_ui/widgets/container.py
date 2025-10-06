"""Container widgets: windows, panels, groups."""

from imgui_bundle import imgui

from champi_gen_ui.core.widget import Widget


class WindowWidget(Widget):
    """Standalone window container widget."""

    def __init__(
        self,
        widget_id: str,
        title: str = "Window",
        closable: bool = True,
        **props,
    ):
        """Initialize window widget."""
        props["title"] = title
        props["closable"] = closable
        props["is_open"] = True
        super().__init__(widget_id, **props)

    def render(self) -> bool:
        """Render the window."""
        title = self.state.properties.get("title", "Window")
        closable = self.state.properties.get("closable", True)
        flags = self.state.properties.get("flags", 0)
        is_open = self.state.properties.get("is_open", True)

        if not is_open:
            return False

        if closable:
            expanded, is_open = imgui.begin(title, True, flags)
            self.state.properties["is_open"] = is_open
        else:
            expanded, _ = imgui.begin(title, None, flags)

        if expanded:
            # Render children widgets here
            # This would be handled by the canvas
            pass

        imgui.end()
        return is_open


class ChildWindowWidget(Widget):
    """Child window (embedded region) widget."""

    def __init__(
        self,
        widget_id: str,
        size: tuple[float, float] = (0, 0),
        border: bool = False,
        **props,
    ):
        """Initialize child window."""
        props["size"] = size
        props["border"] = border
        super().__init__(widget_id, **props)

    def render(self) -> bool:
        """Render the child window."""
        size = self.state.properties.get("size", (0, 0))
        border = self.state.properties.get("border", False)
        flags = self.state.properties.get("flags", 0)

        result = imgui.begin_child(self.widget_id, imgui.ImVec2(*size), border, flags)

        if result:
            # Render children widgets here
            pass

        imgui.end_child()
        return result


class GroupWidget(Widget):
    """Group widget for layout."""

    def __init__(self, widget_id: str, **props):
        """Initialize group widget."""
        super().__init__(widget_id, **props)

    def render(self) -> None:
        """Render the group."""
        imgui.begin_group()
        # Children would be rendered here by canvas
        # The canvas will handle rendering child widgets
        imgui.end_group()


class CollapsingHeaderWidget(Widget):
    """Collapsible section header widget."""

    def __init__(
        self,
        widget_id: str,
        label: str = "Header",
        default_open: bool = False,
        **props,
    ):
        """Initialize collapsing header."""
        props["label"] = label
        props["is_open"] = default_open
        super().__init__(widget_id, **props)

    def render(self) -> bool:
        """Render the collapsing header."""
        label = self.state.properties.get("label", "Header")
        flags = self.state.properties.get("flags", 0)

        is_open = imgui.collapsing_header(label, flags)
        self.state.properties["is_open"] = is_open

        if is_open:
            self.trigger_callback("on_open")

        return is_open


class TabBarWidget(Widget):
    """Tab bar container widget."""

    def __init__(self, widget_id: str, **props):
        """Initialize tab bar."""
        props["active_tab"] = None
        super().__init__(widget_id, **props)

    def render(self) -> str | None:
        """Render the tab bar."""
        flags = self.state.properties.get("flags", 0)

        if imgui.begin_tab_bar(self.widget_id, flags):
            # Tab items would be rendered here
            active_tab = self.state.properties.get("active_tab")
            imgui.end_tab_bar()
            return active_tab
        return None


class TabItemWidget(Widget):
    """Individual tab item widget."""

    def __init__(
        self,
        widget_id: str,
        label: str = "Tab",
        closable: bool = False,
        **props,
    ):
        """Initialize tab item."""
        props["label"] = label
        props["closable"] = closable
        props["is_open"] = True
        super().__init__(widget_id, **props)

    def render(self) -> bool:
        """Render the tab item."""
        label = self.state.properties.get("label", "Tab")
        closable = self.state.properties.get("closable", False)
        is_open = self.state.properties.get("is_open", True)
        flags = self.state.properties.get("flags", 0)

        if not is_open:
            return False

        if closable:
            selected, is_open = imgui.begin_tab_item(label, True, flags)
            self.state.properties["is_open"] = is_open
        else:
            selected, _ = imgui.begin_tab_item(label, None, flags)

        if selected:
            # Tab content would be rendered here
            imgui.end_tab_item()
            self.trigger_callback("on_select")

        return selected


class SeparatorWidget(Widget):
    """Separator line widget."""

    def __init__(self, widget_id: str, vertical: bool = False, **props):
        """Initialize separator."""
        props["vertical"] = vertical
        super().__init__(widget_id, **props)

    def render(self) -> None:
        """Render the separator."""
        vertical = self.state.properties.get("vertical", False)

        if vertical:
            imgui.separator_text("")  # Vertical separator
        else:
            imgui.separator()


class SpacingWidget(Widget):
    """Spacing widget for layout."""

    def __init__(self, widget_id: str, count: int = 1, **props):
        """Initialize spacing widget."""
        props["count"] = count
        super().__init__(widget_id, **props)

    def render(self) -> None:
        """Render spacing."""
        count = self.state.properties.get("count", 1)
        for _ in range(count):
            imgui.spacing()


class DummyWidget(Widget):
    """Dummy (blank space) widget."""

    def __init__(
        self,
        widget_id: str,
        size: tuple[float, float] = (0, 0),
        **props,
    ):
        """Initialize dummy widget."""
        props["size"] = size
        super().__init__(widget_id, **props)

    def render(self) -> None:
        """Render dummy space."""
        size = self.state.properties.get("size", (0, 0))
        imgui.dummy(imgui.ImVec2(*size))
