import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

from src.main.python.app.calculation.tTestCalculation import TTestCalculation
from src.main.python.app.config.appConfig import AppConfig
from src.main.python.app.model.tTestModel import TTestModel
from src.main.python.app.model.userInputModel import UserInputModel
from src.main.python.app.visualization.graphModule import GraphModule


class TTestTab(tk.Frame):
    def __init__(self, parent, ttest_model: TTestModel, user_input_model: UserInputModel,
                 ttest_module: TTestCalculation, graph_module: GraphModule, app_config: AppConfig):
        tk.Frame.__init__(self, parent)
        self.execute_button = None
        self.graph_dropdown = None
        self.graph_var = None
        self.graph_label = None
        self.calc_dropdown = None
        self.calc_var = None
        self.calc_label = None
        self.file_button = None
        self.file_entry = None
        self.file_label = None
        self.ttest_model = ttest_model
        self.user_input_model = user_input_model
        self.ttest_module = ttest_module
        self.graph_module = graph_module
        self.app_config = app_config

        # Create and place widgets
        self.create_widgets()

    def create_widgets(self):
        # File selection
        self.file_label = ttk.Label(self, text="Select Excel File:")
        self.file_label.grid(row=0, column=0)
        self.file_entry = ttk.Entry(self)
        self.file_entry.grid(row=0, column=1)
        self.file_button = ttk.Button(self, text="Browse", command=self.browse_file)
        self.file_button.grid(row=0, column=2)

        # Calculation Types Dropdown
        self.calc_label = ttk.Label(self, text="Select Calculation:")
        self.calc_label.grid(row=1, column=0)
        self.calc_var = tk.StringVar(value="pValue")
        self.calc_dropdown = ttk.Combobox(self, textvariable=self.calc_var)
        self.calc_dropdown['values'] = ['pValue', 'logPValue', 'foldChange', 'log2FoldChange', 'All']
        self.calc_dropdown.grid(row=1, column=1)

        # Graph Types Dropdown
        self.graph_label = ttk.Label(self, text="Select Graph:")
        self.graph_label.grid(row=2, column=0)
        self.graph_var = tk.StringVar(value="Bar")
        self.graph_dropdown = ttk.Combobox(self, textvariable=self.graph_var)
        self.graph_dropdown['values'] = self.app_config.supported_graph_types
        self.graph_dropdown.grid(row=2, column=1)

        # Execute button
        self.execute_button = ttk.Button(self, text="Execute", command=self.execute)
        self.execute_button.grid(row=3, columnspan=3)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)

    def execute(self):
        file_path = self.file_entry.get()
        if not file_path:
            messagebox.showerror("Error", "No Excel file selected")
            return

        if not self.ttest_model.load_from_excel(file_path):
            messagebox.showerror("Error", "Failed to load Excel file.")
            return

        # Update UserInputModel based on GUI selections
        self.user_input_model.ttest_options.sort_by = self.calc_var.get()
        self.user_input_model.graph_options.graph_type = self.graph_var.get()

        # Perform calculation
        if not self.ttest_module.calculate_ttest():
            messagebox.showerror("Error", "Failed to perform t-test calculation.")
            return

        # Generate graph
        if not self.graph_module.generate_graph():
            messagebox.showerror("Error", "Failed to generate graph.")
            return

        # Save graph to Excel
        self.graph_module.save_graph_to_excel()

        messagebox.showinfo("Success", "Calculations and graph generation were successful.")
