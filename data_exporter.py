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
            self.mode = 'txt'

