import pandas as pd
import logging
import sys


class TTestModel:
    def __init__(self, data_validator, app_config, user_input_model):
        self.data_validator = data_validator
        self.logger = logging.getLogger(__name__)
        self.app_config = app_config
        self.user_input_model = user_input_model
        self.df = self.control_set_df = self.change_set_df = self.results_df = self.solutions_df = None

    def load_from_excel(self, file_path):
        try:
            df = pd.read_excel(file_path, sheet_name='data')
            if not self.data_validator.validate_data(df):
                self.logger.error('Data validation failed.')
                sys.exit(1)

            self.df = df
            self._split_data()

        except Exception as e:
            self.logger.error(f'Error loading Excel file: {e}')
            sys.exit(1)

    def _split_data(self):
        self.control_set_df, self.change_set_df = (
            self.df.filter(like='controlSet'),
            self.df.filter(like='changeSet')
        )

    def create_solutions_df(self):
        # Concatenate the original DataFrame and the results DataFrame
        self.solutions_df = pd.concat([self.df, self.results_df], axis=1)

        # Get the ttest_options from the user input model
        ttest_options = self.user_input_model.ttest_options

        # If 'sort_by' exists in DataFrame columns, sort the DataFrame
        if ttest_options.sort_by in self.solutions_df.columns:
            print(f'Sorting by {ttest_options.sort_by} and {ttest_options.ascending} and type(ttest_options.ascending) is {type(ttest_options.ascending)})')
            self.solutions_df.sort_values(by=ttest_options.sort_by, ascending=ttest_options.ascending, inplace=True)

