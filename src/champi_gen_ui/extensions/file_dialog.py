"""File dialog integration using imgui_bundle's portable file dialogs."""

from collections.abc import Callable

from imgui_bundle import imgui, portable_file_dialogs
from loguru import logger

from champi_gen_ui.core.widget import Widget


class FileDialogMode:
    """File dialog modes."""

    OPEN_FILE = "open_file"
    OPEN_FOLDER = "open_folder"
    SAVE_FILE = "save_file"
    SELECT_MULTIPLE = "select_multiple"


class FileDialog:
    """Wrapper for portable file dialogs."""

    def __init__(self):
        """Initialize file dialog."""
        self.current_dialog: portable_file_dialogs.open_file | None = None
        self.result_callback: Callable | None = None
        logger.debug("Initialized FileDialog")

    def open_file(
        self,
        title: str = "Open File",
        filters: list[str] | None = None,
        initial_path: str = "",
        callback: Callable | None = None,
    ) -> None:
        """
        Open a file selection dialog.

        Args:
            title: Dialog title
            filters: File filters (e.g., ["*.txt", "*.py"])
            initial_path: Initial directory path
            callback: Callback function for result
        """
        try:
            self.result_callback = callback
            self.current_dialog = portable_file_dialogs.open_file(
                title=title,
                initial_path=initial_path,
                filters=filters or [],
                opt=portable_file_dialogs.opt.none,
            )
            logger.debug(f"Opened file dialog: {title}")
        except Exception as e:
            logger.error(f"Error opening file dialog: {e}")

    def open_folder(
        self,
        title: str = "Select Folder",
        initial_path: str = "",
        callback: Callable | None = None,
    ) -> None:
        """
        Open a folder selection dialog.

        Args:
            title: Dialog title
            initial_path: Initial directory path
            callback: Callback function for result
        """
        try:
            self.result_callback = callback
            self.current_dialog = portable_file_dialogs.select_folder(
                title=title,
                initial_path=initial_path,
            )
            logger.debug(f"Opened folder dialog: {title}")
        except Exception as e:
            logger.error(f"Error opening folder dialog: {e}")

    def save_file(
        self,
        title: str = "Save File",
        filters: list[str] | None = None,
        initial_path: str = "",
        callback: Callable | None = None,
    ) -> None:
        """
        Open a save file dialog.

        Args:
            title: Dialog title
            filters: File filters
            initial_path: Initial directory path
            callback: Callback function for result
        """
        try:
            self.result_callback = callback
            self.current_dialog = portable_file_dialogs.save_file(
                title=title,
                initial_path=initial_path,
                filters=filters or [],
                opt=portable_file_dialogs.opt.none,
            )
            logger.debug(f"Opened save dialog: {title}")
        except Exception as e:
            logger.error(f"Error opening save dialog: {e}")

    def update(self) -> str | None:
        """
        Update dialog state and check for results.

        Returns:
            Selected file path if ready, None otherwise
        """
        if not self.current_dialog:
            return None

        if self.current_dialog.ready():
            result = self.current_dialog.result()
            if result and self.result_callback:
                self.result_callback(result)
            self.current_dialog = None
            self.result_callback = None
            return result

        return None

    def is_active(self) -> bool:
        """Check if a dialog is currently active."""
        return self.current_dialog is not None


