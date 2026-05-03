#!/usr/bin/env python3
"""
Demonstration of creating UIs using Champi-Gen-UI MCP Tools

This script simulates how an LLM would use the MCP tools to create UIs.
In production, these tools are called via the MCP protocol by an LLM.
"""

from champi_gen_ui.server.main import (
    add_bar_chart,
    add_bullet_text,
    add_button,
    add_checkbox,
    add_collapsing_header,
    add_colored_text,
    add_input_text,
    add_line_chart,
    add_progress_bar,
    add_separator,
    add_slider_float,
    add_slider_int,
    add_text,
    apply_theme,
    create_canvas,
    export_canvas_json,
    generate_canvas_code,
    get_canvas_state,
    list_themes,
)


def print_result(operation, result):
    """Pretty print operation results."""
    success = result.get("success", False)
    symbol = "✓" if success else "✗"
    print(f"{symbol} {operation}")
    if not success and "error" in result:
        print(f"  Error: {result['error']}")


def main():
    print("\n" + "=" * 80)
    print("🎨 CHAMPI-GEN-UI MCP TOOLS DEMONSTRATION")
    print("=" * 80)
    print("\nThis demonstrates how to create UIs using MCP tools.")
    print("In production, an LLM would call these tools via the MCP protocol.\n")

    # Step 1: List available themes
    print("📋 Step 1: List Available Themes")
    print("-" * 80)
    result = list_themes()
    print_result("List themes", result)
    if result["success"]:
        themes = result["data"]["themes"]
        print(f"  Available: {', '.join(themes)}")
    print()

    # Step 2: Create a canvas
    print("🖼️  Step 2: Create Canvas")
    print("-" * 80)
    result = create_canvas(
        canvas_id="demo_ui",
        width=1000,
        height=800,
        mode="docking",
        title="🎨 MCP Generated Dashboard",
    )
    print_result("Create canvas 'demo_ui'", result)
    print()

    # Step 3: Apply theme
    print("🎨 Step 3: Apply Theme")
    print("-" * 80)
    result = apply_theme("Nord")
    print_result("Apply Nord theme", result)
    print()

    # Step 4: Add title
    print("✏️  Step 4: Add Title")
    print("-" * 80)
    result = add_colored_text(
        canvas_id="demo_ui",
        widget_id="title",
        text="🚀 Welcome to MCP-Generated UI!",
        color=[0.3, 0.7, 1.0, 1.0],
    )
    print_result("Add title text", result)
    print()

    # Step 5: Add description
    print("✏️  Step 5: Add Description")
    print("-" * 80)
    result = add_text(
        canvas_id="demo_ui",
        widget_id="description",
        text="This UI was created using MCP tools - no manual coding required!",
    )
    print_result("Add description", result)
    print()

    # Step 6: Add separator
    print("- Step 6: Add Separator")
    print("-" * 80)
    result = add_separator(canvas_id="demo_ui", widget_id="sep1")
    print_result("Add separator", result)
    print()

    # Step 7: Add collapsing header for input section
    print("📂 Step 7: Add Input Section")
    print("-" * 80)
    result = add_collapsing_header(
        canvas_id="demo_ui",
        widget_id="input_section",
        label="📝 User Input",
        default_open=True,
    )
    print_result("Add collapsing header", result)
    print()

    # Step 8: Add input fields
    print("📝 Step 8: Add Input Fields")
    print("-" * 80)
    result = add_input_text(
        canvas_id="demo_ui",
        widget_id="name_input",
        label="Name",
        value="",
        hint="Enter your name...",
    )
    print_result("Add name input", result)

    result = add_input_text(
        canvas_id="demo_ui",
        widget_id="email_input",
        label="Email",
        value="",
        hint="your@email.com",
    )
    print_result("Add email input", result)
    print()

    # Step 9: Add checkbox
    print("☑️  Step 9: Add Checkbox")
    print("-" * 80)
    result = add_checkbox(
        canvas_id="demo_ui",
        widget_id="subscribe",
        label="Subscribe to newsletter",
        checked=True,
    )
    print_result("Add checkbox", result)
    print()

    # Step 10: Add sliders section
    print("🎚️  Step 10: Add Sliders Section")
    print("-" * 80)
    result = add_separator(canvas_id="demo_ui", widget_id="sep2")
    print_result("Add separator", result)

    result = add_collapsing_header(
        canvas_id="demo_ui",
        widget_id="sliders_section",
        label="🎚️ Controls",
        default_open=True,
    )
    print_result("Add sliders header", result)

    result = add_slider_float(
        canvas_id="demo_ui",
        widget_id="volume_slider",
        label="Volume",
        value=0.75,
        v_min=0.0,
        v_max=1.0,
    )
    print_result("Add volume slider", result)

    result = add_slider_int(
        canvas_id="demo_ui",
        widget_id="brightness_slider",
        label="Brightness",
        value=80,
        v_min=0,
        v_max=100,
    )
    print_result("Add brightness slider", result)
    print()

    # Step 11: Add progress bars section
    print("📊 Step 11: Add Metrics Section")
    print("-" * 80)
    result = add_separator(canvas_id="demo_ui", widget_id="sep3")
    print_result("Add separator", result)

    result = add_collapsing_header(
        canvas_id="demo_ui",
        widget_id="metrics_section",
        label="📊 System Metrics",
        default_open=True,
    )
    print_result("Add metrics header", result)

    result = add_text(canvas_id="demo_ui", widget_id="cpu_label", text="CPU Usage:")
    print_result("Add CPU label", result)

    result = add_progress_bar(
        canvas_id="demo_ui", widget_id="cpu_bar", fraction=0.65, overlay="65%"
    )
    print_result("Add CPU progress bar", result)

    result = add_text(
        canvas_id="demo_ui", widget_id="memory_label", text="Memory Usage:"
    )
    print_result("Add memory label", result)

    result = add_progress_bar(
        canvas_id="demo_ui", widget_id="memory_bar", fraction=0.42, overlay="42%"
    )
    print_result("Add memory progress bar", result)
    print()

    # Step 12: Add charts section
    print("📈 Step 12: Add Data Visualization")
    print("-" * 80)
    result = add_separator(canvas_id="demo_ui", widget_id="sep4")
    print_result("Add separator", result)

    result = add_collapsing_header(
        canvas_id="demo_ui",
        widget_id="charts_section",
        label="📈 Data Visualization",
        default_open=True,
    )
    print_result("Add charts header", result)

    result = add_line_chart(
        canvas_id="demo_ui",
        widget_id="performance_chart",
        title="Performance Over Time",
        x_data=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        y_data=[20, 35, 28, 45, 52, 48, 65, 58, 72, 68],
    )
    print_result("Add line chart", result)

    result = add_bar_chart(
        canvas_id="demo_ui",
        widget_id="resources_chart",
        title="Resource Usage",
        values=[65.0, 42.0, 89.0, 52.0],
        labels=["CPU", "Memory", "Disk", "Network"],
    )
    print_result("Add bar chart", result)
    print()

    # Step 13: Add features list
    print("✨ Step 13: Add Features List")
    print("-" * 80)
    result = add_separator(canvas_id="demo_ui", widget_id="sep5")
    print_result("Add separator", result)

    result = add_colored_text(
        canvas_id="demo_ui",
        widget_id="features_header",
        text="✨ Key Features",
        color=[1.0, 0.8, 0.2, 1.0],
    )
    print_result("Add features header", result)

    features = [
        "200+ MCP Tools for comprehensive UI creation",
        "150+ Widget types from ImGui and extensions",
        "Multiple themes (Dark, Light, Nord, Dracula, etc.)",
        "Data binding for reactive updates",
        "Export to JSON or Python code",
    ]

    for i, feature in enumerate(features):
        result = add_bullet_text(
            canvas_id="demo_ui", widget_id=f"feature_{i}", text=feature
        )
        print_result(f"Add feature bullet {i+1}", result)
    print()

    # Step 14: Add action buttons
    print("🔘 Step 14: Add Action Buttons")
    print("-" * 80)
    result = add_separator(canvas_id="demo_ui", widget_id="sep6")
    print_result("Add separator", result)

    result = add_button(
        canvas_id="demo_ui", widget_id="submit_btn", label="Submit Form", size=[150, 40]
    )
    print_result("Add submit button", result)

    result = add_button(
        canvas_id="demo_ui",
        widget_id="refresh_btn",
        label="Refresh Data",
        size=[150, 40],
    )
    print_result("Add refresh button", result)
    print()

    # Step 15: Add status bar
    print("📌 Step 15: Add Status Bar")
    print("-" * 80)
    result = add_separator(canvas_id="demo_ui", widget_id="sep7")
    print_result("Add separator", result)

    result = add_colored_text(
        canvas_id="demo_ui",
        widget_id="status",
        text="✓ All systems operational | UI generated via MCP tools",
        color=[0.3, 1.0, 0.3, 1.0],
    )
    print_result("Add status text", result)
    print()

    # Step 16: Get canvas state
    print("🔍 Step 16: Get Canvas State")
    print("-" * 80)
    result = get_canvas_state("demo_ui")
    print_result("Get canvas state", result)
    if result["success"]:
        state = result["data"]
        print(f"  Canvas: {state['canvas_id']}")
        print(f"  Mode: {state['mode']}")
        print(f"  Size: {state['size']}")
        print(f"  Active: {state['active']}")
        print(f"  Widgets: {len(state['widgets'])} widgets created")
    print()

    # Step 17: Generate Python code
    print("💻 Step 17: Generate Python Code")
    print("-" * 80)
    result = generate_canvas_code("demo_ui")
    print_result("Generate Python code", result)
    if result["success"]:
        code = result["data"]["code"]
        print(f"  Generated {len(code)} characters of Python code")
        print("  Preview (first 200 chars):")
        print(f"  {code[:200]}...")
    print()

    # Step 18: Export to JSON
    print("💾 Step 18: Export to JSON")
    print("-" * 80)
    result = export_canvas_json(canvas_id="demo_ui", filepath="/tmp/demo_ui.json")
    print_result("Export canvas to JSON", result)
    print()

    # Summary
    print("=" * 80)
    print("✅ DEMONSTRATION COMPLETE!")
    print("=" * 80)
    print("\n📊 Summary:")
    print("  • Created a canvas in docking mode")
    print("  • Applied Nord theme")
    print("  • Added 30+ widgets of various types:")
    print("    - Text and colored text")
    print("    - Input fields and checkboxes")
    print("    - Sliders (float and int)")
    print("    - Progress bars")
    print("    - Line and bar charts")
    print("    - Buttons")
    print("    - Collapsing headers and separators")
    print("  • Generated Python code")
    print("  • Exported to JSON")
    print("\n🎯 Use Cases:")
    print("  1. Run as MCP server: champi-gen-ui serve")
    print("  2. Connect LLM client to MCP server")
    print("  3. Ask LLM: 'Create a dashboard with charts and controls'")
    print("  4. LLM uses these MCP tools to build the UI")
    print("\n💡 In a real deployment:")
    print("  • The canvas would render in a GUI window")
    print("  • Users could interact with sliders, buttons, inputs")
    print("  • Charts would display data visualizations")
    print("  • Themes would apply color schemes")
    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()
