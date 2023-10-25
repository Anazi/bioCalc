import pandas as pd
import logging

from .dataValidatorStrategy import DataValidatorStrategy
from ..config.appConfig import AppConfig


class TTestDataValidator(DataValidatorStrategy):
    def __init__(self, app_config: AppConfig):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=app_config.logging_config.level)
        self.app_config = app_config

    def validate_columns(self, df):
        """Validate column names."""
        expected_fixed_columns = self.app_config.data_config.fixed_columns

        # Extracting dynamic columns
        control_columns = sorted([col for col in df.columns if 'controlSet' in col])
        change_columns = sorted([col for col in df.columns if 'changeSet' in col])

        # Validate that there are pairs of control and change sets
        control_nums = [int(col.split('controlSet')[1]) for col in control_columns]
        change_nums = [int(col.split('changeSet')[1]) for col in change_columns]

        if control_nums != change_nums:
            self.logger.error(f'Control sets {control_nums} and change sets {change_nums} do not form valid pairs.')
            return False

        # Check for fixed columns
        missing_columns = [col for col in expected_fixed_columns if col not in df.columns]
        if missing_columns:
            self.logger.error(f'Missing expected fixed columns: {missing_columns}')
            return False

        return True

    def validate_data(self, df):
        """Validate the data in a single DataFrame."""
        if not self.validate_columns(df):
            return False

        if not self.validate_no_nulls(df):
            return False

        return True

    def validate_no_nulls(self, df):
        """Validate for null or NaN values."""
        if df.isnull().values.any():
            self.logger.error('Null values found in the data.')
            return False
        return True
