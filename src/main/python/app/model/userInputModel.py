from src.main.python.app.utils.generalUtils import GeneralUtils


class UserInputModel:
    class TTestOptions:
        def __init__(self):
            self.sort_by = None
            self.ascending = None
            self.calculations = None
            self.file_path = None

        def populate_from_dict(self, config_dict):
            self.sort_by = config_dict.get('sortBy')
            self.ascending = config_dict.get('ascending')
            self.calculations = config_dict.get('calculations')

    class ReportingOptions:
        def __init__(self):
            self.generate_report = None
            self.file_path = None
            self.output_file_name = None
            self.sheet_names = self.SheetNames()
            self.report_graph_options = self.ReportGraphOptions()

        def populate_from_dict(self, config_dict):
            self.generate_report = config_dict.get('generateReport')

            self.output_file_name = config_dict.get('outputFileName')
            # Resolve the full path for the output file
            self.file_path = GeneralUtils.resolve_full_path(self.output_file_name, 'output')

            sheet_names_config = config_dict.get('sheetNames', {})
            self.sheet_names.populate_from_dict(sheet_names_config)

            report_graph_options_config = config_dict.get('reportGraphOptions', {})
            self.report_graph_options.populate_from_dict(report_graph_options_config)

        class SheetNames:
            def __init__(self):
                self.data_sheet = None
                self.result_sheet = None

            def populate_from_dict(self, config_dict):
                self.data_sheet = config_dict.get('data_sheet')
                self.result_sheet = config_dict.get('result_sheet')

        class ReportGraphOptions:
            def __init__(self):
                self.include_in_excel = None
                self.separate_image = None
                self.image_format = None

            def populate_from_dict(self, config_dict):
                self.include_in_excel = config_dict.get('includeInExcel')
                self.separate_image = config_dict.get('separateImage')
                self.image_format = config_dict.get('imageFormat')

    class GraphOptions:
        def __init__(self):
            self.graph_type = None
            self.x_axis = None
            self.y_axis = None
            self.color = None
            self.hue = None
            self.style = None
            self.palette = None
            self.title = None
            self.xLabel = None
            self.yLabel = None
            self.dpi = None
            self.format = None

        def populate_from_dict(self, config_dict):
            self.graph_type = config_dict.get('graphType')
            self.x_axis = config_dict.get('xAxis')
            self.y_axis = config_dict.get('yAxis')
            self.color = config_dict.get('color')
            self.hue = config_dict.get('hue')
            self.style = config_dict.get('style')
            self.palette = config_dict.get('palette')
            self.title = config_dict.get('title')
            self.xLabel = config_dict.get('xLabel')
            self.yLabel = config_dict.get('yLabel')
            self.dpi = config_dict.get('dpi')

    def __init__(self):
        self.calculation_option = None
        self.reporting_options = self.ReportingOptions()
        self.ttest_options = self.TTestOptions()
        self.graph_options: UserInputModel.GraphOptions = self.GraphOptions()
