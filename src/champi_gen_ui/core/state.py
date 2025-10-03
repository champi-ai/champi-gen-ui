"""State management for canvas and widgets."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

import blinker


class CanvasMode(Enum):
    """Canvas rendering modes."""

    STANDARD = "standard"
    DOCKING = "docking"
    MULTI_VIEWPORT = "multi_viewport"
    FULLSCREEN = "fullscreen"
    OVERLAY = "overlay"


@dataclass
class CanvasState:
    """State for a canvas."""

    canvas_id: str
    mode: CanvasMode = CanvasMode.STANDARD
    size: tuple[int, int] = (1280, 720)
    position: tuple[int, int] = (0, 0)
    theme: str = "dark"
    title: str = "ImGui Canvas"
    widgets: dict[str, "WidgetState"] = field(default_factory=dict)
    active: bool = True
    fps_idle: int = 10
    fps_active: int = 60

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "canvas_id": self.canvas_id,
            "mode": self.mode.value,
            "size": list(self.size),
            "position": list(self.position),
            "theme": self.theme,
            "title": self.title,
            "widgets": {wid: wstate.to_dict() for wid, wstate in self.widgets.items()},
            "active": self.active,
            "fps_idle": self.fps_idle,
            "fps_active": self.fps_active,
        }


@dataclass
class WidgetState:
    """State for a widget."""

    widget_id: str
    widget_type: str
    properties: dict[str, Any] = field(default_factory=dict)
    position: tuple[float, float] | None = None
    size: tuple[float, float] | None = None
    visible: bool = True
    enabled: bool = True
    parent: str | None = None
    children: list[str] = field(default_factory=list)
    callbacks: dict[str, str] = field(default_factory=dict)
    data_bindings: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "widget_id": self.widget_id,
            "widget_type": self.widget_type,
            "properties": self.properties.copy(),
            "position": list(self.position) if self.position else None,
            "size": list(self.size) if self.size else None,
            "visible": self.visible,
            "enabled": self.enabled,
            "parent": self.parent,
            "children": self.children.copy(),
            "callbacks": self.callbacks.copy(),
            "data_bindings": self.data_bindings.copy(),
        }


# Signals for state changes
widget_created = blinker.signal("widget-created")
widget_updated = blinker.signal("widget-updated")
widget_deleted = blinker.signal("widget-deleted")
canvas_updated = blinker.signal("canvas-updated")
state_changed = blinker.signal("state-changed")
