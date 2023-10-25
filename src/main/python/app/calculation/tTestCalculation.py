import logging

import numpy as np
import pandas as pd

from src.main.python.app.model.tTestModel import TTestModel
from .calculationStrategy import CalculationStrategy


class TTestCalculation(CalculationStrategy):
    def __init__(self, ttest_model: TTestModel):
        self.ttest_model = ttest_model
        self.logger = logging.getLogger(__name__)

    def calculate(self, calculations: list) -> bool:
        try:
            # Create an empty DataFrame with the same number of rows as the input data
            self.ttest_model.results_df = pd.DataFrame(index=self.ttest_model.df.index)

            control_data = self.ttest_model.control_set_df
            change_data = self.ttest_model.change_set_df

            if 'All' in calculations:
                calculations = ['pValue', 'logPValue', 'foldChange', 'log2FoldChange']

            calculation_methods = {
                'pValue': self.calculate_pvalue,
                'logPValue': self.calculate_log_pvalue,
                'foldChange': self.calculate_fold_change,
                'log2FoldChange': self.calculate_log2_fold_change
            }

            for calc in calculations:
                if calc in calculation_methods:
                    calculation_methods[calc](control_data, change_data)

        except Exception as e:
            self.logger.error(f'Error in t-test calculations: {e}')
            return False

        return True

    def calculate_pvalue(self, control_data, change_data):
        p_values = []
        for i in range(control_data.shape[0]):
            control_row = control_data.iloc[i, 1:]
            change_row = change_data.iloc[i, 1:]
            from scipy.stats import stats
            t_stat, p_value = stats.ttest_rel(control_row, change_row)
            p_values.append(p_value)
        self.ttest_model.results_df['pValue'] = p_values

    def calculate_log_pvalue(self, control_data, change_data):
        self.ttest_model.results_df['logPValue'] = np.log(self.ttest_model.results_df['pValue'])

    def calculate_fold_change(self, control_data, change_data):
        self.ttest_model.results_df['foldChange'] = change_data.mean(axis=1) / control_data.mean(axis=1)

    def calculate_log2_fold_change(self, control_data, change_data):
        self.ttest_model.results_df['log2FoldChange'] = np.log2(self.ttest_model.results_df['foldChange'])
