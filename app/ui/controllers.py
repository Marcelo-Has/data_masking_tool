import tkinter as tk
from tkinter import filedialog, Toplevel, ttk
import pandas as pd

from app.ui.views import MainWindow
from app.services.mask import mask_data, save_masked_data
from app.config.settings import FIELD_TYPES
from app.utils import generate_uuid, generate_random_date
from datetime import datetime
import numpy as np

def run_app():
    root = tk.Tk()
    app = MainWindow(root)

    # Global variables
    df = None
    file_path = None

    # Global variables for configuration
    config_settings = {}
    column_settings = {}

    # Set up event handlers
    app.upload_button.config(command=lambda: process_file(app, config_settings, column_settings))
    app.generate_button.config(command=lambda: generate_fake_data(app, config_settings, column_settings))

    # Start the UI loop
    root.mainloop()

def process_file(app, config_settings, column_settings):
    global df, file_path
    file_path = filedialog.askopenfilename(
        filetypes=[
            ("CSV files", "*.csv"),
            ("Excel files", "*.xlsx"),
            ("Excel files", "*.xls"),
        ]
    )

    if not file_path:
        return  # Exit if no file is selected

    # Load the file with the selected delimiter for CSV files
    try:
        if file_path.endswith(".csv"):
            selected_delimiter = app.delimiter_var.get()
            df = pd.read_csv(file_path, delimiter=selected_delimiter, on_bad_lines='skip')
        elif file_path.endswith((".xlsx", ".xls")):
            df = pd.read_excel(file_path)
        else:
            app.log_text.insert(
                tk.END, "Unsupported file format. Please upload a CSV or Excel file.\n"
            )
            return
    except Exception as e:
        app.log_text.insert(tk.END, f"Error loading file: {e}\n")
        return

    app.log_text.insert(tk.END, f"File '{file_path}' loaded successfully.\n")

    # Display column settings for masking
    for widget in app.column_inner_frame.winfo_children():
        widget.destroy()  # Clear previous widgets

    column_settings.clear()
    for col in df.columns:
        col_var = tk.BooleanVar(value=False)
        field_type_var = tk.StringVar(value="Name")
        blank_percent_var = tk.DoubleVar(value=0.0)

        column_settings[col] = {
            "selected": col_var,
            "field_type": field_type_var,
            "blank_percent": blank_percent_var,
        }

        # Add checkbox
        checkbox = tk.Checkbutton(
            app.column_inner_frame,
            text=col,
            variable=col_var,
            command=lambda cv=col_var, col=col: toggle_inputs(
                cv,
                column_settings[col]["field_type_widget"],
                column_settings[col]["blank_percent_widget"],
                column_settings[col]["config_button"],
            ),
        )
        checkbox.pack(anchor="w")

        # Add dropdown for field type (initially disabled)
        field_type_dropdown = ttk.Combobox(
            app.column_inner_frame,
            textvariable=field_type_var,
            values=list(FIELD_TYPES.keys())
            + ["Row Number", "Custom List", "Number", "Date"],
            state="disabled",
        )
        field_type_dropdown.pack(anchor="w")

        # Add entry for blank percentage (initially disabled)
        blank_percent_entry = tk.Entry(
            app.column_inner_frame, textvariable=blank_percent_var, state="disabled"
        )
        blank_percent_entry.pack(anchor="w")

        # Configuration button (initially disabled)
        config_button = tk.Button(
            app.column_inner_frame,
            text="⚙️",
            state="disabled",
            command=lambda col=col, ft=field_type_var: open_config_pane(
                app.root, col, ft.get(), config_settings
            ),
        )
        config_button.pack(anchor="w")

        # Store widget references to enable/disable them in toggle_inputs
        column_settings[col]["field_type_widget"] = field_type_dropdown
        column_settings[col]["blank_percent_widget"] = blank_percent_entry
        column_settings[col]["config_button"] = config_button

    # Enable generate button
    app.generate_button.config(state="normal")

def toggle_inputs(checkbox_var, field_type_widget, blank_percent_widget, config_button):
    state = "normal" if checkbox_var.get() else "disabled"
    field_type_widget.config(state=state)
    blank_percent_widget.config(state=state)
    config_button.config(state=state)

