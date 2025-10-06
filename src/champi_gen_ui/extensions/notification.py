"""Notification system using imgui toast notifications."""

from dataclasses import dataclass
from enum import Enum

from imgui_bundle import imgui
from loguru import logger


class NotificationType(Enum):
    """Notification types."""

    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class Notification:
    """Notification data."""

    title: str
    message: str
    type: NotificationType
    duration: float = 3.0  # seconds
    dismissible: bool = True
    timestamp: float = 0.0
    visible: bool = True


class NotificationManager:
    """Manager for toast-style notifications."""

    def __init__(self, max_notifications: int = 5):
        """
        Initialize notification manager.

        Args:
            max_notifications: Maximum number of notifications to show
        """
        self.notifications: list[Notification] = []
        self.max_notifications = max_notifications
        self.notification_height = 80.0
        self.notification_width = 300.0
        self.padding = 10.0
        logger.debug("Initialized NotificationManager")

    def add(
        self,
        title: str,
        message: str,
        type: NotificationType = NotificationType.INFO,
        duration: float = 3.0,
        dismissible: bool = True,
    ) -> None:
        """
        Add a new notification.

        Args:
            title: Notification title
            message: Notification message
            type: Notification type
            duration: Display duration in seconds (0 for persistent)
            dismissible: Allow manual dismissal
        """
        notification = Notification(
            title=title,
            message=message,
            type=type,
            duration=duration,
            dismissible=dismissible,
            timestamp=imgui.get_time(),
        )

        self.notifications.append(notification)

        # Remove oldest if exceeding max
        if len(self.notifications) > self.max_notifications:
            self.notifications.pop(0)

        logger.debug(f"Added notification: {title} ({type.value})")

    def info(self, title: str, message: str, duration: float = 3.0) -> None:
        """Add info notification."""
        self.add(title, message, NotificationType.INFO, duration)

    def success(self, title: str, message: str, duration: float = 3.0) -> None:
        """Add success notification."""
        self.add(title, message, NotificationType.SUCCESS, duration)

    def warning(self, title: str, message: str, duration: float = 4.0) -> None:
        """Add warning notification."""
        self.add(title, message, NotificationType.WARNING, duration)

    def error(self, title: str, message: str, duration: float = 5.0) -> None:
        """Add error notification."""
        self.add(title, message, NotificationType.ERROR, duration)

    def render(self) -> None:
        """Render all active notifications."""
        current_time = imgui.get_time()
        viewport = imgui.get_main_viewport()
        size = viewport.size

        # Remove expired notifications
        self.notifications = [
            n
            for n in self.notifications
            if n.visible
            and (n.duration == 0 or current_time - n.timestamp < n.duration)
        ]

        # Render notifications from bottom-right
        y_offset = size.y - self.padding
        for i, notification in enumerate(reversed(self.notifications)):
            y_offset -= self.notification_height + self.padding
            x_pos = size.x - self.notification_width - self.padding

            self._render_notification(notification, x_pos, y_offset, i)

    def _render_notification(
        self, notification: Notification, x: float, y: float, index: int
    ) -> None:
        """Render a single notification."""
        window_id = f"##notification_{index}"

        # Set position and size
        imgui.set_next_window_pos(imgui.ImVec2(x, y))
        imgui.set_next_window_size(
            imgui.ImVec2(self.notification_width, self.notification_height)
        )

        # Window flags
        flags = (
            imgui.WindowFlags_.no_decoration
            | imgui.WindowFlags_.no_move
            | imgui.WindowFlags_.no_saved_settings
            | imgui.WindowFlags_.no_focus_on_appearing
            | imgui.WindowFlags_.no_nav
        )

        # Get colors for notification type
        bg_color, text_color = self._get_notification_colors(notification.type)

        # Push style colors
        imgui.push_style_color(imgui.Col_.window_bg, bg_color)
        imgui.push_style_color(imgui.Col_.text, text_color)

        if imgui.begin(window_id, None, flags):
            # Title
            imgui.push_font(imgui.get_io().fonts.fonts[0])  # Bold font if available
            imgui.text(notification.title)
            imgui.pop_font()

            imgui.spacing()

            # Message (wrapped)
            imgui.push_text_wrap_pos(imgui.get_content_region_avail().x)
            imgui.text(notification.message)
            imgui.pop_text_wrap_pos()

            # Close button if dismissible
            if notification.dismissible:
                imgui.same_line()
                imgui.set_cursor_pos_x(
                    imgui.get_window_width() - 30
                )  # Position at top-right
                if imgui.small_button("X##" + window_id):
                    notification.visible = False

        imgui.end()
        imgui.pop_style_color(2)

    def _get_notification_colors(
        self, type: NotificationType
    ) -> tuple[tuple[float, float, float, float], tuple[float, float, float, float]]:
        """Get background and text colors for notification type."""
        if type == NotificationType.INFO:
            return (0.2, 0.4, 0.8, 0.95), (1.0, 1.0, 1.0, 1.0)  # Blue
        elif type == NotificationType.SUCCESS:
            return (0.2, 0.7, 0.3, 0.95), (1.0, 1.0, 1.0, 1.0)  # Green
        elif type == NotificationType.WARNING:
            return (0.9, 0.7, 0.2, 0.95), (0.1, 0.1, 0.1, 1.0)  # Yellow/Orange
        elif type == NotificationType.ERROR:
            return (0.8, 0.2, 0.2, 0.95), (1.0, 1.0, 1.0, 1.0)  # Red
        else:
            return (0.3, 0.3, 0.3, 0.95), (1.0, 1.0, 1.0, 1.0)  # Gray

    def clear_all(self) -> None:
        """Clear all notifications."""
        self.notifications.clear()
        logger.debug("Cleared all notifications")

    def get_notification_count(self) -> int:
        """Get the number of active notifications."""
        return len(self.notifications)


