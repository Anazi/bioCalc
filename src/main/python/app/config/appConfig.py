import logging
from src.main.python.app.utils.generalUtils import GeneralUtils


class AppConfig:
    class LoggingConfig:
        def __init__(self):
            self.level = logging.INFO

        def populate_from_dict(self, config_dict):
            self.level = config_dict.get('loggingLevel', logging.INFO)

    class DataConfig:
        def __init__(self):
            self.fixed_columns = ['lipidSpecies']
            self.excel_file_path = ""

        def populate_from_dict(self, config_dict):
            self.fixed_columns = config_dict.get('fixedColumns', ['lipidSpecies'])
            excel_file_name = config_dict.get('excelFilePath', "")
            self.excel_file_path = GeneralUtils.resolve_full_path(excel_file_name, 'input')

    class GraphConfig:
        def __init__(self):
            self.supported_graph_types = ['Bar', 'Volcano', 'HeatMap', 'Dot', 'Pie']

        def populate_from_dict(self, config_dict):
            self.supported_graph_types = config_dict.get('supportedGraphTypes',
                                                         ['Bar', 'Volcano', 'HeatMap', 'Dot', 'Pie'])

    def __init__(self, yaml_path):
        self.logging_config = self.LoggingConfig()
        self.data_config = self.DataConfig()
        self.graph_config = self.GraphConfig()
        self.initialize(yaml_path)

    def initialize(self, yaml_path):
        config = GeneralUtils.read_yaml(yaml_path)
        app_config = config.get('app', {})

        self.logging_config.populate_from_dict(app_config)
        self.data_config.populate_from_dict(app_config)
        self.graph_config.populate_from_dict(app_config)

    def set_logging_level(self, level):
        self.logging_config.level = level
