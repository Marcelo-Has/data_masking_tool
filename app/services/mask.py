import numpy as np
import pandas as pd
import random
import tempfile
import shutil
import time
import os
from datetime import datetime

from tkinter import filedialog

from app.config.settings import FIELD_TYPES, fake
from app.utils import generate_uuid, generate_random_date

def mask_data(df, selected_columns, config_settings, keep_mapping=True):
    masked_df = df.copy()  # Copy the original data
    log = []

    # Dictionary to store mappings for each column if "Keep Mapping Consistent" is enabled
    column_fake_mappings = {}

    # Iterate over selected columns and apply fake data where needed
    for col, settings in selected_columns.items():
        if settings["selected"].get():
            field_type = settings["field_type"].get()
            blank_percent = settings["blank_percent"].get()

            # Generate fake data with or without keeping mappings
            if keep_mapping:
                # Generate mappings for unique values in the column to keep them consistent
                unique_values = df[col].unique()
                if col not in column_fake_mappings:
                    fake_mapping = {}
                    if field_type == "Custom List":
                        values = config_settings[col].get("values", [])
                        for idx, val in enumerate(unique_values):
                            fake_mapping[val] = (
                                None
                                if np.random.rand() < blank_percent
                                else values[idx % len(values)]
                            )
                    elif field_type == "Number":
                        min_val = config_settings[col].get("min", 0)
                        max_val = config_settings[col].get("max", 1)
                        is_integer = config_settings[col].get("is_integer", False)
                        for val in unique_values:
                            fake_mapping[val] = (
                                None
                                if np.random.rand() < blank_percent
                                else (
                                    random.randint(int(min_val), int(max_val))
                                    if is_integer
                                    else round(random.uniform(min_val), 2)
                                )
                            )
                    elif field_type == "Date":
                        start_date = datetime.strptime(
                            config_settings[col].get("start_date", "2020-01-01"),
                            "%Y-%m-%d",
                        )
                        end_date = datetime.strptime(
                            config_settings[col].get("end_date", "2023-12-31"),
                            "%Y-%m-%d",
                        )
                        for val in unique_values:
                            fake_mapping[val] = (
                                None
                                if np.random.rand() < blank_percent
                                else generate_random_date(start_date, end_date)
                            )
                    elif field_type == "UUID":
                        prefix = config_settings[col].get("prefix", "")
                        suffix = config_settings[col].get("suffix", "")
                        uuid_type = config_settings[col].get("uuid_type", "UUID")
                        char_length = config_settings[col].get("char_length", 8)
                        for val in unique_values:
                            fake_mapping[val] = (
                                None
                                if np.random.rand() < blank_percent
                                else (
                                    f"{prefix}{generate_uuid()}{suffix}"
                                    if uuid_type == "UUID"
                                    else f"{prefix}{fake.bothify('?' * char_length)}{suffix}"
                                )
                            )
                    else:
                        for val in unique_values:
                            fake_mapping[val] = (
                                None
                                if np.random.rand() < blank_percent
                                else FIELD_TYPES[field_type]()
                            )
                    column_fake_mappings[col] = fake_mapping
                # Map values based on the generated mapping
                masked_df[col] = df[col].map(column_fake_mappings[col])
            else:
                # Generate new fake data for each row independently when keep_mapping is False
                if field_type == "Custom List":
                    values = config_settings[col].get("values", [])
                    fake_data = [
                        (
                            None
                            if np.random.rand() < blank_percent
                            else random.choice(values)
                        )
                        for _ in range(len(df))
                    ]
                elif field_type == "Number":
                    min_val = config_settings[col].get("min", 0)
                    max_val = config_settings[col].get("max", 1)
                    is_integer = config_settings[col].get("is_integer", False)
                    fake_data = [
                        (
                            None
                            if np.random.rand() < blank_percent
                            else (
                                random.randint(int(min_val), int(max_val))
                                if is_integer
                                else round(random.uniform(min_val), 2)
                            )
                        )
                        for _ in range(len(df))
                    ]
                elif field_type == "Date":
                    start_date = datetime.strptime(
                        config_settings[col].get("start_date", "2020-01-01"), "%Y-%m-%d"
                    )
                    end_date = datetime.strptime(
                        config_settings[col].get("end_date", "2023-12-31"), "%Y-%m-%d"
                    )
                    fake_data = [
                        (
                            None
                            if np.random.rand() < blank_percent
                            else generate_random_date(start_date, end_date)
                        )
                        for _ in range(len(df))
                    ]
                elif field_type == "UUID":
                    prefix = config_settings[col].get("prefix", "")
                    suffix = config_settings[col].get("suffix", "")
                    uuid_type = config_settings[col].get("uuid_type", "UUID")
                    char_length = config_settings[col].get("char_length", 8)
                    fake_data = [
                        (
                            None
                            if np.random.rand() < blank_percent
                            else (
                                f"{prefix}{generate_uuid()}{suffix}"
                                if uuid_type == "UUID"
                                else f"{prefix}{fake.bothify('?' * char_length)}{suffix}"
                            )
                        )
                        for _ in range(len(df))
                    ]
                else:
                    fake_data = [
                        (
                            None
                            if np.random.rand() < blank_percent
                            else FIELD_TYPES[field_type]()
                        )
                        for _ in range(len(df))
                    ]
                # Apply generated fake data to the entire column
                masked_df[col] = fake_data
            log.append(
                f"Masked column '{col}' with fake data ({field_type}) and {blank_percent*100}% blanks."
            )
        else:
            log.append(f"Column '{col}' was not selected for masking.")

    # Retain original values for unselected columns only if keep_mapping is True
    if keep_mapping:
        for col in df.columns:
            if (
                col not in selected_columns
                or not selected_columns[col]["selected"].get()
            ):
                masked_df[col] = df[col]  # Keep original values for unmasked columns

    return masked_df, log

def save_masked_data(df, original_file, log_text):
    retry_attempts = 3  # Number of attempts to retry saving
    for attempt in range(retry_attempts):
        try:
            # Use a unique temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
                temp_output_file = temp_file.name

            with pd.ExcelWriter(temp_output_file, engine="xlsxwriter") as writer:
                df.to_excel(writer, index=False, sheet_name="Masked Data")
            log_text.insert(
                "end", f"File saved temporarily to '{temp_output_file}'.\n"
            )

            # Ask user for the final save location
            file_name, _ = os.path.splitext(original_file)
            initial_filename = file_name + "_masked.xlsx"
            final_output_file = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                initialfile=initial_filename,
                filetypes=[("Excel files", "*.xlsx")],
                title="Select Save Location",
            )

            if final_output_file:
                # Try copying to final location
                shutil.copy(temp_output_file, final_output_file)
                log_text.insert(
                    "end", f"File successfully saved to '{final_output_file}'.\n"
                )
                # Clean up the temporary file
                os.remove(temp_output_file)
                return final_output_file
            else:
                log_text.insert("end", "Save operation canceled.\n")
                return None

        except PermissionError as e:
            log_text.insert("end", f"Attempt {attempt + 1}: Permission error - {e}\n")
            time.sleep(1)  # Short delay before retrying

        except Exception as e:
            log_text.insert("end", f"Error saving file: {e}\n")
            return None

    log_text.insert("end", "Failed to save after multiple attempts.\n")
    return None
