import tkinter as tk
from tkinter import ttk
from src.main.python.app.calculation.tTestCalculation import TTestCalculation
from src.main.python.app.config.appConfig import AppConfig
from src.main.python.app.gui.TTestTab import TTestTab
from src.main.python.app.model.tTestModel import TTestModel
from src.main.python.app.model.userInputModel import UserInputModel
from src.main.python.app.validation.dataValidatorStrategy import DataValidatorStrategy
from src.main.python.app.visualization.graphModule import GraphModule


class MainPageGUI(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.pack(expand=1, fill="both")

        # Initialize other modules and models
        app_config = AppConfig()
        user_input_model = UserInputModel()
        data_validator = DataValidatorStrategy(app_config=app_config)
        ttest_model = TTestModel(data_validator=data_validator, app_config=app_config)
        ttest_module = TTestCalculation(ttest_model, user_input_model)
        graph_module = GraphModule(ttest_model, user_input_model, app_config)

        # Create a tab control
        tab_control = ttk.Notebook(self)

        # Create a TTestTab and add it to the Notebook
        ttest_tab = TTestTab(tab_control, ttest_model, user_input_model, ttest_module, graph_module, app_config)
        tab_control.add(ttest_tab, text="T-Test")

        # Pack the tab control
        tab_control.pack(expand=1, fill="both")


# if __name__ == "__main__":
#     app = MainPageGUI()
#     app.mainloop()
