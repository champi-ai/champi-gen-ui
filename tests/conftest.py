"""Pytest configuration and fixtures."""

import pytest

from champi_gen_ui.core.canvas import Canvas, CanvasManager
from champi_gen_ui.core.state import CanvasMode
from champi_gen_ui.core.widget import WidgetFactory, WidgetRegistry
from champi_gen_ui.widgets.basic import ButtonWidget, TextWidget
from champi_gen_ui.widgets.slider import SliderFloatWidget


@pytest.fixture
def widget_factory():
    """Create a widget factory with registered types."""
    factory = WidgetFactory()
    factory.register("button", ButtonWidget)
    factory.register("text", TextWidget)
    factory.register("slider_float", SliderFloatWidget)
    return factory


@pytest.fixture
def widget_registry(widget_factory):
    """Create a widget registry with factory."""
    registry = WidgetRegistry()
    registry._factory = widget_factory
    return registry


@pytest.fixture
def canvas():
    """Create a test canvas."""
    return Canvas(
        canvas_id="test_canvas",
        width=800,
        height=600,
        mode=CanvasMode.STANDARD,
        title="Test Canvas",
    )


@pytest.fixture
def canvas_manager():
    """Create a canvas manager."""
    return CanvasManager()


@pytest.fixture
def button_widget():
    """Create a test button widget."""
    return ButtonWidget(widget_id="test_button", label="Test Button")


@pytest.fixture
def text_widget():
    """Create a test text widget."""
    return TextWidget(widget_id="test_text", text="Test Text")
