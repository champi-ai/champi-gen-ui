"""JSON serialization for UI export/import."""

import json
from pathlib import Path
from typing import Any

from loguru import logger


class UISerializer:
    """Serializer for UI components."""

    @staticmethod
    def serialize_canvas(canvas) -> dict[str, Any]:
        """
        Serialize a canvas to dictionary.

        Args:
            canvas: Canvas instance

        Returns:
            Dictionary representation
        """
        return {
            "type": "canvas",
            "id": canvas.canvas_id,
            "state": {
                "title": canvas.state.title,
                "width": canvas.state.width,
                "height": canvas.state.height,
                "mode": canvas.state.mode.value,
                "background_color": canvas.state.background_color,
            },
            "widgets": [
                UISerializer.serialize_widget(widget)
                for widget in canvas.widget_registry.get_all().values()
            ],
            "metadata": {
                "version": "1.0.0",
                "created_with": "champi-gen-ui",
            },
        }

    @staticmethod
    def serialize_widget(widget) -> dict[str, Any]:
        """
        Serialize a widget to dictionary.

        Args:
            widget: Widget instance

        Returns:
            Dictionary representation
        """
        return {
            "type": "widget",
            "widget_type": widget.__class__.__name__,
            "id": widget.widget_id,
            "state": {
                "visible": widget.state.visible,
                "enabled": widget.state.enabled,
                "position": widget.state.position,
                "size": widget.state.size,
                "properties": dict(widget.state.properties),
            },
            "callbacks": list(widget.state.callbacks.keys()),
        }

    @staticmethod
    def serialize_theme(theme) -> dict[str, Any]:
        """
        Serialize a theme to dictionary.

        Args:
            theme: Theme instance

        Returns:
            Dictionary representation
        """
        return {
            "type": "theme",
            "name": theme.name,
            "colors": {
                "window_bg": theme.colors.window_bg,
                "frame_bg": theme.colors.frame_bg,
                "button": theme.colors.button,
                "button_hovered": theme.colors.button_hovered,
                "button_active": theme.colors.button_active,
                "text": theme.colors.text,
                # Add more colors as needed
            },
            "style": {
                "window_rounding": theme.style.window_rounding,
                "frame_rounding": theme.style.frame_rounding,
                "window_padding": theme.style.window_padding,
                "frame_padding": theme.style.frame_padding,
                # Add more style properties as needed
            },
        }

    @staticmethod
    def deserialize_canvas(data: dict[str, Any], canvas_manager) -> Any:
        """
        Deserialize a canvas from dictionary.

        Args:
            data: Dictionary representation
            canvas_manager: CanvasManager instance

        Returns:
            Canvas instance
        """
        from champi_gen_ui.core.state import CanvasMode

        # Create canvas
        canvas = canvas_manager.create_canvas(
            canvas_id=data["id"],
            width=data["state"]["width"],
            height=data["state"]["height"],
            mode=CanvasMode(data["state"]["mode"]),
            title=data["state"]["title"],
        )

        # Deserialize widgets
        for widget_data in data.get("widgets", []):
            widget = UISerializer.deserialize_widget(widget_data)
            if widget:
                canvas.add_widget(widget)

        return canvas

    @staticmethod
    def deserialize_widget(data: dict[str, Any]) -> Any:
        """
        Deserialize a widget from dictionary.

        Args:
            data: Dictionary representation

        Returns:
            Widget instance
        """
        # Dynamic widget creation based on type
        widget_type = data["widget_type"]
        widget_id = data["id"]
        properties = data["state"]["properties"]

        # Import widget classes dynamically
        try:
            from champi_gen_ui import widgets

            widget_class = getattr(widgets, widget_type)
            widget = widget_class(widget_id, **properties)

            # Restore state
            widget.state.visible = data["state"]["visible"]
            widget.state.enabled = data["state"]["enabled"]
            if data["state"]["position"]:
                widget.state.position = tuple(data["state"]["position"])
            if data["state"]["size"]:
                widget.state.size = tuple(data["state"]["size"])

            return widget
        except Exception as e:
            logger.error(f"Error deserializing widget {widget_type}: {e}")
            return None


class UIExporter:
    """Export UI to various formats."""

    @staticmethod
    def export_to_json(canvas, filepath: str, pretty: bool = True) -> bool:
        """
        Export canvas to JSON file.

        Args:
            canvas: Canvas instance
            filepath: Output file path
            pretty: Pretty print JSON

        Returns:
            True if successful
        """
        try:
            data = UISerializer.serialize_canvas(canvas)

            with open(filepath, "w") as f:
                if pretty:
                    json.dump(data, f, indent=2)
                else:
                    json.dump(data, f)

            logger.info(f"Exported UI to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error exporting to JSON: {e}")
            return False

    @staticmethod
    def export_to_python(canvas, filepath: str) -> bool:
        """
        Export canvas to Python code.

        Args:
            canvas: Canvas instance
            filepath: Output file path

        Returns:
            True if successful
        """
        try:
            from champi_gen_ui.core.codegen import CodeGenerator

            code = CodeGenerator.generate_canvas_code(canvas)

            with open(filepath, "w") as f:
                f.write(code)

            logger.info(f"Exported UI to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error exporting to Python: {e}")
            return False

    @staticmethod
    def export_canvas_state(canvas) -> str:
        """
        Export canvas state as JSON string.

        Args:
            canvas: Canvas instance

        Returns:
            JSON string
        """
        data = UISerializer.serialize_canvas(canvas)
        return json.dumps(data, indent=2)


