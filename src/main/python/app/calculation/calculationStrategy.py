from abc import ABC, abstractmethod
import pandas as pd


class CalculationStrategy(ABC):

    @abstractmethod
    def calculate(self, calculations: list) -> bool:
        """Perform the required calculation."""
        pass
