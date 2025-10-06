"""Code generation for creating UI from specifications."""


class CodeGenerator:
    """Generator for Python code from UI components."""

    @staticmethod
    def generate_canvas_code(canvas) -> str:
        """
        Generate Python code for a canvas.

        Args:
            canvas: Canvas instance

        Returns:
            Python code as string
        """
        code_lines = [
            '"""Generated UI code."""',
            "",
            "from champi_gen_ui.core import Canvas, CanvasManager",
            "from champi_gen_ui.core.state import CanvasMode",
            "from champi_gen_ui.widgets import *",
            "from imgui_bundle import imgui",
            "",
            "",
            "def create_ui():",
            '    """Create the UI."""',
            "    # Create canvas manager",
            "    canvas_manager = CanvasManager()",
            "",
            f"    # Create canvas: {canvas.canvas_id}",
            "    canvas = canvas_manager.create_canvas(",
            f'        canvas_id="{canvas.canvas_id}",',
            f"        width={canvas.state.width},",
            f"        height={canvas.state.height},",
            f"        mode=CanvasMode.{canvas.state.mode.name},",
            f'        title="{canvas.state.title}",',
            "    )",
            "",
        ]

        # Generate widget creation code
        widgets = canvas.widget_registry.get_all().values()
        if widgets:
            code_lines.append("    # Create widgets")

        for widget in widgets:
            widget_code = CodeGenerator._generate_widget_code(widget, indent=1)
            code_lines.extend(widget_code)

        code_lines.extend(
            [
                "",
                "    return canvas",
                "",
                "",
                'if __name__ == "__main__":',
                "    canvas = create_ui()",
                "    # Run your application here",
            ]
        )

        return "\n".join(code_lines)

    @staticmethod
    def _generate_widget_code(widget, indent: int = 0) -> list[str]:
        """Generate code for a widget."""
        indent_str = "    " * indent
        widget_type = widget.__class__.__name__
        widget_id = widget.widget_id

        lines = [f"{indent_str}    # Create {widget_type}: {widget_id}"]

        # Build constructor arguments
        args = [f'"{widget_id}"']

        # Add common properties
        props = widget.state.properties
        for key, value in props.items():
            if value is not None:
                if isinstance(value, str):
                    args.append(f'{key}="{value}"')
                elif isinstance(value, list | tuple):
                    args.append(f"{key}={list(value)}")
                elif isinstance(value, bool | int | float):
                    args.append(f"{key}={value}")

        # Generate widget creation
        if len(args) <= 3:
            widget_line = f"{indent_str}    {widget_id.replace('.', '_')} = {widget_type}({', '.join(args)})"
        else:
            widget_line = (
                f"{indent_str}    {widget_id.replace('.', '_')} = {widget_type}("
            )
            lines.append(widget_line)
            for i, arg in enumerate(args):
                comma = "," if i < len(args) - 1 else ""
                lines.append(f"{indent_str}        {arg}{comma}")
            lines.append(f"{indent_str}    )")
            widget_line = None

        if widget_line:
            lines.append(widget_line)

        # Add to canvas
        lines.append(
            f"{indent_str}    canvas.add_widget({widget_id.replace('.', '_')})"
        )
        lines.append("")

        return lines

    @staticmethod
    def generate_widget_code_snippet(widget_type: str, widget_id: str, **kwargs) -> str:
        """
        Generate code snippet for a widget.

        Args:
            widget_type: Widget class name
            widget_id: Widget identifier
            **kwargs: Widget properties

        Returns:
            Code snippet
        """
        args = [f'"{widget_id}"']

        for key, value in kwargs.items():
            if isinstance(value, str):
                args.append(f'{key}="{value}"')
            elif isinstance(value, list | tuple):
                args.append(f"{key}={list(value)}")
            else:
                args.append(f"{key}={value}")

        return f"{widget_type}({', '.join(args)})"

    @staticmethod
    def generate_callback_code(callback_name: str, widget_id: str) -> str:
        """
        Generate callback function code.

        Args:
            callback_name: Callback name
            widget_id: Widget identifier

        Returns:
            Callback function code
        """
        return f"""
def {callback_name}_{widget_id.replace(".", "_")}(*args, **kwargs):
    '''Callback for {widget_id}.'''
    # Add your callback logic here
    print(f"Callback triggered: {callback_name}")
    print(f"Args: {{args}}")
    print(f"Kwargs: {{kwargs}}")
"""

    @staticmethod
    def generate_theme_code(theme) -> str:
        """
        Generate code for a theme.

        Args:
            theme: Theme instance

        Returns:
            Theme creation code
        """
        return f"""
from champi_gen_ui.themes.manager import Theme, ThemeColors, ThemeStyle

# Create theme: {theme.name}
theme = Theme(
    name="{theme.name}",
    colors=ThemeColors(
        window_bg={theme.colors.window_bg},
        frame_bg={theme.colors.frame_bg},
        button={theme.colors.button},
        button_hovered={theme.colors.button_hovered},
        button_active={theme.colors.button_active},
        text={theme.colors.text},
    ),
    style=ThemeStyle(
        window_rounding={theme.style.window_rounding},
        frame_rounding={theme.style.frame_rounding},
    ),
)
"""


