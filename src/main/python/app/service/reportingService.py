import os
from datetime import datetime

from src.main.python.app.model.tTestModel import TTestModel
from src.main.python.app.model.userInputModel import UserInputModel
from src.main.python.app.reporting.excelReport import ExcelReport
from src.main.python.app.reporting.graphViewer import GraphViewer
from src.main.python.app.reporting.imageReport import ImageReport


class ReportingService:
    def __init__(self, ttest_model: TTestModel, user_input_model: UserInputModel):
        self.ttest_model = ttest_model
        self.user_input_model = user_input_model
        self.reporting_options = self.user_input_model.reporting_options
        self.report_graph_options = self.reporting_options.report_graph_options

    def generate_reports(self, fig):
        """Main method to generate all reports based on user input."""
        self._display_graph(fig)
        self._generate_excel_report(fig)
        self._generate_image_report(fig)

    def _generate_excel_report(self, fig):
        """Generate Excel report if required."""
        if self.reporting_options.generate_report:
            excel_report = ExcelReport(self.ttest_model, self.user_input_model)
            if self.report_graph_options.include_in_excel:
                # Include the graph in the Excel report
                excel_report.save_to_excel(fig)
            else:
                # Generate only the Excel report without the graph
                excel_report.save_to_excel()

    def _generate_image_report(self, fig):
        """Generate a separate image file for the graph if required."""
        if self.report_graph_options.separate_image:
            # Get directory path from the file path and the base file name
            dir_path = os.path.dirname(self.reporting_options.file_path)
            base_file_name = os.path.basename(self.reporting_options.file_path).split(".")[0]
            # Get current time and format it as a string
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            # Construct the image file path with a timestamp with the format: graph_<base_file_name>_<timestamp>.<image_format>
            image_path = f"{dir_path}/graph_{base_file_name}_{timestamp}.{self.report_graph_options.image_format}"

            image_report = ImageReport(image_path)
            # Save the graph as a separate image file
            image_report.save_graph_as_png(fig)

    def _display_graph(self, fig):
        """Display the graph if either include in Excel or save as separate image are chosen."""
        graph_viewer = GraphViewer(self.user_input_model)
        if self.report_graph_options.include_in_excel or self.report_graph_options.separate_image:
            # Display the graph
            if self.user_input_model.calculation_option == "ttest":
                graph_viewer.display_graph(self.ttest_model)
