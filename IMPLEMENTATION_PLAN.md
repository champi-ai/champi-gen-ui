# Champi-Gen-UI: MCP Server for Generative UI with ImGui

## Overview
Build a Model Context Protocol (MCP) server that provides LLMs with generative UI capabilities through ImGui/Python, enabling real-time visual interface creation and manipulation.

---

## 1. Project Structure & Configuration

### 1.1 Dependencies Setup (pyproject.toml)
- **Core**: `fastmcp`, `imgui-bundle`, `pyglm`, `loguru`, `blinker`
- **Build**: `hatchling`, `uv`
- **Dev**: `pytest`, `pytest-asyncio`, `ruff`, `mypy`, `pre-commit`
- Follow champi-signals/champi-tts conventions for tooling config
- Use UV package manager exclusively
- Python >=3.12 requirement

### 1.2 Directory Structure
```
champi-gen-ui/
├── src/champi_gen_ui/
│   ├── server/           # FastMCP server implementation
│   ├── core/             # Core UI management
│   ├── canvas/           # Canvas rendering engine
│   ├── widgets/          # Widget library
│   ├── extensions/       # Third-party integrations
│   ├── animation/        # Animation system
│   ├── themes/           # Theming & styling
│   ├── layout/           # Layout managers
│   └── utils/            # Utilities
├── docs/                 # Reference documentation (MD files)
├── examples/             # Usage examples
└── tests/               # Test suite
```

---

## 2. Core Architecture

### 2.1 Canvas System (Mode-Based)
- **Canvas Manager**: Main rendering context
- **Viewport System**: Multi-viewport support
- **Rendering Loop**: ImGui render loop with FastMCP integration
- **State Management**: Canvas state persistence

**Modes**:
1. **Standard Canvas**: Traditional widget placement
2. **Docking Mode**: Dockable window layout
3. **Multi-Viewport**: Multi-window support
4. **Fullscreen**: Immersive UI mode
5. **Overlay**: Transparent overlay mode

### 2.2 Widget Registry System
- Dynamic widget registration
- Widget factory pattern
- Type-safe widget creation
- Widget templates/presets
- Widget serialization/deserialization

---

## 3. MCP Tools Architecture

### 3.1 Canvas Management Tools
1. **create_canvas**: Initialize new canvas
2. **update_canvas**: Modify canvas properties
3. **clear_canvas**: Reset canvas state
4. **get_canvas_state**: Retrieve current state
5. **set_canvas_mode**: Switch rendering modes
6. **resize_canvas**: Adjust dimensions
7. **capture_canvas**: Screenshot/export

### 3.2 Core Widget Tools
**Basic Widgets**:
- `add_button`, `add_text`, `add_input_text`, `add_checkbox`
- `add_radio_button`, `add_slider`, `add_combo`
- `add_list_box`, `add_color_picker`, `add_tree_node`
- `add_tab_bar`, `add_menu`, `add_tooltip`

**Container Widgets**:
- `add_window`, `add_child_window`, `add_group`
- `add_panel`, `add_collapsing_header`

**Advanced Widgets**:
- `add_table`, `add_plot`, `add_graph`
- `add_node_editor`, `add_sequencer`

### 3.3 Layout Tools
- `set_layout_horizontal`, `set_layout_vertical`
- `set_layout_grid`, `set_layout_stack`
- `add_separator`, `add_spacing`, `add_indent`
- `set_item_width`, `align_text`, `center_widget`

### 3.4 Styling & Theming Tools
- `set_color_scheme`: Apply theme presets
- `set_widget_style`: Individual styling
- `set_font`: Change fonts
- `set_spacing`: Adjust padding/margins
- `apply_rounded_corners`, `set_transparency`

### 3.5 Animation Tools (HImGuiAnimation integration)
- `create_animation`: Define keyframe animations
- `animate_value`: Interpolate values
- `play_animation`, `pause_animation`, `stop_animation`
- `set_easing_function`: Configure interpolation
- `create_transition`: State transitions

