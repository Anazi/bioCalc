import logging
import sys

from src.main.python.app.calculation.tTestCalculation import TTestCalculation
from src.main.python.app.config.appConfig import AppConfig
from src.main.python.app.model.tTestModel import TTestModel
from src.main.python.app.model.userInputModel import UserInputModel
from src.main.python.app.service.reportingService import ReportingService
from src.main.python.app.service.userInputService import UserInputService

from src.main.python.app.validation.tTestDataValidator import TTestDataValidator
from src.main.python.app.visualization.graphModule import GraphModule


class CalculationService:
    def __init__(self, yaml_path):
        self.logger = logging.getLogger(__name__)

        # Step 1: Initialize AppConfig
        self.app_config = AppConfig(yaml_path=yaml_path)

        # Step 2: Initialize UserInput using UserInputService
        self.user_input_service = UserInputService(yaml_path)
        self.user_input_service.initialize()
        self.user_input_model: UserInputModel = self.user_input_service.get_user_input_model()

        # Step 3, 4: Load and Validate Data
        self.data_validator = TTestDataValidator(self.app_config)
        self.ttest_model = TTestModel(
            app_config=self.app_config,
            data_validator=self.data_validator,
            user_input_model=self.user_input_model
        )

        # Step 5: Initialize Calculator
        self.ttest_calculator = TTestCalculation(self.ttest_model)

        # Step 6: Initialize GraphModule
        self.graph_module = GraphModule(self.ttest_model, self.user_input_model)

        # Step 7, 8: Initialize ReportingService
        self.reporting_service = ReportingService(self.ttest_model, self.user_input_model)

    def perform_operations(self):
        try:
            # Step 3, 4: Load and Validate Data
            self._load_and_validate_data()

            # Step 5: Perform Calculations
            self._perform_calculations()

            # Step 6: Generate Graphs
            fig = self.graph_module.generate_graph()

            # Step 7, 8: Reporting
            self.reporting_service.generate_reports(fig)

        except Exception as e:
            self.logger.error(f"Error in perform_operations: {e}")
            sys.exit(1)

    def _load_and_validate_data(self):
        self.ttest_model.load_from_excel(self.app_config.data_config.excel_file_path)
        if not self.data_validator.validate_data(self.ttest_model.df):
            self.logger.error("Data validation failed.")
            sys.exit(1)

    def _perform_calculations(self):
        if not self.ttest_calculator.calculate(self.user_input_model.ttest_options.calculations):
            self.logger.error("Failed to perform calculations.")
            sys.exit(1)
        self.ttest_model.create_solutions_df()
