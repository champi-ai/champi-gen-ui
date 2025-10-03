"""Widget implementations."""

# Basic widgets
from champi_gen_ui.widgets.basic import (
    ButtonWidget,
    CheckboxWidget,
    ColorPickerWidget,
    ComboWidget,
    InputTextWidget,
    ListBoxWidget,
    RadioButtonWidget,
    TextWidget,
)

# Container widgets
from champi_gen_ui.widgets.container import (
    ChildWindowWidget,
    CollapsingHeaderWidget,
    DummyWidget,
    GroupWidget,
    SeparatorWidget,
    SpacingWidget,
    TabBarWidget,
    TabItemWidget,
    WindowWidget,
)

# Display widgets
from champi_gen_ui.widgets.display import (
    BulletTextWidget,
    BulletWidget,
    HelpMarkerWidget,
    ImageButtonWidget,
    ImageWidget,
    LabelTextWidget,
    LoadingIndicatorWidget,
    PlotHistogramWidget,
    PlotLinesWidget,
    ProgressBarWidget,
    TextColoredWidget,
    TextDisabledWidget,
    TextWrappedWidget,
)

# Menu widgets
from champi_gen_ui.widgets.menu import (
    ContextMenuWidget,
    MenuBarWidget,
    MenuItemWidget,
    MenuWidget,
    PopupWidget,
    SelectableWidget,
    TooltipWidget,
    TreeNodeWidget,
)

# Plotting widgets
from champi_gen_ui.widgets.plotting import (
    BarChartWidget,
    CandlestickChartWidget,
    ErrorBarsWidget,
    HeatmapWidget,
    HistogramWidget,
    LineChartWidget,
    PieChartWidget,
    RealtimePlotWidget,
    ScatterPlotWidget,
)

# Slider widgets
from champi_gen_ui.widgets.slider import (
    DragFloatWidget,
    DragIntWidget,
    SliderFloatWidget,
    SliderIntWidget,
)
from champi_gen_ui.widgets.slider import (
    ProgressBarWidget as SliderProgressBarWidget,
)

__all__ = [
    # Plotting
    "BarChartWidget",
    # Display
    "BulletTextWidget",
    "BulletWidget",
    # Basic
    "ButtonWidget",
    "CandlestickChartWidget",
    "CheckboxWidget",
    # Container
    "ChildWindowWidget",
    "CollapsingHeaderWidget",
    "ColorPickerWidget",
    "ComboWidget",
    # Menu
    "ContextMenuWidget",
    # Slider
    "DragFloatWidget",
    "DragIntWidget",
    "DummyWidget",
    "ErrorBarsWidget",
    "GroupWidget",
    "HeatmapWidget",
    "HelpMarkerWidget",
    "HistogramWidget",
    "ImageButtonWidget",
    "ImageWidget",
    "InputTextWidget",
    "LabelTextWidget",
    "LineChartWidget",
    "ListBoxWidget",
    "LoadingIndicatorWidget",
    "MenuBarWidget",
    "MenuItemWidget",
    "MenuWidget",
    "PieChartWidget",
    "PlotHistogramWidget",
    "PlotLinesWidget",
    "PopupWidget",
    "ProgressBarWidget",
    "RadioButtonWidget",
    "RealtimePlotWidget",
    "ScatterPlotWidget",
    "SelectableWidget",
    "SeparatorWidget",
    "SliderFloatWidget",
    "SliderIntWidget",
    "SliderProgressBarWidget",
    "SpacingWidget",
    "TabBarWidget",
    "TabItemWidget",
    "TextColoredWidget",
    "TextDisabledWidget",
    "TextWidget",
    "TextWrappedWidget",
    "TooltipWidget",
    "TreeNodeWidget",
    "WindowWidget",
]