def open_config_pane(root, field_name, field_type, config_settings):
    """Opens a configuration pane to set options for the field type."""
    config_window = Toplevel(root)
    config_window.title(f"Configure {field_type}")

    # Retrieve existing configuration if available
    existing_config = config_settings.get(field_name, {})

    # Save configuration data when user clicks "Save"
    def save_configuration():
        # Save prefix/suffix for applicable field types
        if field_type in [
            "Name",
            "Full Name",
            "Company",
            "Department",
            "Phone",
            "Email",
            "Product Name",
            "Row Number",
            "UUID",
        ]:
            prefix = prefix_entry.get()
            suffix = suffix_entry.get()
            config_settings[field_name] = {"prefix": prefix, "suffix": suffix}
            if field_type == "UUID":
                uuid_type = uuid_type_var.get()
                char_length = (
                    int(char_length_entry.get())
                    if uuid_type == "Alphanumeric Code"
                    else None
                )
                config_settings[field_name]["uuid_type"] = uuid_type
                config_settings[field_name]["char_length"] = char_length
        elif field_type == "Custom List":
            custom_values = list_entry.get("1.0", "end-1c").split(",")
            config_settings[field_name] = {"values": [v.strip() for v in custom_values]}
        elif field_type == "Number":
            min_value = float(min_entry.get())
            max_value = float(max_entry.get())
            is_integer = int_check.get()
            config_settings[field_name] = {
                "min": min_value,
                "max": max_value,
                "is_integer": is_integer,
            }
        elif field_type == "Date":
            start_date = start_date_entry.get()
            end_date = end_date_entry.get()
            config_settings[field_name] = {
                "start_date": start_date,
                "end_date": end_date,
            }

        config_window.destroy()

    # Add fields for prefix and suffix where applicable
    if field_type in [
        "Name",
        "Full Name",
        "Company",
        "Department",
        "Phone",
        "Email",
        "Product Name",
        "Row Number",
        "UUID",
    ]:
        tk.Label(config_window, text="Prefix:").grid(row=0, column=0)
        prefix_entry = tk.Entry(config_window)
        prefix_entry.insert(
            0, existing_config.get("prefix", "")
        )  # Load existing prefix
        prefix_entry.grid(row=0, column=1)
        tk.Label(config_window, text="Suffix:").grid(row=1, column=0)
        suffix_entry = tk.Entry(config_window)
        suffix_entry.insert(
            0, existing_config.get("suffix", "")
        )  # Load existing suffix
        suffix_entry.grid(row=1, column=1)
        row_offset = 2
    else:
        row_offset = 0

    # Additional configuration for UUID type
    if field_type == "UUID":
        tk.Label(config_window, text="UUID Type:").grid(row=row_offset, column=0)
        uuid_type_var = tk.StringVar(value=existing_config.get("uuid_type", "UUID"))
        uuid_type_dropdown = ttk.Combobox(
            config_window,
            textvariable=uuid_type_var,
            values=["UUID", "Alphanumeric Code"],
        )
        uuid_type_dropdown.grid(row=row_offset, column=1)

        # Additional option for character length when using Alphanumeric Code
        tk.Label(config_window, text="Character Length:").grid(
            row=row_offset + 1, column=0
        )
        char_length_entry = tk.Entry(config_window)
        char_length_value = str(
            existing_config.get("char_length", "8")
        )  # Ensure a string value
        char_length_entry.insert(0, char_length_value)  # Default to 8 if None
        char_length_entry.grid(row=row_offset + 1, column=1)

        # Show/Hide character length field based on selection
        def toggle_char_length(event):
            state = (
                "normal" if uuid_type_var.get() == "Alphanumeric Code" else "disabled"
            )
            char_length_entry.config(state=state)

        uuid_type_dropdown.bind("<<ComboboxSelected>>", toggle_char_length)
        toggle_char_length(None)  # Initialize visibility based on current selection

        row_offset += 2

    # Specific configurations for other field types
    if field_type == "Custom List":
        tk.Label(config_window, text="Enter values (comma-separated):").grid(
            row=row_offset, column=0
        )
        list_entry = tk.Text(config_window, width=30, height=5)
        list_entry.insert(
            "1.0", ",".join(existing_config.get("values", []))
        )  # Load existing values
        list_entry.grid(row=row_offset + 1, column=0, columnspan=2)
    elif field_type == "Number":
        tk.Label(config_window, text="Min Value:").grid(row=row_offset, column=0)
        min_entry = tk.Entry(config_window)
        min_entry.insert(0, existing_config.get("min", ""))  # Load existing min value
        min_entry.grid(row=row_offset, column=1)
        tk.Label(config_window, text="Max Value:").grid(row=row_offset + 1, column=0)
        max_entry = tk.Entry(config_window)
        max_entry.insert(0, existing_config.get("max", ""))  # Load existing max value
        max_entry.grid(row=row_offset + 1, column=1)
        int_check = tk.BooleanVar(value=existing_config.get("is_integer", False))
        tk.Checkbutton(config_window, text="Integer", variable=int_check).grid(
            row=row_offset + 2, column=0, columnspan=2
        )
    elif field_type == "Date":
        tk.Label(config_window, text="Start Date (YYYY-MM-DD):").grid(
            row=row_offset, column=0
        )
        start_date_entry = tk.Entry(config_window)
        start_date_entry.insert(
            0, existing_config.get("start_date", "")
        )  # Load start date
        start_date_entry.grid(row=row_offset, column=1)
        tk.Label(config_window, text="End Date (YYYY-MM-DD):").grid(
            row=row_offset + 1, column=0
        )
        end_date_entry = tk.Entry(config_window)
        end_date_entry.insert(0, existing_config.get("end_date", ""))  # Load end date
        end_date_entry.grid(row=row_offset + 1, column=1)

    # Save button for the configuration
    tk.Button(config_window, text="Save", command=save_configuration).grid(
        row=row_offset + 3, column=0, columnspan=2
    )

def generate_fake_data(app, config_settings, column_settings):
    selected_columns = {
        col: {
            "selected": settings["selected"],
            "field_type": settings["field_type"],
            "blank_percent": settings["blank_percent"],
        }
        for col, settings in column_settings.items()
    }

    keep_mapping = (
        app.keep_mapping_var.get()
    )  # Get the state of the "Keep Mapping Consistent" checkbox

    # Access the global variables df and file_path
    global df, file_path

    if df is None or file_path is None:
        app.log_text.insert(tk.END, "No data loaded. Please upload a file first.\n")
        return

    masked_df, log = mask_data(df, selected_columns, config_settings, keep_mapping)
    output_file = save_masked_data(masked_df, file_path, app.log_text)

    # Display logs
    if output_file:
        for entry in log:
            app.log_text.insert(tk.END, entry + "\n")
        app.log_text.insert(tk.END, f"Masked data saved to '{output_file}'\n")
