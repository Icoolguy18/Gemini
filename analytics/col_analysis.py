import pandas as pd
import json
import numpy as np
from collections import defaultdict

#check the application for this file 

class DataProcessor:
    def __init__(self, data):
        self.data = data
        self.processed_data = {}

    def process_tabular_data(self):
        """
        Process tabular data (CSV) and create a dictionary of columns and their entries.
        """
        if isinstance(self.data, pd.DataFrame):
            for column in self.data.columns:
                column_data = self.data[column]
                column_entries = self.identify_column_entries(column_data)
                self.processed_data[column] = column_entries
        else:
            print("Provided data is not a DataFrame.")

    def process_json_data(self):
        """
        Process JSON data and create a dictionary of column names and their entries.
        """
        if isinstance(self.data, dict):
            # Flatten the JSON into a DataFrame
            json_df = pd.json_normalize(self.data)
            for column in json_df.columns:
                column_data = json_df[column]
                column_entries = self.identify_column_entries(column_data)
                self.processed_data[column] = column_entries
        else:
            print("Provided data is not a valid JSON object.")

    def identify_column_entries(self, column_data):
        """
        Identify the type of each entry in a column and return a list of entries with types.
        """
        entries_with_type = []
        for value in column_data:
            value_type = type(value).__name__
            if isinstance(value, (int, float)):
                entries_with_type.append((value, 'numeric'))
            elif isinstance(value, str):
                entries_with_type.append((value, 'string'))
            elif isinstance(value, bool):
                entries_with_type.append((value, 'boolean'))
            elif isinstance(value, (pd.Timestamp, np.datetime64)):
                entries_with_type.append((value, 'date'))
            else:
                entries_with_type.append((value, 'unknown'))
        return entries_with_type

    def get_processed_data(self):
        """
        Return the processed data dictionary.
        """
        return self.processed_data
