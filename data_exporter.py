import os
import csv
import sqlite3
from datetime import datetime


curr_dt = datetime.now().strftime('%Y.%m.%d_%H.%M.%S')


class DataExporter:
    """
    Handles exporting data to CSV, SQLite, or both based on the specified mode
    """

    def __init__(self, mode='*', filename=f'data_{curr_dt}', dirname='ProcessedData', tablename=None):
        """
        Initialize export mode and filename, defaulting to CSV and timestamped name
        """
        self.mode = mode.lower()
        self.filename = filename
        self.tablename = tablename
        self.extn = ''

        if not tablename:
            self.tablename = filename

        if self.mode not in ['csv', 'sqlite3', 'sqlite', 'db', '*']:
            self.mode = '*'

        if not dirname:
            dirname = 'ProcessedData'

        self.filepath = os.path.join(dirname, f"{self.filename}")
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

            if self.extn != '.csv':
                self.extn = '.csv'

            filepath = self.filepath + self.extn

            if not os.path.isfile(filepath):
                with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()

            with open(filepath, 'a', newline='', encoding='utf-8') as csvfile:
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

            print(f"[CSV] Data saved: {filepath}")

        except Exception as e:
            print(f"[CSV] Error saving: {e}")

    def _save_to_sqlite(self, data):
        """
        Internal method to save data to a SQLite database file
        """
        conn = None
        try:
            fieldnames = ''
            if isinstance(data, dict):
                fieldnames = list(data.keys())
            elif isinstance(data[0], dict):
                fieldnames = list(data[0].keys())
            else:
                raise ValueError("Data must be a dict or a list/tuple with a dict as the first element")

            if self.extn not in ['.sqlite3', '.sqlite', '.db']:
                self.extn = '.db'

            filepath = self.filepath + self.extn

            conn = sqlite3.connect(filepath)
            cursor = conn.cursor()
            
            # Sanitize tablename
            tablename = ''.join(c if c.isalnum() or c == '_' else '_' for c in self.tablename)
            if not tablename or tablename[0].isdigit():
                tablename = 'data_' + tablename
            
            column_definitions = ', '.join([f'`{field}` TEXT' for field in fieldnames])
            create_table_query = f'CREATE TABLE IF NOT EXISTS `{tablename}` ({column_definitions})'
            cursor.execute(create_table_query)
            
            if isinstance(data, dict):
                data = [data]
            
            for record in data:
                record_copy = record.copy()
                
                for key in record_copy:
                    value = record_copy[key]
                    if isinstance(value, (list, tuple, set)):
                        record_copy[key] = '; '.join(str(item) for item in value)
                    else:
                        record_copy[key] = str(value) if value is not None else ''
                
                column_names = ', '.join([f'`{field}`' for field in fieldnames])
                placeholders = ', '.join(['?' for _ in fieldnames])
                insert_query = f'INSERT INTO `{tablename}` ({column_names}) VALUES ({placeholders})'
                
                values = [record_copy.get(field, '') for field in fieldnames]
                cursor.execute(insert_query, values)
            
            conn.commit()
            print(f"[SQLite] Data saved: {filepath} (table: {tablename})")
            
        except Exception as e:
            print(f"[SQLite] Error saving: {e}")
        finally:
            if conn:
                conn.close()

    def save(self, data, mode=None):
        """
        Save the given data in the selected format(s)
        """
        if mode not in ['csv', 'sqlite3', 'sqlite', 'db', '*']:
            self.mode = '*'

        if self.mode in ['csv', '*']:
            self.extn = '.csv'
            self._save_to_csv(data)

        if self.mode in ['sqlite3', 'sqlite', 'db', '*']:
            self.extn = '.db'
            self._save_to_sqlite(data)