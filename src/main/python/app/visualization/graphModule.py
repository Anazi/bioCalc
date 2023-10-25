import matplotlib.pyplot as plt
import seaborn as sns
import logging

from ..model.tTestModel import TTestModel
from ..model.userInputModel import UserInputModel


class GraphModule:
    def __init__(self, ttest_model: TTestModel, user_input_model: UserInputModel):
        """
            For example, if you want to generate a heatmap using specific columns other than what's set in
            graph_options.x_axis and graph_options.y_axis, you can do:

            `graph_module = GraphModule(ttest_model, user_input_model)
            fig = graph_module.generate_graph(columns=['col1', 'col2', 'col3'])`

            Here, columns=['col1', 'col2', 'col3'] is an optional keyword argument that will be passed to generate_heat_map,
            and it will use these columns to generate the heatmap.

            Similarly, for generating a pie chart where you want to use a specific set of values to aggregate, you can do:

            `graph_module = GraphModule(ttest_model, user_input_model)
            fig = graph_module.generate_graph(values='some_value_field')`

            Here, values='some_value_field' is an optional keyword argument that will be passed to generate_pie_chart, and
            it will use this field for aggregation.
        """
        self.ttest_model = ttest_model
        self.user_input_model = user_input_model
        self.logger = logging.getLogger(__name__)

    def generate_graph(self, **kwargs):
        graph_options = self.user_input_model.graph_options
        graph_type = graph_options.graph_type

        graph_methods = {
            'HeatMap': self.generate_heat_map,
            'Volcano': self.generate_volcano_plot,
            'Bar': self.generate_bar_chart,
            'Dot': self.generate_dot_chart,
            'Pie': self.generate_pie_chart,
        }

        try:
            fig = graph_methods[graph_type](graph_options, **kwargs)
            return fig
        except KeyError:
            self.logger.error(f'Unsupported graph type: {graph_type}')
            return None
        except Exception as e:
            self.logger.error(f'Error generating graph: {e}')
            return None

    @staticmethod
    def _add_graph_customization(graph_options):
        plt.title(graph_options.title)
        plt.style.use(graph_options.style)
        if graph_options.xLabel:
            plt.xlabel(graph_options.xLabel)
        if graph_options.yLabel:
            plt.ylabel(graph_options.yLabel)

    def _add_optional_params(self, kwargs, graph_options: UserInputModel.GraphOptions):
        if graph_options.color:
            kwargs['color'] = graph_options.color
        # if graph_options.hue:
        #     kwargs['hue'] = graph_options.hue
        if graph_options.palette:
            kwargs['palette'] = graph_options.palette

    def generate_heat_map(self, graph_options, columns=None):
        # columns could be a list of column names that you want to include in the heatmap.
        try:
            fig, ax = plt.subplots()
            if columns:
                sns.heatmap(self.ttest_model.solutions_df[columns].corr(), annot=True)
            else:
                sns.heatmap(self.ttest_model.solutions_df[[graph_options.x_axis, graph_options.y_axis]].corr(), annot=True)
            self._add_graph_customization(graph_options)
            return fig
        except Exception as e:
            self.logger.error(f'Error generating heat map: {e}')
            return None

    def generate_pie_chart(self, graph_options, values=None):
        # values could be used to group y_axis values for each unique x_axis value.
        try:
            fig, ax = plt.subplots()
            if values:
                df = self.ttest_model.solutions_df.groupby(graph_options.x_axis)[values].sum()
            else:
                df = self.ttest_model.solutions_df.groupby(graph_options.x_axis)[graph_options.y_axis].sum()
            plt.pie(df, labels=df.index, autopct='%1.1f%%')
            self._add_graph_customization(graph_options)
            return fig
        except Exception as e:
            self.logger.error(f'Error generating pie chart: {e}')
            return None

    def generate_volcano_plot(self, graph_options: UserInputModel.GraphOptions):
        try:
            fig, ax = plt.subplots()

            kwargs = {}
            self._add_optional_params(kwargs, graph_options)

            sns.scatterplot(data=self.ttest_model.solutions_df, x=graph_options.x_axis, y=graph_options.y_axis,
                            **kwargs)
            self._add_graph_customization(graph_options)
            return fig
        except Exception as e:
            self.logger.error(f'Error generating volcano plot: {e}')
            return None

    def generate_bar_chart(self, graph_options):
        try:
            fig, ax = plt.subplots()
            kwargs = {}
            self._add_optional_params(kwargs, graph_options)
            sns.barplot(data=self.ttest_model.solutions_df, x=graph_options.x_axis, y=graph_options.y_axis, **kwargs)
            self._add_graph_customization(graph_options)
            return fig
        except Exception as e:
            self.logger.error(f'Error generating bar chart: {e}')
            return None

    def generate_dot_chart(self, graph_options):
        try:
            fig, ax = plt.subplots()
            kwargs = {}
            self._add_optional_params(kwargs, graph_options)
            sns.stripplot(data=self.ttest_model.solutions_df, x=graph_options.x_axis, y=graph_options.y_axis, **kwargs)
            self._add_graph_customization(graph_options)
            return fig
        except Exception as e:
            self.logger.error(f'Error generating dot chart: {e}')
            return None
