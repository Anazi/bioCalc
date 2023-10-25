import logging
import sys
from src.main.python.app.model.userInputModel import UserInputModel
from src.main.python.app.utils.generalUtils import GeneralUtils


class UserInputService:
    def __init__(self, yaml_path):
        self.yaml_path = yaml_path
        self.user_input_model: UserInputModel = UserInputModel()
        self.logger = logging.getLogger(__name__)

    def initialize(self):
        try:
            config = GeneralUtils.read_yaml(self.yaml_path)
            user_config = config.get('user', {})
            self.user_input_model.calculation_option = user_config.get('calculation_option', '')

            # Validate mandatory fields
            if not self.user_input_model.calculation_option:
                self.logger.error("Field 'calculation_option' is mandatory.")
                sys.exit(1)

            reporting_config = user_config.get('reporting', {})
            self.user_input_model.reporting_options.populate_from_dict(reporting_config)

            if self.user_input_model.reporting_options.generate_report is None:
                self.logger.error("Field 'generateReport' is mandatory and must be set to true or false.")
                sys.exit(1)

            if self.user_input_model.reporting_options.generate_report and not self.user_input_model.reporting_options.file_path:
                self.logger.error("Field 'filePath' is mandatory when 'generateReport' is set to true.")
                sys.exit(1)

            for option in user_config.get('options', []):
                if 'ttestOptions' in option:
                    self.user_input_model.ttest_options.populate_from_dict(option.get('ttestOptions', {}))
                if 'graphOptions' in option:
                    self.user_input_model.graph_options.populate_from_dict(option.get('graphOptions', {}))

            self._validate_inputs()

        except Exception as e:
            self.logger.error(f"Failed to initialize UserInputModel: {e}")
            raise

    def _validate_inputs(self):
        # Validate mandatory fields for ttestOptions
        if not self.user_input_model.ttest_options.calculations:
            self.logger.error("No calculation selected. At least one calculation type must be selected.")
            sys.exit(1)

        # Validate conditional mandatory fields for graphs
        report_graph_options = self.user_input_model.reporting_options.report_graph_options
        include_in_excel = report_graph_options.include_in_excel
        separate_image = report_graph_options.separate_image

        graph_options: UserInputModel.GraphOptions = self.user_input_model.graph_options

        if include_in_excel or separate_image:
            mandatory_graph_fields = ['graph_type', 'x_axis', 'y_axis', 'style', 'title']
            for field in mandatory_graph_fields:
                if not hasattr(graph_options, field) or getattr(graph_options, field) is None:
                    self.logger.error(
                        f"Field '{field}' is mandatory when either 'includeInExcel' or 'separateImage' is set to true.")
                    sys.exit(1)

    def get_user_input_model(self):
        return self.user_input_model
