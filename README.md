# BioCalc - A Biological Data Analysis Tool

## Overview

BioCalc is a robust tool designed for the analysis of biological data. It supports various types of calculations 
and graph generations tailored to the user's needs. The tool is highly configurable, allowing for detailed customization 
of calculations and visualizations.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Tool](#running-the-tool)
- [Features](#features)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [User Configuration Guide](#User Configuration Guide)

## Prerequisites

- Python 3.x
- Pip (Python package installer)

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/bioCalc.git
    ```

2. **Navigate to the Project Directory**

    ```bash
    cd bioCalc
    ```

3. **Install Required Packages**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

The tool is configured via an `application.yaml` file located in the `src/resources/` directory. This file includes settings for:

- Logging level
- Fixed columns in the input Excel file
- Supported graph types
- Input Excel file path

For a detailed explanation of user-specific options in `application.yaml`, refer to the [User Configuration Guide](#user-configuration-guide) section below.

## Running the Tool

To run the tool, navigate to the directory containing `bioCalcApp.py` and execute:

```bash
python bioCalcApp.py
```

Follow the on-screen prompts to perform calculations and generate reports.

## Features

- **T-Test Calculations**: Statistical tests like T-Test.
- **Graph Generation**: Various types of graphs including Bar, Volcano, HeatMap, etc.
- **Excel Reporting**: Comprehensive Excel reports with both raw data and results.
- **Customization**: Easily configurable via the `application.yaml` configuration file.

## Project Structure

The directory structure of BioCalc is organized as follows:

```plaintext
.
├── README.md                       # This README file, containing all project documentation
├── requirements.txt                # File containing the required Python packages for the project
├── results                         # Directory where all the output files are stored
│   ├── geneExpressionAnalysis.xlsx # Sample Excel file for gene expression analysis results
│   ├── graph.png                   # Sample graph output as an image
│   └── ...                         # Other generated output files
└── src                             # Source code directory
    ├── main                        # Main application code
    │   └── python
    │       └── app
    │           ├── bioCalcApp.py    # Main application entry point
    │           ├── calculation      # Contains all calculation logic and algorithms
    │           │   ├── calculationStrategy.py  # Strategy pattern interface for calculations
    │           │   └── tTestCalculation.py     # T-Test calculation implementation
    │           ├── config           # Configuration related code
    │           │   └── appConfig.py # Class to load and manage application configuration
    │           ├── constants        # Constants used throughout the application
    │           │   └── constants.py # File containing all the constant values
    │           ├── model            # Data models for the application
    │           │   ├── tTestModel.py     # Model for T-Test data
    │           │   └── userInputModel.py # Model for capturing user input
    │           ├── reporting        # Reporting logic and classes
    │           │   ├── excelReport.py  # Class to generate Excel reports
    │           │   ├── graphViewer.py  # Class to display graphs
    │           │   └── imageReport.py  # Class to save graphs as image files
    │           ├── service          # Service layer classes
    │           │   ├── calculationService.py # Orchestrates the calculation process
    │           │   ├── reportingService.py   # Orchestrates the reporting process
    │           │   └── userInputService.py   # Manages the user input
    │           ├── utils            # Utility functions and helpers
    │           │   └── generalUtils.py # General utility functions
    │           ├── validation       # Validation logic for data and models
    │           │   ├── dataValidatorStrategy.py  # Strategy pattern interface for data validation
    │           │   └── tTestDataValidator.py     # T-Test data validation implementation
    │           └── visualization    # Code related to data visualization
    │               └── graphModule.py  # Class to handle all graphing logic
    └── resources                    # Configuration files and other resources
        └── application.yaml         # Main configuration file

```

## Troubleshooting

For troubleshooting, please refer to the generated log files in the `logs` directory or open an issue on GitHub.


## User Configuration Guide

### `user` Configuration Key

#### `calculation_option`

- **Description**: Specifies the type of calculation to perform.
- **Options**: "ttest", "another_calculation"
- **Mandatory**: Yes

#### `reporting`

This is a nested key containing various reporting options.

##### `generateReport`

- **Description**: Whether to generate an Excel report.
- **Options**: true, false
- **Mandatory**: Yes

##### `filePath`

- **Description**: The file path where the Excel report will be saved. 
- **Mandatory**: Yes, if `generateReport` is set to true.

##### `sheetNames`

A nested key to specify sheet names in the Excel report.

- **data_sheet**: Sheet name for raw data.
- **result_sheet**: Sheet name for results.
- **Optional**: Yes

##### `reportGraphOptions`

A nested key for various graph options within the report.

- **includeInExcel**: Whether to include the graph in the Excel report.
  - **Optional**: Yes
- **separateImage**: Whether to save the graph as a separate image file.
  - **Optional**: Yes
- **imageFormat**: The format in which the image will be saved (e.g., png, jpg).
  - **Optional**: Yes

#### `options`

This is a list of dictionaries containing optional settings for both calculations and graphs.

##### `ttestOptions`

A dictionary for t-test-specific options.

- **calculations**: Types of calculations to perform like pValue, logPValue, etc.
  - **Mandatory**: Yes
- **sortBy**: The column by which to sort the results.
  - **Optional**: Yes
- **ascending**: Sort order; true for ascending, false for descending.
  - **Optional**: Yes

##### `graphOptions`

A dictionary for graph-specific options.

- **graphType**: Specifies the type of graph to generate.
  - **Mandatory**: Yes
- **xAxis**: The variable for the X-axis.
  - **Optional**: Yes, but mandatory if `includeInExcel` or `separateImage` is true.
- **yAxis**: The variable for the Y-axis.
  - **Optional**: Yes, but mandatory if `includeInExcel` or `separateImage` is true.
- **color**: Color scheme for the graph.
  - **Optional**: Yes
- **hue**: Variable for color encoding.
  - **Optional**: Yes
- **style**: Style of the graph like ggplot, seaborn, etc.
  - **Optional**: Yes, but mandatory if `includeInExcel` or `separateImage` is true.
- **palette**: Color palette to use.
  - **Optional**: Yes
- **title**: Title of the graph.
  - **Optional**: Yes, but mandatory if `includeInExcel` or `separateImage` is true.
- **xLabel**: Label for the X-axis.
  - **Optional**: Yes
- **yLabel**: Label for the Y-axis.
  - **Optional**: Yes
- **dpi**: Dots per inch for image quality.
  - **Optional**: Yes

---