class NotificationWidget:
    """Widget for displaying a notification area."""

    def __init__(self, manager: NotificationManager):
        """
        Initialize notification widget.

        Args:
            manager: NotificationManager instance
        """
        self.manager = manager

    def render(self) -> None:
        """Render the notification area."""
        self.manager.render()


# Simple inline notification widget
class InlineNotification:
    """Inline notification that can be embedded in UI."""

    def __init__(
        self,
        message: str = "",
        type: NotificationType = NotificationType.INFO,
        visible: bool = True,
    ):
        """Initialize inline notification."""
        self.message = message
        self.type = type
        self.visible = visible

    def render(self) -> None:
        """Render inline notification."""
        if not self.visible or not self.message:
            return

        # Get colors
        bg_color, text_color = self._get_colors()

        # Render with colored background
        imgui.push_style_color(imgui.Col_.child_bg, bg_color)
        imgui.push_style_color(imgui.Col_.text, text_color)

        if imgui.begin_child(
            "##inline_notification",
            imgui.ImVec2(-1, 60),
            True,
            imgui.WindowFlags_.no_scrollbar,
        ):
            imgui.spacing()
            imgui.indent(10)
            imgui.push_text_wrap_pos(imgui.get_content_region_avail().x - 10)
            imgui.text(self.message)
            imgui.pop_text_wrap_pos()
            imgui.unindent(10)

        imgui.end_child()
        imgui.pop_style_color(2)

    def _get_colors(
        self,
    ) -> tuple[tuple[float, float, float, float], tuple[float, float, float, float]]:
        """Get colors based on notification type."""
        if self.type == NotificationType.INFO:
            return (0.2, 0.4, 0.8, 0.3), (0.8, 0.9, 1.0, 1.0)
        elif self.type == NotificationType.SUCCESS:
            return (0.2, 0.7, 0.3, 0.3), (0.8, 1.0, 0.8, 1.0)
        elif self.type == NotificationType.WARNING:
            return (0.9, 0.7, 0.2, 0.3), (0.1, 0.1, 0.1, 1.0)
        elif self.type == NotificationType.ERROR:
            return (0.8, 0.2, 0.2, 0.3), (1.0, 0.8, 0.8, 1.0)
        else:
            return (0.3, 0.3, 0.3, 0.3), (1.0, 1.0, 1.0, 1.0)

    def set_message(self, message: str, type: NotificationType = None) -> None:
        """Update notification message."""
        self.message = message
        if type:
            self.type = type
        self.visible = True

    def hide(self) -> None:
        """Hide the notification."""
        self.visible = False

    def show(self) -> None:
        """Show the notification."""
        self.visible = True
