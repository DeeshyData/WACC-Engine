import pandas as pd
from pandas.tseries.offsets import MonthEnd

from .data_source import DataSource
from .source_config import RBA_F03HIST

class CorporateBonds(DataSource):
    URL = RBA_F03HIST.URL
    PATH = RBA_F03HIST.PATH
    COLUMNS = ["7Y Effective Tenor", "7Y Yield", "10Y Effective Tenor", "10Y Yield"]

    @classmethod
    def _clean_data(cls) -> pd.DataFrame:
        df = super().clean(io=cls.PATH, usecols="A,S:V", skiprows=10)
        df.columns = cls.COLUMNS
        df.index.name = "Date"

        end_date = df.index[-1]
        start_date = (end_date - pd.DateOffset(years=1)) + MonthEnd(1)

        return df.loc[start_date:]

    @classmethod
    def load_data(cls) -> pd.DataFrame:
        return cls._clean_data()
