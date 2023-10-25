from abc import ABC, abstractmethod
import pandas as pd


class DataValidatorStrategy(ABC):

    @abstractmethod
    def validate_columns(self, df: pd.DataFrame) -> bool:
        pass

    @abstractmethod
    def validate_data(self, df: pd.DataFrame) -> bool:
        pass

    @abstractmethod
    def validate_no_nulls(self, df: pd.DataFrame) -> bool:
        pass