### 3.6 Extension Tools

#### imgui_club Integration:
- `add_memory_editor`: Hex editor widget
- `add_multi_context`: Context compositor
- `render_threaded`: Threaded rendering

#### File Dialog Tools (ImGuiFD/imfile):
- `open_file_dialog`: File selection
- `open_dir_dialog`: Directory selection
- `save_file_dialog`: Save file picker
- `set_file_filters`: Configure file types

#### Notification Tools (imgui-notify):
- `show_notification`: Toast notifications
- `show_success`, `show_warning`, `show_error`, `show_info`
- `clear_notifications`, `set_notification_position`

#### Plotting & Visualization:
- `add_line_plot`, `add_bar_chart`, `add_scatter_plot`
- `add_histogram`, `add_heatmap`, `add_pie_chart`

#### Node Editor:
- `create_node_graph`, `add_node`, `add_link`
- `get_node_connections`, `set_node_position`

#### Text Editor:
- `create_code_editor`: Syntax-highlighted editor
- `set_editor_language`, `get_editor_text`

#### Custom Widgets:
- `add_knob`: Rotary knobs
- `add_toggle`: Toggle switches
- `add_spinner`: Loading spinners
- `add_date_picker`: Date selection
- `add_color_gradient`: Gradient editors

### 3.7 Input Handling Tools
- `register_key_callback`: Keyboard events
- `register_mouse_callback`: Mouse events
- `set_drag_drop_source`, `set_drag_drop_target`
- `capture_input_state`: Input polling

### 3.8 Rendering & Graphics Tools
- `draw_line`, `draw_rect`, `draw_circle`, `draw_polygon`
- `draw_text`, `draw_image`, `add_texture`
- `set_clip_rect`, `push_draw_layer`

### 3.9 Data Binding Tools
- `bind_data_source`: Connect external data
- `create_live_chart`: Real-time data viz
- `update_widget_data`: Dynamic updates
- `watch_variable`: Reactive updates

### 3.10 Export/Import Tools
- `export_ui_json`: Save UI definition
- `import_ui_json`: Load UI definition
- `generate_code`: Export to Python code
- `create_template`: Save as reusable template

---

## 4. Documentation Files (MD)

### 4.1 Widget Reference Docs
1. **basic-widgets.md**: Buttons, text, inputs, checkboxes
2. **container-widgets.md**: Windows, panels, groups
3. **data-widgets.md**: Tables, lists, trees
4. **input-widgets.md**: Sliders, combos, pickers
5. **visualization-widgets.md**: Plots, graphs, charts
6. **custom-widgets.md**: Third-party extensions

### 4.2 Extension Reference Docs
1. **imgui-club-extensions.md**: Memory editor, multi-context
2. **animation-system.md**: HImGuiAnimation guide
3. **file-dialogs.md**: File picker implementations
4. **notifications.md**: Toast notification system
5. **node-editor.md**: Node graph editing
6. **text-editor.md**: Code/text editing
7. **plotting-extensions.md**: Data visualization

### 4.3 Feature Docs
1. **canvas-modes.md**: Canvas rendering modes
2. **layout-system.md**: Layout management
3. **theming-guide.md**: Styling & customization
4. **docking-viewports.md**: Advanced windowing
5. **input-handling.md**: Events & callbacks
6. **data-binding.md**: Reactive data connections
7. **serialization.md**: Save/load UI state

### 4.4 ImGui Core Docs (from wiki)
1. **imgui-basics.md**: Core concepts
2. **imgui-drawing.md**: Custom rendering
3. **imgui-fonts.md**: Font management
4. **imgui-tables.md**: Table system
5. **imgui-docking.md**: Docking system
6. **imgui-multiviewport.md**: Multi-viewport
7. **imgui-debugging.md**: Debug tools

### 4.5 Integration Docs
1. **mcp-integration.md**: FastMCP setup
2. **llm-usage-guide.md**: How LLMs use this
3. **code-generation.md**: Generated UI patterns
4. **best-practices.md**: UI design guidelines

