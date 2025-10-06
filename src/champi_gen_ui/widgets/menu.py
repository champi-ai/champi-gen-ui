"""Menu and navigation widgets."""

from imgui_bundle import imgui

from champi_gen_ui.core.widget import Widget


class MenuBarWidget(Widget):
    """Main menu bar widget."""

    def __init__(self, widget_id: str, **props):
        """Initialize menu bar."""
        super().__init__(widget_id, **props)

    def render(self) -> bool:
        """Render the menu bar."""
        return imgui.begin_main_menu_bar()

    def end_render(self) -> None:
        """End menu bar rendering."""
        imgui.end_main_menu_bar()


class MenuWidget(Widget):
    """Menu item widget."""

    def __init__(
        self,
        widget_id: str,
        label: str = "Menu",
        enabled: bool = True,
        **props,
    ):
        """Initialize menu."""
        props["label"] = label
        props["enabled"] = enabled
        super().__init__(widget_id, **props)

    def render(self) -> bool:
        """Render the menu."""
        label = self.state.properties.get("label", "Menu")
        enabled = self.state.properties.get("enabled", True)

        return imgui.begin_menu(label, enabled)

    def end_render(self) -> None:
        """End menu rendering."""
        imgui.end_menu()


class MenuItemWidget(Widget):
    """Menu item widget."""

    def __init__(
        self,
        widget_id: str,
        label: str = "Item",
        shortcut: str | None = None,
        selected: bool = False,
        enabled: bool = True,
        **props,
    ):
        """Initialize menu item."""
        props["label"] = label
        props["shortcut"] = shortcut
        props["selected"] = selected
        props["enabled"] = enabled
        super().__init__(widget_id, **props)

    def render(self) -> tuple[bool, bool]:
        """Render the menu item."""
        label = self.state.properties.get("label", "Item")
        shortcut = self.state.properties.get("shortcut")
        selected = self.state.properties.get("selected", False)
        enabled = self.state.properties.get("enabled", True)

        clicked, selected = imgui.menu_item(label, shortcut, selected, enabled)

        if clicked:
            self.state.properties["selected"] = selected
            self.trigger_callback("on_click", selected)

        return clicked, selected


class TreeNodeWidget(Widget):
    """Tree node widget for hierarchical data."""

    def __init__(
        self,
        widget_id: str,
        label: str = "Node",
        default_open: bool = False,
        **props,
    ):
        """Initialize tree node."""
        props["label"] = label
        props["is_open"] = default_open
        super().__init__(widget_id, **props)

    def render(self) -> bool:
        """Render the tree node."""
        label = self.state.properties.get("label", "Node")
        flags = self.state.properties.get("flags", 0)

        is_open = imgui.tree_node_ex(label, flags)
        self.state.properties["is_open"] = is_open

        if is_open:
            self.trigger_callback("on_open")

        return is_open

    def end_render(self) -> None:
        """End tree node rendering."""
        if self.state.properties.get("is_open", False):
            imgui.tree_pop()


class SelectableWidget(Widget):
    """Selectable item widget."""

    def __init__(
        self,
        widget_id: str,
        label: str = "Selectable",
        selected: bool = False,
        **props,
    ):
        """Initialize selectable."""
        props["label"] = label
        props["selected"] = selected
        super().__init__(widget_id, **props)

    def render(self) -> tuple[bool, bool]:
        """Render the selectable."""
        label = self.state.properties.get("label", "Selectable")
        selected = self.state.properties.get("selected", False)
        flags = self.state.properties.get("flags", 0)
        size = self.state.properties.get("size", (0, 0))

        clicked, selected = imgui.selectable(
            label, selected, flags, imgui.ImVec2(*size)
        )

        if clicked:
            self.state.properties["selected"] = selected
            self.trigger_callback("on_select", selected)

        return clicked, selected


class TooltipWidget(Widget):
    """Tooltip widget."""

    def __init__(self, widget_id: str, text: str = "", **props):
        """Initialize tooltip."""
        props["text"] = text
        super().__init__(widget_id, **props)

    def render(self) -> None:
        """Render the tooltip."""
        text = self.state.properties.get("text", "")
        imgui.set_tooltip(text)


class PopupWidget(Widget):
    """Generic popup widget."""

    def __init__(
        self,
        widget_id: str,
        title: str = "Popup",
        modal: bool = False,
        **props,
    ):
        """Initialize popup."""
        props["title"] = title
        props["modal"] = modal
        props["is_open"] = False
        super().__init__(widget_id, **props)

    def open(self) -> None:
        """Open the popup."""
        self.state.properties["is_open"] = True
        imgui.open_popup(self.widget_id)

    def render(self) -> bool:
        """Render the popup."""
        title = self.state.properties.get("title", "Popup")
        modal = self.state.properties.get("modal", False)
        flags = self.state.properties.get("flags", 0)

        if modal:
            is_open, still_open = imgui.begin_popup_modal(title, True, flags)
            self.state.properties["is_open"] = still_open
        else:
            is_open = imgui.begin_popup(self.widget_id, flags)

        if is_open:
            # Popup content would be rendered here
            imgui.end_popup()

        return is_open

    def close(self) -> None:
        """Close the popup."""
        self.state.properties["is_open"] = False
        imgui.close_current_popup()


class ContextMenuWidget(Widget):
    """Context menu (right-click menu) widget."""

    def __init__(self, widget_id: str, **props):
        """Initialize context menu."""
        super().__init__(widget_id, **props)

    def render(self) -> bool:
        """Render the context menu."""
        popup_flags = self.state.properties.get("popup_flags", 1)
        return imgui.begin_popup_context_item(self.widget_id, popup_flags)

    def end_render(self) -> None:
        """End context menu rendering."""
        imgui.end_popup()