class MarkupGenerator:
    """Generator for markup-based UI specifications."""

    @staticmethod
    def generate_yaml(canvas) -> str:
        """
        Generate YAML specification for a canvas.

        Args:
            canvas: Canvas instance

        Returns:
            YAML string
        """
        import yaml

        data = {
            "canvas": {
                "id": canvas.canvas_id,
                "title": canvas.state.title,
                "width": canvas.state.width,
                "height": canvas.state.height,
                "mode": canvas.state.mode.value,
            },
            "widgets": [
                {
                    "type": widget.__class__.__name__,
                    "id": widget.widget_id,
                    "properties": dict(widget.state.properties),
                }
                for widget in canvas.widget_registry.get_all().values()
            ],
        }

        return yaml.dump(data, default_flow_style=False, sort_keys=False)

    @staticmethod
    def generate_toml(canvas) -> str:
        """
        Generate TOML specification for a canvas.

        Args:
            canvas: Canvas instance

        Returns:
            TOML string
        """
        import toml

        data = {
            "canvas": {
                "id": canvas.canvas_id,
                "title": canvas.state.title,
                "width": canvas.state.width,
                "height": canvas.state.height,
                "mode": canvas.state.mode.value,
            },
            "widgets": {
                widget.widget_id: {
                    "type": widget.__class__.__name__,
                    "properties": dict(widget.state.properties),
                }
                for widget in canvas.widget_registry.get_all().values()
            },
        }

        return toml.dumps(data)


class TemplateCodeGenerator:
    """Generator for template-based code."""

    @staticmethod
    def generate_component_template(name: str, widgets: list[str]) -> str:
        """
        Generate a reusable component template.

        Args:
            name: Component name
            widgets: List of widget types

        Returns:
            Component code
        """
        component_name = "".join(word.capitalize() for word in name.split("_"))

        code = f"""
class {component_name}Component:
    '''Reusable {name} component.'''

    def __init__(self, component_id: str):
        self.component_id = component_id
        self.widgets = {{}}
        self._create_widgets()

    def _create_widgets(self):
        '''Create component widgets.'''
"""

        for i, widget_type in enumerate(widgets):
            widget_id = f"{{self.component_id}}.widget_{i}"
            code += f"        self.widgets['{widget_type.lower()}_{i}'] = {widget_type}('{widget_id}')\n"

        code += """
    def render(self, canvas):
        '''Render component on canvas.'''
        for widget in self.widgets.values():
            canvas.add_widget(widget)

    def get_widget(self, key: str):
        '''Get widget by key.'''
        return self.widgets.get(key)
"""

        return code

    @staticmethod
    def generate_form_template(fields: list[dict[str, str]]) -> str:
        """
        Generate a form template.

        Args:
            fields: List of field specifications

        Returns:
            Form code
        """
        code = """
class FormComponent:
    '''Auto-generated form component.'''

    def __init__(self, form_id: str):
        self.form_id = form_id
        self.fields = {}
        self._create_fields()

    def _create_fields(self):
        '''Create form fields.'''
"""

        for field in fields:
            field_name = field.get("name", "field")
            field_type = field.get("type", "InputTextWidget")
            label = field.get("label", field_name.title())

            code += f"""        self.fields['{field_name}'] = {field_type}(
            f'{{self.form_id}}.{field_name}',
            label='{label}'
        )
"""

        code += """
    def render(self, canvas):
        '''Render form on canvas.'''
        for field in self.fields.values():
            canvas.add_widget(field)

    def get_values(self):
        '''Get form values.'''
        return {
            name: widget.state.properties.get('value', '')
            for name, widget in self.fields.items()
        }

    def set_values(self, values: dict):
        '''Set form values.'''
        for name, value in values.items():
            if name in self.fields:
                self.fields[name].state.properties['value'] = value
"""

        return code
