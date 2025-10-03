import os
import csv
from datetime import datetime


curr_dt = datetime.now().strftime('%Y.%m.%d_%H.%M.%S')


class DataExporter:
    """
    Handles exporting data to CSV, SQLite, or both based on the specified mode
    """

    def __init__(self, mode='csv', filename=f'data_{curr_dt}'):
        """
        Initialize export mode and filename, defaulting to CSV and timestamped name
        """
        self.mode = mode.lower()
        self.filename = filename

        if self.mode not in ['csv', 'sqlite', 'both']:
            self.mode = 'csv'

        self.filepath = f"{self.filename}.{self.mode}"
        dirpath = os.path.dirname(self.filepath)
        if dirpath:
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)

    def _save_to_csv(self, data):
        """
        Internal method to save data to a CSV file
        """
        try:
            fieldnames = ''
            if isinstance(data, dict):
                fieldnames = list(data.keys())
            elif isinstance(data[0], dict):
                fieldnames = list(data[0].keys())
            else:
                raise ValueError("Data must be a dict or a list/tuple with a dict as the first element")

            if not os.path.isfile(self.filepath):
                with open(self.filepath, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()

            with open(self.filepath, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                if isinstance(data, dict):
                    data = [data]

                for post in data:
                    post_copy = post.copy()

                    for key in post_copy:
                        value = post_copy[key]
                        if isinstance(value, (list, tuple, set)):
                            post_copy[key] = '; '.join(str(item) for item in value)
                        else:
                            post_copy[key] = str(value) if value is not None else ''

                    writer.writerow(post_copy)

            print(f"[CSV] Data saved: {self.filepath}")

        except Exception as e:
            print(f"[CSV] Error saving: {e}")

            