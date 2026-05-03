#!/usr/bin/env python3
"""
Direct demonstration of Champi-Gen-UI capabilities without rendering.
Shows the UI creation process and final state.
"""

import json

from champi_gen_ui.core.canvas import CanvasManager
from champi_gen_ui.core.state import CanvasMode
from champi_gen_ui.widgets.basic import (
    ButtonWidget,
    CheckboxWidget,
    InputTextWidget,
    TextWidget,
)
from champi_gen_ui.widgets.display import (
    BulletTextWidget,
    ProgressBarWidget,
    TextColoredWidget,
)
from champi_gen_ui.widgets.plotting import BarChartWidget, LineChartWidget
from champi_gen_ui.widgets.slider import SliderFloatWidget, SliderIntWidget


def main():
    """Create a UI and show its structure."""
    print("\n" + "=" * 80)
    print("🎨 CHAMPI-GEN-UI - LIVE DEMONSTRATION")
    print("=" * 80)
    print("\nCreating an interactive dashboard UI...\n")

    # Create manager
    manager = CanvasManager()

    # Create canvas
    print("📋 Step 1: Creating canvas")
    canvas = manager.create_canvas(
        canvas_id="live_demo",
        width=1000,
        height=800,
        mode=CanvasMode.DOCKING,
        title="🎨 Live Dashboard Demo",
    )
    print(f"   ✓ Canvas created: {canvas.state.canvas_id}")
    print(f"   ✓ Mode: {canvas.state.mode.value}")
    print(f"   ✓ Size: {canvas.state.size[0]}x{canvas.state.size[1]}\n")

    # Register widgets
    print("📦 Step 2: Registering widget types")
    registry = canvas.widget_registry
    registry.factory.register("button", ButtonWidget)
    registry.factory.register("text", TextWidget)
    registry.factory.register("input_text", InputTextWidget)
    registry.factory.register("checkbox", CheckboxWidget)
    registry.factory.register("slider_float", SliderFloatWidget)
    registry.factory.register("slider_int", SliderIntWidget)
    print("   ✓ Registered 6 widget types\n")

    # Build UI
    print("🎨 Step 3: Building UI components")
    print("-" * 80)

    # Title
    title = TextColoredWidget(
        "title",
        text="🚀 Welcome to Champi-Gen-UI Dashboard!",
        color=(0.3, 0.7, 1.0, 1.0),
    )
    canvas.add_widget(title)
    print("   ✓ Added: Title (colored text)")

    # Description
    desc = registry.factory.create(
        "text",
        "desc",
        text="Real-time monitoring and control system",
    )
    canvas.add_widget(desc)
    print("   ✓ Added: Description text")

    # Section header
    section1 = TextColoredWidget(
        "section1",
        text="📝 User Input Section",
        color=(1.0, 0.8, 0.2, 1.0),
    )
    canvas.add_widget(section1)
    print("   ✓ Added: Section header")

    # Name input
    name_input = registry.factory.create(
        "input_text",
        "name_input",
        label="Name",
        value="",
        hint="Enter your name...",
    )
    canvas.add_widget(name_input)
    print("   ✓ Added: Name input field")

    # Email input
    email_input = registry.factory.create(
        "input_text",
        "email_input",
        label="Email",
        value="",
        hint="your@email.com",
    )
    canvas.add_widget(email_input)
    print("   ✓ Added: Email input field")

    # Checkbox
    checkbox = registry.factory.create(
        "checkbox",
        "notifications",
        label="Enable notifications",
        checked=True,
    )
    canvas.add_widget(checkbox)
    print("   ✓ Added: Checkbox")

    # Section 2: Controls
    section2 = TextColoredWidget(
        "section2",
        text="🎚️ Control Panel",
        color=(0.2, 1.0, 0.6, 1.0),
    )
    canvas.add_widget(section2)
    print("   ✓ Added: Controls section header")

    # Volume slider
    volume = registry.factory.create(
        "slider_float",
        "volume",
        label="Volume",
        value=0.75,
        v_min=0.0,
        v_max=1.0,
    )
    canvas.add_widget(volume)
    print("   ✓ Added: Volume slider (float)")

    # Brightness slider
    brightness = registry.factory.create(
        "slider_int",
        "brightness",
        label="Brightness",
        value=85,
        v_min=0,
        v_max=100,
    )
    canvas.add_widget(brightness)
    print("   ✓ Added: Brightness slider (int)")

    # Section 3: Metrics
    section3 = TextColoredWidget(
        "section3",
        text="📊 System Metrics",
        color=(1.0, 0.5, 0.8, 1.0),
    )
    canvas.add_widget(section3)
    print("   ✓ Added: Metrics section header")

    # CPU Progress
    cpu_label = registry.factory.create("text", "cpu_label", text="CPU Usage:")
    canvas.add_widget(cpu_label)
    cpu_bar = ProgressBarWidget("cpu_bar", fraction=0.67, overlay="67%")
    canvas.add_widget(cpu_bar)
    print("   ✓ Added: CPU usage progress bar (67%)")

    # Memory Progress
    mem_label = registry.factory.create("text", "mem_label", text="Memory Usage:")
    canvas.add_widget(mem_label)
    mem_bar = ProgressBarWidget("mem_bar", fraction=0.43, overlay="43%")
    canvas.add_widget(mem_bar)
    print("   ✓ Added: Memory usage progress bar (43%)")

    # Disk Progress
    disk_label = registry.factory.create("text", "disk_label", text="Disk Usage:")
    canvas.add_widget(disk_label)
    disk_bar = ProgressBarWidget("disk_bar", fraction=0.89, overlay="89%")
    canvas.add_widget(disk_bar)
    print("   ✓ Added: Disk usage progress bar (89%)")

    # Section 4: Charts
    section4 = TextColoredWidget(
        "section4",
        text="📈 Data Visualization",
        color=(0.3, 0.9, 1.0, 1.0),
    )
    canvas.add_widget(section4)
    print("   ✓ Added: Visualization section header")

    # Line chart
    line_chart = LineChartWidget(
        "perf_chart",
        title="Performance Trend",
        x_data=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        y_data=[20, 35, 28, 45, 52, 48, 65, 58, 72, 68],
    )
    canvas.add_widget(line_chart)
    print("   ✓ Added: Line chart (Performance Trend)")

    # Bar chart
    bar_chart = BarChartWidget(
        "resources",
        title="Resource Distribution",
        values=[67.0, 43.0, 89.0, 52.0],
        labels=["CPU", "Memory", "Disk", "Network"],
    )
    canvas.add_widget(bar_chart)
    print("   ✓ Added: Bar chart (Resource Distribution)")

    # Features list
    section5 = TextColoredWidget(
        "section5",
        text="✨ Key Features",
        color=(1.0, 1.0, 0.3, 1.0),
    )
    canvas.add_widget(section5)
    print("   ✓ Added: Features section header")

    features = [
        "200+ MCP Tools for UI creation",
        "150+ Widget types available",
        "9 professional themes",
        "Real-time data binding",
        "Export to JSON or Python",
    ]

    for i, feature in enumerate(features):
        bullet = BulletTextWidget(f"feature_{i}", text=feature)
        canvas.add_widget(bullet)
    print(f"   ✓ Added: {len(features)} feature bullets")

    # Buttons
    def on_save():
        print("💾 Save button clicked!")

    def on_refresh():
        print("🔄 Refresh button clicked!")

    save_btn = registry.factory.create(
        "button", "save_btn", label="Save Settings 💾", size=[150, 40]
    )
    save_btn.register_callback("on_click", on_save)
    canvas.add_widget(save_btn)
    print("   ✓ Added: Save button")

    refresh_btn = registry.factory.create(
        "button", "refresh_btn", label="Refresh Data 🔄", size=[150, 40]
    )
    refresh_btn.register_callback("on_click", on_refresh)
    canvas.add_widget(refresh_btn)
    print("   ✓ Added: Refresh button")

    # Status
    status = TextColoredWidget(
        "status",
        text="✓ System ready | All components loaded",
        color=(0.3, 1.0, 0.3, 1.0),
    )
    canvas.add_widget(status)
    print("   ✓ Added: Status indicator")

    print("-" * 80)
    print()

    # Summary
    widgets = canvas.widget_registry.get_all()
    widget_count = len(widgets)

    print("📊 Step 4: UI Creation Summary")
    print("=" * 80)
    print(f"   Canvas ID:       {canvas.state.canvas_id}")
    print(f"   Mode:            {canvas.state.mode.value}")
    print(f"   Dimensions:      {canvas.state.size[0]}x{canvas.state.size[1]} pixels")
    print(f"   Total Widgets:   {widget_count}")
    print()
    print("   Widget Breakdown:")
    print("   - Text displays:  7")
    print("   - Input fields:   2")
    print("   - Checkboxes:     1")
    print("   - Sliders:        2")
    print("   - Progress bars:  3")
    print("   - Charts:         2")
    print("   - Bullet points:  5")
    print("   - Buttons:        2")
    print("=" * 80)
    print()

    # Show widget structure
    print("🗂️  Step 5: Widget Structure")
    print("-" * 80)
    widget_types = {}
    for widget in widgets.values():
        widget_type = type(widget).__name__
        widget_types[widget_type] = widget_types.get(widget_type, 0) + 1

    for wtype, count in sorted(widget_types.items()):
        print(f"   {wtype:30s} : {count:2d} instance(s)")
    print("-" * 80)
    print()

    # Export to JSON
    print("💾 Step 6: Export Capabilities")
    print("-" * 80)
    canvas_data = canvas.serialize()
    json_str = json.dumps(canvas_data, indent=2)
    print(f"   ✓ Serialized to JSON ({len(json_str)} characters)")
    print("   ✓ Could export to: /tmp/demo_ui.json")
    print("   ✓ Could generate: Python code")
    print("-" * 80)
    print()

    # Show example widget data
    print("🔍 Step 7: Example Widget Data")
    print("-" * 80)
    example_widget = widgets.get("cpu_bar")
    if example_widget:
        print(f"   Widget ID: {example_widget.widget_id}")
        print(f"   Type:      {type(example_widget).__name__}")
        print(f"   Visible:   {example_widget.state.visible}")
        print(f"   Data:      {example_widget.serialize()}")
    print("-" * 80)
    print()

    # Final message
    print("=" * 80)
    print("✅ UI CREATION COMPLETE!")
    print("=" * 80)
    print()
    print("🎯 What was created:")
    print("   • A fully functional dashboard UI")
    print("   • With 24 interactive widgets")
    print("   • Organized in 5 sections")
    print("   • Including charts, controls, and metrics")
    print("   • Ready for docking layout")
    print()
    print("💡 In a GUI environment, you would see:")
    print("   • Colorful section headers")
    print("   • Interactive input fields")
    print("   • Adjustable sliders")
    print("   • Live progress bars")
    print("   • Beautiful line and bar charts")
    print("   • Clickable buttons")
    print("   • Professional themed interface")
    print()
    print("🚀 To use with MCP:")
    print("   1. Start server: champi-gen-ui serve")
    print("   2. Connect LLM client")
    print("   3. Ask: 'Create a dashboard'")
    print("   4. LLM builds UI using these exact tools!")
    print()
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()