---

## 5. Implementation Phases

### Phase 1: Foundation (Week 1-2)
- Project setup with UV
- FastMCP server skeleton
- Basic canvas system
- Core widget implementation (10-15 basic widgets)
- Simple rendering loop

### Phase 2: Widget Library (Week 3-4)
- Complete basic widgets (30+ widgets)
- Container widgets
- Layout system
- Styling/theming foundation

### Phase 3: Extensions (Week 5-6)
- imgui_club integration
- File dialog tools
- Notification system
- Animation framework (HImGuiAnimation)

### Phase 4: Advanced Features (Week 7-8)
- Node editor integration
- Plotting/visualization
- Text/code editor
- Data binding system

### Phase 5: Export/Templates (Week 9)
- JSON serialization
- Code generation
- Template system
- Documentation completion

### Phase 6: Testing & Polish (Week 10)
- Comprehensive test suite
- Example gallery
- Performance optimization
- Documentation review

---

## 6. Key Technical Decisions

### 6.1 State Management
- Use blinker for signal-based updates (like champi-signals)
- Canvas state stored in-memory with optional persistence
- Widget state tracked per-canvas

### 6.2 Threading Model
- Main thread: ImGui rendering
- Worker threads: MCP tool execution
- Thread-safe queues for commands

### 6.3 Serialization Format
```json
{
  "canvas": {
    "mode": "standard",
    "size": [1280, 720],
    "theme": "dark"
  },
  "widgets": [
    {
      "type": "button",
      "id": "btn1",
      "props": {"label": "Click", "pos": [10, 10]}
    }
  ]
}
```

### 6.4 Code Generation
Generate standalone Python scripts using imgui-bundle

---

## 7. Testing Strategy

### 7.1 Unit Tests
- Widget creation/manipulation
- Layout algorithms
- Serialization/deserialization
- Animation interpolation

### 7.2 Integration Tests
- MCP tool execution
- Canvas state management
- Multi-widget interactions
- Extension integrations

### 7.3 Visual Tests
- Screenshot comparisons
- Rendering verification
- Theme consistency

---

## 8. MCP Server Configuration

### 8.1 .mcp.json Entry
```json
{
  "champi-gen-ui": {
    "command": "uv",
    "args": ["run", "champi-gen-ui"],
    "cwd": "/path/to/champi-gen-ui"
  }
}
```

### 8.2 Server Entry Point
- CLI command: `champi-gen-ui serve`
- FastMCP server with all tools registered
- WebSocket/stdio transport support

---

## 9. Additional Features

### 9.1 Live Preview
- HTTP endpoint for canvas preview
- WebSocket updates for real-time sync
- Browser-based preview option

### 9.2 Preset Library
- Pre-built UI templates
- Common patterns (forms, dashboards, dialogs)
- One-command template insertion

### 9.3 AI-Specific Enhancements
- Natural language widget descriptions
- Smart layout suggestions
- Auto-responsive design
- Accessibility helpers

---

## 10. Documentation Deliverables

### MD Files to Create:
1. README.md - Project overview
2. ARCHITECTURE.md - System design
3. API_REFERENCE.md - All MCP tools
4. WIDGET_CATALOG.md - Complete widget list
5. EXTENSIONS_GUIDE.md - Third-party integrations
6. QUICK_START.md - Getting started
7. EXAMPLES.md - Code examples
8. ROADMAP.md - Future plans
9. CONTRIBUTING.md - Development guide
10. All widget/extension reference docs listed in section 4

---

## Success Criteria

✅ 100+ MCP tools for UI generation
✅ Support for all imgui-bundle widgets
✅ Integration with all listed extensions
✅ Complete documentation
✅ Working examples
✅ Test coverage >80%
✅ Successful LLM-driven UI generation

---

This plan provides a comprehensive foundation for building a powerful generative UI MCP server that LLMs can use to create sophisticated interfaces through natural language.
