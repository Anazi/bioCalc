# import tkinter as tk
# from tkinter import ttk
# from tkinter import filedialog
#
# from src.main.python.app.model.userInputModel import UserInputModel
# from src.main.python.app.service.calculationService import CalculationService
#
#
# class BioCalcGUI:
#
#     def __init__(self, master):
#         self.master = master
#         self.master.title('BioCalc')
#         self.master.geometry('400x400')
#
#         self.user_input_model = UserInputModel()
#
#         self.label1 = ttk.Label(self.master, text='File Path:')
#         self.label1.grid(row=0, column=0)
#         self.file_path = tk.StringVar()
#         self.entry1 = ttk.Entry(self.master, textvariable=self.file_path)
#         self.entry1.grid(row=0, column=1)
#         self.button1 = ttk.Button(self.master, text='Browse', command=self.browse_file)
#         self.button1.grid(row=0, column=2)
#
#         self.label2 = ttk.Label(self.master, text='Calculations:')
#         self.label2.grid(row=1, column=0, sticky=tk.W)
#         # Calculations Check-buttons
#         self.calc_options = ['pValue', 'logPValue', 'foldChange', 'log2FoldChange']
#         self.calculations = {calc: tk.BooleanVar() for calc in self.calc_options}
#         col_index = 1
#         for calc, var in self.calculations.items():
#             c = ttk.Checkbutton(self.master, text=calc, variable=var)
#             c.grid(row=1, column=col_index)
#             col_index += 1
#
#         self.label3 = ttk.Label(self.master, text='Graph Type:')
#         self.label3.grid(row=2, column=0)
#         self.graph_type = tk.StringVar()
#         self.gui_graph_options = ['HeatMap', 'Volcano', 'Bar', 'Dot', 'Pie']  # Fixed set of graph types
#         self.combo3 = ttk.Combobox(self.master, textvariable=self.graph_type, values=self.gui_graph_options)
#         self.combo3.grid(row=2, column=1)
#
#         self.label4 = ttk.Label(self.master, text='X Axis:')
#         self.label4.grid(row=3, column=0)
#         self.x_axis = tk.StringVar()
#         self.entry4 = ttk.Entry(self.master, textvariable=self.x_axis)
#         self.entry4.grid(row=3, column=1)
#
#         self.label5 = ttk.Label(self.master, text='Y Axis:')
#         self.label5.grid(row=4, column=0)
#         self.y_axis = tk.StringVar()
#         self.entry5 = ttk.Entry(self.master, textvariable=self.y_axis)
#         self.entry5.grid(row=4, column=1)
#
#         self.label6 = ttk.Label(self.master, text='Sort By:')
#         self.label6.grid(row=5, column=0)
#         self.sort_by = tk.StringVar()
#         self.entry6 = ttk.Entry(self.master, textvariable=self.sort_by)
#         self.entry6.grid(row=5, column=1)
#
#         self.button2 = ttk.Button(self.master, text='Run', command=self.run_calculation)
#         self.button2.grid(row=6, column=1)
#
#     def browse_file(self):
#         self.file_path.set(filedialog.askopenfilename())
#
#     def run_calculation(self):
#         # Populate UserInputModel
#         self.user_input_model.ttest_options.file_path = self.file_path.get()
#
#         selected_calculations = [
#             calc for calc, var in self.calculations.items() if var.get()
#         ]
#         self.user_input_model.ttest_options.calculations = selected_calculations
#
#         graph_details_provided = self.graph_type.get() and self.x_axis.get() and self.y_axis.get()
#         self.user_input_model.graph_options.generate_graph = graph_details_provided
#         if graph_details_provided:
#             self.user_input_model.graph_options.graph_type = self.graph_type.get()
#             self.user_input_model.graph_options.graph_type = self.graph_type.get()
#             self.user_input_model.graph_options.x_axis = self.x_axis.get()
#             self.user_input_model.graph_options.y_axis = self.y_axis.get()
#
#         self.user_input_model.ttest_options.sort_by = self.sort_by.get()
#
#         # Run the service layer
#         service = CalculationService(self.user_input_model)
#
#         if service.perform_operations():
#             print("Calculations and/or graphs performed and saved successfully.")
#         else:
#             print("Calculations failed.")
#
#
# if __name__ == '__main__':
#     root = tk.Tk()
#     app = BioCalcGUI(root)
#     root.mainloop()
