import logging
import sys

from src.main.python.app.constants import constants as const
from src.main.python.app.service.calculationService import CalculationService


class BioCalcApp:
    def __init__(self, yaml_path):
        # Initialize logger
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

        # Initialize CalculationService
        self.calculation_service = CalculationService(yaml_path)

    def run(self):
        try:
            # Perform all the operations: Load Data, Validate, Calculate, Generate Graphs, and Reporting
            self.calculation_service.perform_operations()
        except Exception as e:
            self.logger.error(f"An error occurred while running the application: {e}")
            sys.exit(1)


if __name__ == "__main__":
    # Set the path to the YAML configuration file
    app_yaml_path = const.APP_YAML_PATH

    # Initialize and run the application
    app = BioCalcApp(yaml_path=app_yaml_path)
    app.run()
