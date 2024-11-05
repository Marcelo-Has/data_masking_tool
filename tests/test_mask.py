import unittest
import pandas as pd
import numpy as np
from unittest.mock import MagicMock
from app.services.mask import mask_data, save_masked_data
from app.config.settings import FIELD_TYPES
from app.utils import generate_uuid, generate_random_date
from datetime import datetime
import tempfile
import os

class TestMask(unittest.TestCase):

    def setUp(self):
        # Sample DataFrame for testing
        self.df = pd.DataFrame({
            'Name': ['Alice', 'Bob', 'Charlie', 'David'],
            'Email': ['alice@example.com', 'bob@example.com', 'charlie@example.com', 'david@example.com'],
            'Age': [25, 30, 35, 40],
            'Date': pd.to_datetime(['2020-01-01', '2021-06-15', '2022-03-10', '2023-12-31'])
        })

        # Mock tkinter variables
        self.selected_columns = {
            'Name': {
                'selected': self.create_mock_var(True),
                'field_type': self.create_mock_var('Full Name'),
                'blank_percent': self.create_mock_var(0.0)
            },
            'Email': {
                'selected': self.create_mock_var(True),
                'field_type': self.create_mock_var('Email'),
                'blank_percent': self.create_mock_var(0.0)
            },
            'Age': {
                'selected': self.create_mock_var(True),
                'field_type': self.create_mock_var('Number'),
                'blank_percent': self.create_mock_var(0.0)
            },
            'Date': {
                'selected': self.create_mock_var(True),
                'field_type': self.create_mock_var('Date'),
                'blank_percent': self.create_mock_var(0.0)
            }
        }

        self.config_settings = {
            'Age': {
                'min': 20,
                'max': 60,
                'is_integer': True
            },
            'Date': {
                'start_date': '2020-01-01',
                'end_date': '2023-12-31'
            }
        }

    def create_mock_var(self, value):
        # Mock tkinter variable
        mock_var = MagicMock()
        mock_var.get.return_value = value
        return mock_var

    def test_mask_data_with_keep_mapping(self):
        masked_df, log = mask_data(
            self.df,
            self.selected_columns,
            self.config_settings,
            keep_mapping=True
        )

        # Ensure that original data is not the same as masked data
        self.assertFalse(self.df.equals(masked_df))

        # Check that names are masked
        self.assertFalse((masked_df['Name'] == self.df['Name']).any())

        # Check that emails are masked
        self.assertFalse((masked_df['Email'] == self.df['Email']).any())

        # Check that ages are within the specified range
        self.assertTrue(masked_df['Age'].between(20, 60).all())

        # Check that dates are within the specified range
        start_date = datetime.strptime('2020-01-01', '%Y-%m-%d')
        end_date = datetime.strptime('2023-12-31', '%Y-%m-%d')
        self.assertTrue(masked_df['Date'].between(start_date, end_date).all())

    def test_mask_data_without_keep_mapping(self):
        masked_df, log = mask_data(
            self.df,
            self.selected_columns,
            self.config_settings,
            keep_mapping=False
        )

        # Similar checks as before
        self.assertFalse((masked_df['Name'] == self.df['Name']).any())
        self.assertFalse((masked_df['Email'] == self.df['Email']).any())
        self.assertTrue(masked_df['Age'].between(20, 60).all())
        start_date = datetime.strptime('2020-01-01', '%Y-%m-%d')
        end_date = datetime.strptime('2023-12-31', '%Y-%m-%d')
        self.assertTrue(masked_df['Date'].between(start_date, end_date).all())

    def test_blank_percent_effect(self):
        # Set blank_percent to 0.5 for the 'Name' column
        self.selected_columns['Name']['blank_percent'] = self.create_mock_var(0.5)

        masked_df, log = mask_data(
            self.df,
            self.selected_columns,
            self.config_settings,
            keep_mapping=False
        )

        # Check that approximately half of the 'Name' entries are None
        num_blanks = masked_df['Name'].isnull().sum()
        self.assertTrue(1 <= num_blanks <= 3)

    def test_save_masked_data(self):
        # Create a temporary file path
        temp_original_file = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
        temp_original_file.close()

        # Save the DataFrame to the temporary file
        self.df.to_excel(temp_original_file.name, index=False)

        # Mock log_text
        log_text = MagicMock()
        log_text.insert = MagicMock()

        # Since save_masked_data involves file dialogs, we will mock filedialog.asksaveasfilename
        from unittest.mock import patch

        with patch('data_masking_tool.services.mask.filedialog.asksaveasfilename') as mock_saveas:
            # Mock the save location
            mock_saveas.return_value = temp_original_file.name  # Overwrite the same file for testing

            # Call save_masked_data
            output_file = save_masked_data(self.df, temp_original_file.name, log_text)

            # Check that output_file is not None
            self.assertIsNotNone(output_file)

            # Check that the file exists
            self.assertTrue(os.path.exists(output_file))

        # Clean up temporary files
        os.remove(temp_original_file.name)

    # Additional tests can be added here

if __name__ == '__main__':
    unittest.main()
