# Champi-Gen-UI 🎨

> **Generative UI for LLMs through ImGui and Python**

An MCP (Model Context Protocol) server that enables Large Language Models to create sophisticated user interfaces using ImGui through natural language commands.

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.0+-green.svg)](https://github.com/jlowin/fastmcp)
[![ImGui Bundle](https://img.shields.io/badge/ImGui-Bundle-red.svg)](https://github.com/pthom/imgui_bundle)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## ✨ Features

- **200+ MCP Tools** for comprehensive UI creation
- **150+ Widget Types** from ImGui core and extensions
- **10+ Integrated Extensions** (plotting, node editing, file dialogs, etc.)
- **5 Canvas Modes** (standard, docking, multi-viewport, fullscreen, overlay)
- **Keyframe Animation System** with multiple easing functions
- **Data Binding** for reactive UI updates
- **JSON Serialization** for saving/loading UI definitions
- **Code Generation** to export standalone Python scripts
- **Template System** for reusable UI patterns

---

## 🚀 Quick Start

### Installation

```bash
# Using UV (recommended)
uv pip install champi-gen-ui

# Or with pip
pip install champi-gen-ui
```

### Running the MCP Server

```bash
champi-gen-ui serve
```

### MCP Client Configuration

Add to your MCP client configuration (e.g., `.mcp.json`):

```json
{
  "mcpServers": {
    "champi-gen-ui": {
      "command": "uv",
      "args": ["run", "champi-gen-ui", "serve"],
      "cwd": "/path/to/champi-gen-ui"
    }
  }
}
```

---

## 💡 Usage Examples

### Example 1: Simple Button
```
LLM: "Create a button that says 'Click Me'"

MCP executes:
- create_canvas(canvas_id="main")
- add_button(canvas_id="main", widget_id="btn1", label="Click Me")
```

### Example 2: Data Dashboard
```
LLM: "Create a dashboard with a line chart showing sales data and a data table below"

MCP executes:
- create_canvas(canvas_id="dashboard", mode="docking")
- add_line_plot(canvas_id="dashboard", plot_id="sales_chart", ...)
- create_table(canvas_id="dashboard", table_id="sales_table", ...)
- set_layout_vertical(canvas_id="dashboard")
```

### Example 3: Node Editor
```
LLM: "Create a node graph editor for a processing pipeline"

MCP executes:
- create_canvas(canvas_id="pipeline")
- create_node_editor(canvas_id="pipeline", editor_id="graph")
- add_node(editor_id="graph", node_id="input", title="Input")
- add_node(editor_id="graph", node_id="process", title="Process")
- add_link(editor_id="graph", from_pin="input.out", to_pin="process.in")
```

---

## 📚 Documentation

Comprehensive documentation is available in the `/docs` directory:

### Core Documentation
- **[IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md)** - Complete implementation roadmap
- **[PLAN_SUMMARY.md](PLAN_SUMMARY.md)** - Executive summary
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System architecture

### Reference Guides
- **[WIDGET_CATALOG.md](docs/WIDGET_CATALOG.md)** - All 150+ widgets documented
- **[MCP_TOOLS_API.md](docs/MCP_TOOLS_API.md)** - Complete API for 200+ MCP tools
- **[EXTENSIONS_GUIDE.md](docs/EXTENSIONS_GUIDE.md)** - Third-party extension integration
- **[IMGUI_CORE_REFERENCE.md](docs/IMGUI_CORE_REFERENCE.md)** - ImGui API reference

---

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│             LLM                     │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│        MCP Client                   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│     FastMCP Server (200+ tools)     │
└──────────────┬──────────────────────┘
               │
    ┌──────────┴──────────┐
    │   Canvas Manager    │
    └──────────┬──────────┘
               │
               ▼
┌─────────────────────────────────────┐
│      Widget System                  │
├─────────────────────────────────────┤
│    Widget Registry (150+)           │
│    Animation Engine                 │
│    Layout Manager                   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│      ImGui Bundle                   │
│  - ImGui Core                       │
│  - ImPlot (plotting)                │
│  - Extensions (node editor, etc.)   │
└─────────────────────────────────────┘
```

---

## 🛠️ MCP Tool Categories

The server provides 200+ tools organized into 20 categories:

1. **Canvas Management** (7 tools)
2. **Basic Widgets** (25 tools)
3. **Container Widgets** (5 tools)
4. **Layout Tools** (10 tools)
5. **Styling & Theming** (12 tools)
6. **Animation Tools** (10 tools)
7. **File Dialog Tools** (5 tools)
8. **Notification Tools** (7 tools)
9. **Table Tools** (10 tools)
10. **Plotting Tools** (15 tools)
11. **Node Editor Tools** (10 tools)
12. **Text Editor Tools** (8 tools)
13. **Memory Editor Tools** (5 tools)
14. **Input Handling Tools** (10 tools)
15. **Drawing Tools** (15 tools)
16. **Data Binding Tools** (8 tools)
17. **Export/Import Tools** (8 tools)
18. **Custom Widgets** (10 tools)
19. **Advanced Features** (8 tools)
20. **Utility Tools** (7 tools)

See [MCP_TOOLS_API.md](docs/MCP_TOOLS_API.md) for complete documentation.

---

## 🧩 Supported Widgets

### Basic Widgets (25+)
Buttons, text labels, input fields, checkboxes, radio buttons, sliders, drag controls, combo boxes, list boxes, color pickers, and more.

### Data Visualization (15+)
Line charts, scatter plots, bar charts, histograms, heatmaps, pie charts, candlestick charts, and more (via ImPlot).

### Advanced Widgets (30+)
Tables, tree views, node graphs, syntax-highlighted text editors, file dialogs, notifications, memory editors, and more.

### Custom Widgets (10+)
Knobs, toggles, spinners, date pickers, time pickers, gradient editors, and community-contributed widgets.

See [WIDGET_CATALOG.md](docs/WIDGET_CATALOG.md) for the complete list.

---

## 🔌 Extensions

Champi-Gen-UI integrates 10+ powerful extensions:

- **imgui_club** - Memory editor, multi-context compositor
- **HImGuiAnimation** - Keyframe animation system
- **ImGuiFD** - Lightweight file dialogs
- **imgui-notify** - Toast notification system
- **ImPlot** - Advanced plotting library
- **ImNodes** - Node graph editing
- **ImGuiColorTextEdit** - Syntax-highlighted editor
- **imgui-markdown** - Markdown rendering
- And more!

See [EXTENSIONS_GUIDE.md](docs/EXTENSIONS_GUIDE.md) for details.

---

## 🖼️ Canvas Modes

1. **Standard** - Traditional window-based UI
2. **Docking** - Dockable window layout
3. **Multi-Viewport** - Multiple windows support
4. **Fullscreen** - Immersive full-screen mode
5. **Overlay** - Transparent overlay mode

---

## 💾 Data Persistence

### Export UI Definition
```python
export_ui_json(canvas_id="dashboard", file_path="dashboard.json")
```

### Import UI Definition
```python
import_ui_json(file_path="dashboard.json")
```

### Generate Python Code
```python
generate_code(canvas_id="dashboard", output_path="dashboard.py")
```

---

## ⚙️ Development

### Project Structure
```
champi-gen-ui/
├── src/champi_gen_ui/
│   ├── server/          # FastMCP server
│   ├── core/            # Core UI management
│   ├── canvas/          # Canvas rendering
│   ├── widgets/         # Widget library
│   ├── extensions/      # Third-party integrations
│   ├── animation/       # Animation system
│   ├── themes/          # Theming & styling
│   └── layout/          # Layout managers
├── docs/                # Documentation
├── examples/            # Usage examples
└── tests/               # Test suite
```

### Running Tests
```bash
# Install dev dependencies
uv sync --all-extras

# Run tests
pytest

# Run with coverage
pytest --cov=champi_gen_ui
```

### Linting & Formatting
```bash
# Format code
ruff format src/

# Lint code
ruff check src/
```

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup
```bash
# Clone repository
git clone https://github.com/yourusername/champi-gen-ui.git
cd champi-gen-ui

# Install with UV
uv sync --all-extras

# Run in development mode
uv run champi-gen-ui serve
```

---

## 📋 Requirements

- Python 3.12+
- imgui-bundle
- pyglm
- fastmcp
- blinker
- loguru

See [pyproject.toml](pyproject.toml) for complete dependencies.

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- **Dear ImGui** - Amazing immediate mode GUI library
- **imgui-bundle** - Comprehensive Python bindings
- **FastMCP** - Excellent MCP server framework
- **ImPlot** - Powerful plotting library
- **Community Extensions** - All the awesome widget creators

---

## 🔗 Related Projects

Part of the Champi project family:
- **[champi-signals](../champi-signals)** - Signal management and event processing
- **[champi-stt](../champi-stt)** - Multi-provider speech-to-text
- **[champi-tts](../champi-tts)** - Multi-provider text-to-speech
- **[champi-gen-ui](../champi-gen-ui)** - Generative UI (this project)

---

## 💬 Support

- 📚 [Documentation](docs/)
- 🐛 [Issue Tracker](https://github.com/yourusername/champi-gen-ui/issues)
- 💭 [Discussions](https://github.com/yourusername/champi-gen-ui/discussions)

---

## 🗺️ Roadmap

### Phase 1: Foundation ✅
- Project setup
- Basic canvas system
- Core widgets (10-15)

### Phase 2: Widget Library ✅
- Complete widget set (30+)
- Layout system
- Theming foundation

### Phase 3: Extensions ✅
- Extension integration
- Animation system
- File dialogs & notifications

### Phase 4: Advanced Features ✅
- Node editor
- Plotting library
- Data binding

### Phase 5: Polish ✅
- Template system
- Code generation
- Complete documentation

See [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) for detailed timeline.

---

## ⭐ Star History

If you find this project useful, please consider giving it a star!

---

**Built with ❤️ using ImGui, Python, and FastMCP**
