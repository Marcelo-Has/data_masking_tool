# Data Masking Tool

A Python application for masking sensitive data in CSV and Excel files using customizable fake data.

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Documentation](#documentation)
- [Executable](#executable)
- [Contributing](#contributing)
- [Author](#author)
- [License](#license)

## Description

The Data Masking Tool is designed to help users anonymize sensitive data within CSV and Excel files. It replaces selected columns with fake data generated using the [Faker](https://faker.readthedocs.io/en/master/) library. The tool provides a graphical user interface (GUI) built with Tkinter, allowing users to easily select columns to mask, configure fake data types, and customize settings.

## Features

- Supports CSV and Excel (`.xlsx`, `.xls`) files.
- Customizable masking options for each column.
- Multiple fake data types, including names, emails, phone numbers, dates, and more.
- Configurable settings for fake data generation (e.g., prefixes, suffixes, ranges).
- Option to keep mappings consistent across the dataset.
- Ability to introduce blank values at a specified percentage.
- Simple and intuitive GUI.
- Generates a masked data file without altering the original file.

## Installation

### Prerequisites

- Python 3.6 or higher.
- Required Python libraries:
  - `pandas`
  - `numpy`
  - `faker`
  - `openpyxl`
  - `xlsxwriter`
  - `xlrd`
  - `tkinter` (comes pre-installed with Python on most systems)

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Marcelo-Has/data-masking-tool.git
   cd data-masking-tool

2. **Create a Virtual Environment (Recommended)**

   ```bash
   python -m venv venv

3. **Activate the Virtual Environment**

  - On Windows:

     ```bash
     venv\Scripts\activate

  - On macOS/Linux:

     ```bash
     source venv/bin/activate

4. **Install Dependencies**

   ```bash
   pip install -r data_masking_tool/app/docs/requirements.txt

5. **Run the Application**

   ```bash
   python data_masking_tool/main.py

## Usage

1. **Launch the Application**

    Run the main script:

       python data_masking_tool/main.py

2. **Select CSV Delimiter (If Applicable)**

  If you're working with CSV files, choose the appropriate delimiter from the dropdown menu.

3. **Upload a File**

  Click on the **"Upload and Mask Data"** button and select the CSV or Excel file you wish to mask.

4. **Select Columns to Mask**

  - Check the boxes next to the columns you want to mask.
  - For each selected column:
    - Choose the **Field Type** for fake data generation.
    - Optionally, set the **Blank Percentage** to introduce null values.
    - Click on the ⚙️ button to configure additional settings.

5. **Configure Fake Data (Optional)**

  Customize settings such as prefixes, suffixes, ranges, and custom lists in the configuration pane.

6. **Generate Fake Data**

  Click the **"Generate Fake Data"** button to start the masking process.

7. **Save the Masked Data**

  After processing, you'll be prompted to choose a location to save the masked file. The default filename will be the original name appended with `_masked.xlsx`.

8. **View Logs**

  Monitor the progress and view detailed logs in the log display area within the application.

## Examples

### Masking a CSV File

1. Launch the application.

2. Select the comma (`,`) delimiter, or the appropriate one.

3. Upload your `data.csv`, `data.xlsx`, or `data.xls` file.

4. Select columns like `Name`, `Email`, and `Phone` to mask.

5. Configure each field type as desired.

6. Generate the fake data and save the output.

  **Note**: Your computer may deny saving depending on the folder (for example the downloads folder), in this case try saving in another folder, such as on the desktop.

### Customizing Fake Data

- Use the **Custom List** field type to mask a column with specific values.
- Set up a **Number** field type to generate random integers within a range.
- Configure the **Date** field type to generate random dates between two specified dates.


## Documentation

### Supported Field Types

- **Name**
- **Full Name**
- **Address**
- **Phone**
- **Email**
- **UUID**
- **Company**
- **Department**
- **City**
- **Country**
- **Zip Code**
- **Product Name**
- **State or Province**
- **Row Number**
- **Custom List**
- **Number**
- **Date**


### Configuration Options

- **Prefix/Suffix**: Add custom text before or after the generated fake data.
- **Blank Percentage**: Specify the percentage of blank (null) values to introduce.
- **Custom Lists**: Provide a list of custom values for masking.
- **Number Ranges**: Set minimum and maximum values for numeric fields.
- **Date Ranges**: Define start and end dates for date fields.
- **UUID Types**: Choose between standard UUIDs or custom alphanumeric codes.

## Executable

If you prefer to use the application without setting up the development environment, you can use the standalone executable file.

- The executable file can be found in the `dist` folder.
- **Path**: `dist/DataMaskingTool.exe`
- **Usage**:
  Navigate to the `dist` directory.
  Run the executable:
    On Windows: Double-click `DataMaskingTool.exe` or run it via command prompt.

**Note**: The executable includes all necessary dependencies and can be run on any Windows machine without installing Python or additional libraries.

## Contributing

Contributions are welcome! To contribute:

1. **Fork the Repository**

  Click the **Fork** button on the top right to create a copy of this repository on your GitHub account.

2. **Clone Your Fork**

   ```bash
   git clone https://github.com/Marcelo-Has/data-masking-tool.git

3. **Create a Feature Branch**

   ```bash
   git checkout -b feature/your-feature-name

4. **Commit Your Changes**

   ```bash
   git commit -am 'Add new feature'

5. **Push to the Branch**

   ```bash
   git push origin feature/your-feature-name

6. **Open a Pull Request**

  Submit a pull request to the main repository for review.

### Coding Guidelines

- Follow PEP 8 style guidelines.
- Write clear, concise commit messages.
- Include docstrings and comments where necessary.
- Update or add tests for new features.

### Reporting Issues

- Use the GitHub issue tracker to report bugs or request features.
- Provide detailed information and steps to reproduce issues.

## Author

Created by **Marcelo Has**
- **Email**: [marcelo_has@outlook.com](mailto:marcelo_has@outlook.com)
- **GitHub**: [Marcelo-Has](https://github.com/Marcelo-Has/)
- **Linkedin**: [marcelo_has@outlook.com](https://www.linkedin.com/in/marcelohas/)

## License

This project is licensed under the [MIT License](LICENSE).

Feel free to reach out with questions, suggestions, or contributions!