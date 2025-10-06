"""Advanced plotting widgets using ImPlot."""

from imgui_bundle import imgui, implot

from champi_gen_ui.core.widget import Widget


class PlotWidget(Widget):
    """Base plot widget using ImPlot."""

    def __init__(
        self,
        widget_id: str,
        title: str = "Plot",
        size: tuple[float, float] = (-1, -1),
        **props,
    ):
        """Initialize plot widget."""
        props["title"] = title
        props["size"] = size
        props["x_label"] = props.get("x_label", "X")
        props["y_label"] = props.get("y_label", "Y")
        props["legend"] = props.get("legend", True)
        super().__init__(widget_id, **props)

    def begin_plot(self) -> bool:
        """Begin plot rendering."""
        title = self.state.properties.get("title", "Plot")
        size = self.state.properties.get("size", (-1, -1))
        flags = self.state.properties.get("flags", 0)

        return implot.begin_plot(title, imgui.ImVec2(*size), flags)

    def end_plot(self) -> None:
        """End plot rendering."""
        implot.end_plot()

    def setup_axes(self) -> None:
        """Setup plot axes."""
        x_label = self.state.properties.get("x_label", "X")
        y_label = self.state.properties.get("y_label", "Y")
        x_flags = self.state.properties.get("x_flags", 0)
        y_flags = self.state.properties.get("y_flags", 0)

        implot.setup_axes(x_label, y_label, x_flags, y_flags)


class LineChartWidget(PlotWidget):
    """Line chart widget."""

    def __init__(
        self,
        widget_id: str,
        title: str = "Line Chart",
        x_data: list[float] | None = None,
        y_data: list[float] | None = None,
        **props,
    ):
        """Initialize line chart."""
        props["x_data"] = x_data or []
        props["y_data"] = y_data or []
        props["line_label"] = props.get("line_label", "Line")
        super().__init__(widget_id, title, **props)

    def render(self) -> None:
        """Render line chart."""
        if self.begin_plot():
            self.setup_axes()

            x_data = self.state.properties.get("x_data", [])
            y_data = self.state.properties.get("y_data", [])
            line_label = self.state.properties.get("line_label", "Line")

            if x_data and y_data and len(x_data) == len(y_data):
                implot.plot_line(line_label, x_data, y_data)

            self.end_plot()


class BarChartWidget(PlotWidget):
    """Bar chart widget."""

    def __init__(
        self,
        widget_id: str,
        title: str = "Bar Chart",
        values: list[float] | None = None,
        labels: list[str] | None = None,
        **props,
    ):
        """Initialize bar chart."""
        props["values"] = values or []
        props["labels"] = labels or []
        props["bar_label"] = props.get("bar_label", "Bars")
        props["bar_width"] = props.get("bar_width", 0.67)
        super().__init__(widget_id, title, **props)

    def render(self) -> None:
        """Render bar chart."""
        if self.begin_plot():
            self.setup_axes()

            values = self.state.properties.get("values", [])
            bar_label = self.state.properties.get("bar_label", "Bars")
            bar_width = self.state.properties.get("bar_width", 0.67)

            if values:
                implot.plot_bars(bar_label, values, bar_width)

            self.end_plot()


class ScatterPlotWidget(PlotWidget):
    """Scatter plot widget."""

    def __init__(
        self,
        widget_id: str,
        title: str = "Scatter Plot",
        x_data: list[float] | None = None,
        y_data: list[float] | None = None,
        **props,
    ):
        """Initialize scatter plot."""
        props["x_data"] = x_data or []
        props["y_data"] = y_data or []
        props["scatter_label"] = props.get("scatter_label", "Points")
        super().__init__(widget_id, title, **props)

    def render(self) -> None:
        """Render scatter plot."""
        if self.begin_plot():
            self.setup_axes()

            x_data = self.state.properties.get("x_data", [])
            y_data = self.state.properties.get("y_data", [])
            scatter_label = self.state.properties.get("scatter_label", "Points")

            if x_data and y_data and len(x_data) == len(y_data):
                implot.plot_scatter(scatter_label, x_data, y_data)

            self.end_plot()


class HistogramWidget(PlotWidget):
    """Histogram widget."""

    def __init__(
        self,
        widget_id: str,
        title: str = "Histogram",
        values: list[float] | None = None,
        bins: int = 10,
        **props,
    ):
        """Initialize histogram."""
        props["values"] = values or []
        props["bins"] = bins
        props["histogram_label"] = props.get("histogram_label", "Distribution")
        super().__init__(widget_id, title, **props)

    def render(self) -> None:
        """Render histogram."""
        if self.begin_plot():
            self.setup_axes()

            values = self.state.properties.get("values", [])
            bins = self.state.properties.get("bins", 10)
            histogram_label = self.state.properties.get(
                "histogram_label", "Distribution"
            )

            if values:
                implot.plot_histogram(histogram_label, values, bins)

            self.end_plot()