class FileDialogWidget(Widget):
    """Widget wrapper for file dialogs."""

    def __init__(
        self,
        widget_id: str,
        button_label: str = "Browse...",
        mode: str = FileDialogMode.OPEN_FILE,
        title: str = "Select File",
        filters: list[str] | None = None,
        **props,
    ):
        """
        Initialize file dialog widget.

        Args:
            widget_id: Unique widget identifier
            button_label: Label for the browse button
            mode: Dialog mode (open_file, open_folder, save_file)
            title: Dialog title
            filters: File filters
        """
        props["button_label"] = button_label
        props["mode"] = mode
        props["title"] = title
        props["filters"] = filters or []
        props["selected_path"] = ""
        props["dialog_open"] = False
        super().__init__(widget_id, **props)
        self.file_dialog = FileDialog()

    def render(self) -> str | None:
        """
        Render the file dialog widget.

        Returns:
            Selected path if changed, None otherwise
        """
        button_label = self.state.properties.get("button_label", "Browse...")
        selected_path = self.state.properties.get("selected_path", "")
        dialog_open = self.state.properties.get("dialog_open", False)

        # Display current path
        if selected_path:
            imgui.text(f"Selected: {selected_path}")
            imgui.same_line()

        # Browse button
        if imgui.button(button_label):
            self._open_dialog()
            self.state.properties["dialog_open"] = True

        # Update dialog state
        if dialog_open:
            result = self.file_dialog.update()
            if result:
                self.state.properties["selected_path"] = str(result)
                self.state.properties["dialog_open"] = False
                self.trigger_callback("on_select", str(result))
                return str(result)

        return None

    def _open_dialog(self) -> None:
        """Open the appropriate dialog based on mode."""
        mode = self.state.properties.get("mode", FileDialogMode.OPEN_FILE)
        title = self.state.properties.get("title", "Select File")
        filters = self.state.properties.get("filters", [])

        if mode == FileDialogMode.OPEN_FILE:
            self.file_dialog.open_file(title=title, filters=filters)
        elif mode == FileDialogMode.OPEN_FOLDER:
            self.file_dialog.open_folder(title=title)
        elif mode == FileDialogMode.SAVE_FILE:
            self.file_dialog.save_file(title=title, filters=filters)

    def get_selected_path(self) -> str:
        """Get the currently selected path."""
        return self.state.properties.get("selected_path", "")

    def set_filters(self, filters: list[str]) -> None:
        """Set file filters."""
        self.state.properties["filters"] = filters


class MessageDialog:
    """Simple message/notification dialogs."""

    @staticmethod
    def info(title: str, message: str) -> None:
        """Show info message."""
        try:
            portable_file_dialogs.message(
                title=title,
                message=message,
                choice=portable_file_dialogs.choice.ok,
                icon=portable_file_dialogs.icon.info,
            )
        except Exception as e:
            logger.error(f"Error showing info dialog: {e}")

    @staticmethod
    def warning(title: str, message: str) -> None:
        """Show warning message."""
        try:
            portable_file_dialogs.message(
                title=title,
                message=message,
                choice=portable_file_dialogs.choice.ok,
                icon=portable_file_dialogs.icon.warning,
            )
        except Exception as e:
            logger.error(f"Error showing warning dialog: {e}")

    @staticmethod
    def error(title: str, message: str) -> None:
        """Show error message."""
        try:
            portable_file_dialogs.message(
                title=title,
                message=message,
                choice=portable_file_dialogs.choice.ok,
                icon=portable_file_dialogs.icon.error,
            )
        except Exception as e:
            logger.error(f"Error showing error dialog: {e}")

    @staticmethod
    def question(title: str, message: str) -> bool:
        """
        Show yes/no question dialog.

        Returns:
            True if yes was clicked, False otherwise
        """
        try:
            result = portable_file_dialogs.message(
                title=title,
                message=message,
                choice=portable_file_dialogs.choice.yes_no,
                icon=portable_file_dialogs.icon.question,
            )
            return (
                result.ready() and result.result() == portable_file_dialogs.button.yes
            )
        except Exception as e:
            logger.error(f"Error showing question dialog: {e}")
            return False


class InputDialog:
    """Text input dialog."""

    @staticmethod
    def prompt(title: str, message: str, default_value: str = "") -> str | None:
        """
        Show text input dialog.

        Args:
            title: Dialog title
            message: Prompt message
            default_value: Default input value

        Returns:
            Input text if OK was clicked, None if cancelled
        """
        try:
            dialog = portable_file_dialogs.input(
                title=title,
                message=message,
                default_input=default_value,
            )
            if dialog.ready():
                result = dialog.result()
                return result if result else None
            return None
        except Exception as e:
            logger.error(f"Error showing input dialog: {e}")
            return None