class UIImporter:
    """Import UI from various formats."""

    @staticmethod
    def import_from_json(filepath: str, canvas_manager) -> Any:
        """
        Import canvas from JSON file.

        Args:
            filepath: Input file path
            canvas_manager: CanvasManager instance

        Returns:
            Canvas instance
        """
        try:
            with open(filepath) as f:
                data = json.load(f)

            canvas = UISerializer.deserialize_canvas(data, canvas_manager)
            logger.info(f"Imported UI from {filepath}")
            return canvas
        except Exception as e:
            logger.error(f"Error importing from JSON: {e}")
            return None

    @staticmethod
    def import_from_dict(data: dict[str, Any], canvas_manager) -> Any:
        """
        Import canvas from dictionary.

        Args:
            data: Canvas data
            canvas_manager: CanvasManager instance

        Returns:
            Canvas instance
        """
        try:
            canvas = UISerializer.deserialize_canvas(data, canvas_manager)
            logger.info("Imported UI from dictionary")
            return canvas
        except Exception as e:
            logger.error(f"Error importing from dict: {e}")
            return None


class TemplateManager:
    """Manager for UI templates."""

    def __init__(self, templates_dir: str | None = None):
        """
        Initialize template manager.

        Args:
            templates_dir: Directory for template files
        """
        self.templates_dir = (
            Path(templates_dir) if templates_dir else Path("./templates")
        )
        self.templates: dict[str, dict[str, Any]] = {}
        logger.debug("Initialized TemplateManager")

    def save_template(self, name: str, canvas, description: str = "") -> bool:
        """
        Save canvas as a template.

        Args:
            name: Template name
            canvas: Canvas instance
            description: Template description

        Returns:
            True if successful
        """
        try:
            template_data = UISerializer.serialize_canvas(canvas)
            template_data["template_name"] = name
            template_data["description"] = description

            self.templates[name] = template_data

            # Save to file
            self.templates_dir.mkdir(exist_ok=True)
            filepath = self.templates_dir / f"{name}.json"

            with open(filepath, "w") as f:
                json.dump(template_data, f, indent=2)

            logger.info(f"Saved template: {name}")
            return True
        except Exception as e:
            logger.error(f"Error saving template: {e}")
            return False

    def load_template(self, name: str, canvas_manager) -> Any:
        """
        Load a template.

        Args:
            name: Template name
            canvas_manager: CanvasManager instance

        Returns:
            Canvas instance
        """
        try:
            # Try in-memory first
            if name in self.templates:
                return UISerializer.deserialize_canvas(
                    self.templates[name], canvas_manager
                )

            # Load from file
            filepath = self.templates_dir / f"{name}.json"
            if filepath.exists():
                with open(filepath) as f:
                    template_data = json.load(f)

                self.templates[name] = template_data
                return UISerializer.deserialize_canvas(template_data, canvas_manager)

            logger.warning(f"Template not found: {name}")
            return None
        except Exception as e:
            logger.error(f"Error loading template: {e}")
            return None

    def list_templates(self) -> list[dict[str, str]]:
        """
        List available templates.

        Returns:
            List of template info
        """
        templates = []

        # In-memory templates
        for name, data in self.templates.items():
            templates.append(
                {
                    "name": name,
                    "description": data.get("description", ""),
                    "source": "memory",
                }
            )

        # File-based templates
        if self.templates_dir.exists():
            for filepath in self.templates_dir.glob("*.json"):
                name = filepath.stem
                if name not in self.templates:
                    try:
                        with open(filepath) as f:
                            data = json.load(f)
                        templates.append(
                            {
                                "name": name,
                                "description": data.get("description", ""),
                                "source": "file",
                            }
                        )
                    except Exception as e:
                        logger.error(f"Error reading template {name}: {e}")

        return templates

    def delete_template(self, name: str) -> bool:
        """
        Delete a template.

        Args:
            name: Template name

        Returns:
            True if successful
        """
        try:
            # Remove from memory
            if name in self.templates:
                del self.templates[name]

            # Remove file
            filepath = self.templates_dir / f"{name}.json"
            if filepath.exists():
                filepath.unlink()

            logger.info(f"Deleted template: {name}")
            return True
        except Exception as e:
            logger.error(f"Error deleting template: {e}")
            return False
