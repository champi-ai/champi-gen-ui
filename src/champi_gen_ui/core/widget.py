"""Base widget class and registry."""

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

from loguru import logger

from champi_gen_ui.core.state import WidgetState, widget_created, widget_updated


class Widget(ABC):
    """Base class for all widgets."""

    def __init__(self, widget_id: str, **props):
        """Initialize widget."""
        self.widget_id = widget_id
        self.state = WidgetState(
            widget_id=widget_id, widget_type=self.__class__.__name__, properties=props
        )
        self._callbacks: dict[str, Callable] = {}

    @abstractmethod
    def render(self) -> Any:
        """Render the widget using ImGui calls."""
        pass

    def update(self, **props) -> None:
        """Update widget properties."""
        self.state.properties.update(props)
        widget_updated.send(self, widget=self)
        logger.debug(f"Updated widget {self.widget_id} with {props}")

    def set_visible(self, visible: bool) -> None:
        """Set widget visibility."""
        self.state.visible = visible

    def set_enabled(self, enabled: bool) -> None:
        """Set widget enabled state."""
        self.state.enabled = enabled

    def set_position(self, x: float, y: float) -> None:
        """Set widget position."""
        self.state.position = (x, y)

    def set_size(self, width: float, height: float) -> None:
        """Set widget size."""
        self.state.size = (width, height)

    def register_callback(self, event: str, callback: Callable) -> None:
        """Register a callback function."""
        self._callbacks[event] = callback
        self.state.callbacks[event] = callback.__name__

    def trigger_callback(self, event: str, *args, **kwargs) -> Any:
        """Trigger a registered callback."""
        if event in self._callbacks:
            return self._callbacks[event](*args, **kwargs)
        return None

    def serialize(self) -> dict[str, Any]:
        """Serialize widget state to dictionary."""
        return self.state.to_dict()


class WidgetFactory:
    """Factory for creating widgets."""

    def __init__(self):
        """Initialize factory."""
        self._creators: dict[str, type[Widget]] = {}

    def register(self, widget_type: str, creator: type[Widget]) -> None:
        """Register a widget creator."""
        self._creators[widget_type] = creator
        logger.info(f"Registered widget type: {widget_type}")

    def create(self, widget_type: str, widget_id: str, **props) -> Widget:
        """Create a widget instance."""
        creator = self._creators.get(widget_type)
        if not creator:
            raise ValueError(f"Unknown widget type: {widget_type}")

        widget = creator(widget_id, **props)
        widget_created.send(self, widget=widget)
        logger.debug(f"Created widget {widget_id} of type {widget_type}")
        return widget

    def list_types(self) -> list[str]:
        """List all registered widget types."""
        return list(self._creators.keys())


class WidgetRegistry:
    """Registry for managing widget instances."""

    def __init__(self):
        """Initialize registry."""
        self._widgets: dict[str, Widget] = {}
        self._factory = WidgetFactory()

    @property
    def factory(self) -> WidgetFactory:
        """Get the widget factory."""
        return self._factory

    def add(self, widget: Widget) -> None:
        """Add a widget to the registry."""
        self._widgets[widget.widget_id] = widget
        logger.debug(f"Added widget {widget.widget_id} to registry")

    def get(self, widget_id: str) -> Widget | None:
        """Get a widget by ID."""
        return self._widgets.get(widget_id)

    def remove(self, widget_id: str) -> bool:
        """Remove a widget from the registry."""
        if widget_id in self._widgets:
            del self._widgets[widget_id]
            logger.debug(f"Removed widget {widget_id} from registry")
            return True
        return False

    def list(self) -> list[str]:
        """List all widget IDs."""
        return list(self._widgets.keys())

    def get_all(self) -> dict[str, Widget]:
        """Get all widgets."""
        return self._widgets.copy()

    def clear(self) -> None:
        """Clear all widgets."""
        self._widgets.clear()
        logger.debug("Cleared widget registry")
