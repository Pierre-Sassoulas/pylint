"""docstring"""
import pandas as pd

class TraceLoad:
    """docstring"""
    csvdata = None

    def __init__(self, filename):
        """docstring"""
        cls = self.__class__
        cls.csvdata = pd.read_csv(filename, comment='#', sep=',')
        cls.csvdata['Date_Time'] = \
            pd.to_datetime(cls.csvdata['Date'] + ' ' + cls.csvdata['Time'])
