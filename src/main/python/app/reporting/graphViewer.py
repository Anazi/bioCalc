import numpy as np
import pandas as pd
from plotly import graph_objects as go
from bokeh.layouts import column
from bokeh.models import Slider, CustomJS
from bokeh.plotting import figure, show, ColumnDataSource

from src.main.python.app.model.tTestModel import TTestModel
from src.main.python.app.model.userInputModel import UserInputModel


class GraphViewer:

    def __init__(self, user_input_model: UserInputModel):
        self.user_input_model = user_input_model
        self.graph_options: UserInputModel.GraphOptions = self.user_input_model.graph_options

    def display_graph(self, ttest_model: TTestModel):
        graph_type = self.graph_options.graph_type
        if graph_type == 'HeatMap':
            self._display_interactive_heatmap(ttest_model.solutions_df)
        elif graph_type == 'Volcano':
            self._display_interactive_volcano(ttest_model.solutions_df)
        elif graph_type == 'Bar':
            self._display_interactive_bar(ttest_model.solutions_df)

    def _display_interactive_heatmap(self, ttest_model):
        # Create example data
        df = ttest_model.solution_df

        # Create correlation and covariance matrices
        corr_matrix = df.corr()
        cov_matrix = df.cov()

        # Create the heatmap
        heatmap = go.FigureWidget(
            data=[go.Heatmap(z=corr_matrix,
                             x=corr_matrix.columns,
                             y=corr_matrix.columns,
                             colorscale='Viridis')],
            layout=go.Layout(
                title=self.graph_options.title,
                xaxis=dict(title=self.graph_options.x_axis),
                yaxis=dict(title=self.graph_options.y_axis),
            )
        )

        # Add dropdown menu
        heatmap.update_layout(
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=['z', [corr_matrix]],
                            label="Correlation",
                            method="restyle"
                        ),
                        dict(
                            args=['z', [cov_matrix]],
                            label="Covariance",
                            method="restyle"
                        )
                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.11,
                    xanchor="left",
                    y=1.15,
                    yanchor="top"
                ),
            ]
        )

        # Show the heatmap
        heatmap.show()

    def _display_interactive_volcano(self, df):
        x_axis_name = self.graph_options.x_axis
        y_axis_name = self.graph_options.y_axis
        # Assuming df is the DataFrame from TTestModel
        source = ColumnDataSource(data=dict(x=df[x_axis_name], y=df[y_axis_name]))

        # Create a new Bokeh figure for the Volcano plot
        fig = figure(title=self.graph_options.title, x_axis_label=x_axis_name, y_axis_label=y_axis_name)

        # Add scatter points to the figure
        fig.scatter('x', 'y', source=source)

        # Initialize a list for threshold values
        threshold_values = [50] * len(df[y_axis_name])

        # Add a line glyph for threshold
        threshold_line = fig.line(df[x_axis_name], threshold_values, line_width=2, line_dash="dashed", line_color="red")

        # Create slider
        slider = Slider(start=0, end=100, value=50, step=1, title="Threshold")

        # JavaScript code to update the plot based on the slider
        callback = CustomJS(args=dict(line=threshold_line, threshold_values=threshold_values), code="""
            var threshold = cb_obj.value;
            for (var i = 0; i < threshold_values.length; i++) {
                threshold_values[i] = threshold;
            }
            line.data_source.data['y'] = threshold_values;
            line.data_source.change.emit();
        """)

        slider.js_on_change('value', callback)

        # Show plot and slider
        layout = column(slider, fig)
        show(layout)

    def _display_interactive_bar(self, df):
        # Assuming df is the DataFrame from TTestModel
        x_data = df[self.graph_options.x_axis].tolist()
        y_data = df[self.graph_options.y_axis].tolist()

        # Create the bar chart
        bar_chart = go.FigureWidget(
            data=[go.Bar(x=x_data, y=y_data)],
            layout=go.Layout(
                title=self.graph_options.title,
                xaxis=dict(title=self.graph_options.x_axis),
                yaxis=dict(title=self.graph_options.y_axis),
            )
        )

        # Show the bar chart
        bar_chart.show()
