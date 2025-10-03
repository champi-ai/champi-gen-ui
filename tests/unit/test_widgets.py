"""Unit tests for widget implementations."""

from champi_gen_ui.widgets.basic import (
    ButtonWidget,
    CheckboxWidget,
    InputTextWidget,
    TextWidget,
)
from champi_gen_ui.widgets.slider import SliderFloatWidget, SliderIntWidget


class TestButtonWidget:
    """Tests for ButtonWidget."""

    def test_creation(self):
        """Test button widget creation."""
        button = ButtonWidget(widget_id="btn1", label="Test Button")
        assert button.widget_id == "btn1"
        assert button.state.properties["label"] == "Test Button"

    def test_update_label(self):
        """Test updating button label."""
        button = ButtonWidget(widget_id="btn1", label="Original")
        button.update(label="Updated")
        assert button.state.properties["label"] == "Updated"

    def test_callback_registration(self):
        """Test callback registration."""
        button = ButtonWidget(widget_id="btn1", label="Test")
        callback_called = False

        def on_click():
            nonlocal callback_called
            callback_called = True

        button.register_callback("on_click", on_click)
        button.trigger_callback("on_click")
        assert callback_called

    def test_serialization(self):
        """Test widget serialization."""
        button = ButtonWidget(widget_id="btn1", label="Test", size=[100, 30])
        data = button.serialize()
        assert data["widget_id"] == "btn1"
        assert data["widget_type"] == "ButtonWidget"
        assert data["properties"]["label"] == "Test"


class TestTextWidget:
    """Tests for TextWidget."""

    def test_creation(self):
        """Test text widget creation."""
        text = TextWidget(widget_id="text1", text="Hello World")
        assert text.widget_id == "text1"
        assert text.state.properties["text"] == "Hello World"

    def test_with_color(self):
        """Test text with color."""
        text = TextWidget(widget_id="text1", text="Colored", color=[1.0, 0.0, 0.0, 1.0])
        assert text.state.properties["color"] == [1.0, 0.0, 0.0, 1.0]

    def test_wrapped_text(self):
        """Test wrapped text."""
        text = TextWidget(widget_id="text1", text="Long text", wrapped=True)
        assert text.state.properties["wrapped"] is True


class TestInputTextWidget:
    """Tests for InputTextWidget."""

    def test_creation(self):
        """Test input text widget creation."""
        input_field = InputTextWidget(widget_id="input1", label="Name", value="Initial")
        assert input_field.widget_id == "input1"
        assert input_field.get_value() == "Initial"

    def test_set_value(self):
        """Test setting input value."""
        input_field = InputTextWidget(widget_id="input1", value="")
        input_field.set_value("New Value")
        assert input_field.get_value() == "New Value"

    def test_multiline(self):
        """Test multiline input."""
        input_field = InputTextWidget(
            widget_id="input1", label="Comment", multiline=True
        )
        assert input_field.state.properties["multiline"] is True


class TestCheckboxWidget:
    """Tests for CheckboxWidget."""

    def test_creation(self):
        """Test checkbox creation."""
        checkbox = CheckboxWidget(widget_id="check1", label="Enable", checked=True)
        assert checkbox.get_checked() is True

    def test_set_checked(self):
        """Test setting checked state."""
        checkbox = CheckboxWidget(widget_id="check1", checked=False)
        checkbox.set_checked(True)
        assert checkbox.get_checked() is True

    def test_callback_on_change(self):
        """Test checkbox change callback."""
        checkbox = CheckboxWidget(widget_id="check1", checked=False)
        changed_value = None

        def on_change(value):
            nonlocal changed_value
            changed_value = value

        checkbox.register_callback("on_change", on_change)
        # Would need to simulate ImGui interaction to test fully


class TestSliderIntWidget:
    """Tests for SliderIntWidget."""

    def test_creation(self):
        """Test integer slider creation."""
        slider = SliderIntWidget(
            widget_id="slider1", label="Volume", value=50, v_min=0, v_max=100
        )
        assert slider.get_value() == 50
        assert slider.state.properties["v_min"] == 0
        assert slider.state.properties["v_max"] == 100

    def test_set_value(self):
        """Test setting slider value."""
        slider = SliderIntWidget(widget_id="slider1", value=0, v_min=0, v_max=100)
        slider.set_value(75)
        assert slider.get_value() == 75


class TestSliderFloatWidget:
    """Tests for SliderFloatWidget."""

    def test_creation(self):
        """Test float slider creation."""
        slider = SliderFloatWidget(
            widget_id="slider1", label="Volume", value=0.5, v_min=0.0, v_max=1.0
        )
        assert slider.get_value() == 0.5

    def test_set_value(self):
        """Test setting slider value."""
        slider = SliderFloatWidget(widget_id="slider1", value=0.0, v_min=0.0, v_max=1.0)
        slider.set_value(0.75)
        assert slider.get_value() == 0.75


class TestWidgetVisibility:
    """Tests for widget visibility and enabled state."""

    def test_set_visible(self):
        """Test setting widget visibility."""
        button = ButtonWidget(widget_id="btn1", label="Test")
        assert button.state.visible is True
        button.set_visible(False)
        assert button.state.visible is False

    def test_set_enabled(self):
        """Test setting widget enabled state."""
        button = ButtonWidget(widget_id="btn1", label="Test")
        assert button.state.enabled is True
        button.set_enabled(False)
        assert button.state.enabled is False


class TestWidgetPosition:
    """Tests for widget positioning."""

    def test_set_position(self):
        """Test setting widget position."""
        button = ButtonWidget(widget_id="btn1", label="Test")
        button.set_position(100, 200)
        assert button.state.position == (100, 200)

    def test_set_size(self):
        """Test setting widget size."""
        button = ButtonWidget(widget_id="btn1", label="Test")
        button.set_size(150, 40)
        assert button.state.size == (150, 40)