class HeatmapWidget(PlotWidget):
    """Heatmap widget."""

    def __init__(
        self,
        widget_id: str,
        title: str = "Heatmap",
        values: list[list[float]] | None = None,
        **props,
    ):
        """Initialize heatmap."""
        props["values"] = values or []
        props["heatmap_label"] = props.get("heatmap_label", "Heatmap")
        props["scale_min"] = props.get("scale_min", 0.0)
        props["scale_max"] = props.get("scale_max", 1.0)
        super().__init__(widget_id, title, **props)

    def render(self) -> None:
        """Render heatmap."""
        if self.begin_plot():
            self.setup_axes()

            values = self.state.properties.get("values", [])
            heatmap_label = self.state.properties.get("heatmap_label", "Heatmap")
            scale_min = self.state.properties.get("scale_min", 0.0)
            scale_max = self.state.properties.get("scale_max", 1.0)

            if values and len(values) > 0:
                rows = len(values)
                cols = len(values[0]) if values else 0

                if rows > 0 and cols > 0:
                    # Flatten 2D array for ImPlot
                    flat_values = [val for row in values for val in row]
                    implot.plot_heatmap(
                        heatmap_label,
                        flat_values,
                        rows,
                        cols,
                        scale_min,
                        scale_max,
                    )

            self.end_plot()


class PieChartWidget(Widget):
    """Pie chart widget."""

    def __init__(
        self,
        widget_id: str,
        values: list[float] | None = None,
        labels: list[str] | None = None,
        center: tuple[float, float] = (0.5, 0.5),
        radius: float = 0.4,
        **props,
    ):
        """Initialize pie chart."""
        props["values"] = values or []
        props["labels"] = labels or []
        props["center"] = center
        props["radius"] = radius
        super().__init__(widget_id, **props)

    def render(self) -> None:
        """Render pie chart."""
        values = self.state.properties.get("values", [])
        labels = self.state.properties.get("labels", [])
        center = self.state.properties.get("center", (0.5, 0.5))
        radius = self.state.properties.get("radius", 0.4)

        if (
            values
            and labels
            and len(values) == len(labels)
            and implot.begin_plot("##pie", imgui.ImVec2(-1, -1))
        ):
            implot.setup_axes("", "", implot.AxisFlags_.no_decorations)
            implot.plot_pie_chart(labels, values, *center, radius)
            implot.end_plot()


class RealtimePlotWidget(PlotWidget):
    """Realtime scrolling plot widget."""

    def __init__(
        self,
        widget_id: str,
        title: str = "Realtime Plot",
        max_points: int = 1000,
        **props,
    ):
        """Initialize realtime plot."""
        props["data"] = []
        props["max_points"] = max_points
        props["line_label"] = props.get("line_label", "Signal")
        super().__init__(widget_id, title, **props)

    def add_point(self, value: float) -> None:
        """Add a data point."""
        data = self.state.properties.get("data", [])
        max_points = self.state.properties.get("max_points", 1000)

        data.append(value)

        # Keep only recent points
        if len(data) > max_points:
            data.pop(0)

        self.state.properties["data"] = data

    def render(self) -> None:
        """Render realtime plot."""
        if self.begin_plot():
            # Setup auto-scrolling axes
            implot.setup_axes_limits(
                0, self.state.properties.get("max_points", 1000), -1, 1
            )

            data = self.state.properties.get("data", [])
            line_label = self.state.properties.get("line_label", "Signal")

            if data:
                x_data = list(range(len(data)))
                implot.plot_line(line_label, x_data, data)

            self.end_plot()


class CandlestickChartWidget(PlotWidget):
    """Candlestick chart widget for financial data."""

    def __init__(
        self,
        widget_id: str,
        title: str = "Candlestick Chart",
        dates: list[float] | None = None,
        opens: list[float] | None = None,
        highs: list[float] | None = None,
        lows: list[float] | None = None,
        closes: list[float] | None = None,
        **props,
    ):
        """Initialize candlestick chart."""
        props["dates"] = dates or []
        props["opens"] = opens or []
        props["highs"] = highs or []
        props["lows"] = lows or []
        props["closes"] = closes or []
        super().__init__(widget_id, title, **props)

    def render(self) -> None:
        """Render candlestick chart."""
        if self.begin_plot():
            self.setup_axes()

            dates = self.state.properties.get("dates", [])
            opens = self.state.properties.get("opens", [])
            highs = self.state.properties.get("highs", [])
            lows = self.state.properties.get("lows", [])
            closes = self.state.properties.get("closes", [])

            if (
                dates
                and opens
                and highs
                and lows
                and closes
                and len(dates) == len(opens) == len(highs) == len(lows) == len(closes)
            ):
                implot.plot_candlestick(
                    "OHLC",
                    dates,
                    opens,
                    closes,
                    lows,
                    highs,
                    bull_col=None,
                    bear_col=None,
                )

            self.end_plot()


class ErrorBarsWidget(PlotWidget):
    """Plot with error bars."""

    def __init__(
        self,
        widget_id: str,
        title: str = "Error Bars",
        x_data: list[float] | None = None,
        y_data: list[float] | None = None,
        y_errors: list[float] | None = None,
        **props,
    ):
        """Initialize error bars plot."""
        props["x_data"] = x_data or []
        props["y_data"] = y_data or []
        props["y_errors"] = y_errors or []
        props["error_label"] = props.get("error_label", "Data")
        super().__init__(widget_id, title, **props)

    def render(self) -> None:
        """Render error bars."""
        if self.begin_plot():
            self.setup_axes()

            x_data = self.state.properties.get("x_data", [])
            y_data = self.state.properties.get("y_data", [])
            y_errors = self.state.properties.get("y_errors", [])
            error_label = self.state.properties.get("error_label", "Data")

            if (
                x_data
                and y_data
                and y_errors
                and len(x_data) == len(y_data) == len(y_errors)
            ):
                implot.plot_error_bars(error_label, x_data, y_data, y_errors)
                implot.plot_line(error_label, x_data, y_data)

            self.end_plot()
