import pandas as pd

from .data_source import DataSource
from .source_config import RBA_G01HIST

class InflationRates(DataSource):
    URL = RBA_G01HIST.URL
    PATH = RBA_G01HIST.PATH
    COLUMNS = ["Inflation"]

    @classmethod
    def _clean_data(cls) -> pd.DataFrame:
        df = super().clean(io=cls.PATH, usecols="A,C", skiprows=10).dropna()
        df.columns = cls.COLUMNS
        df = df.resample("YE").last()
        df.index = df.index.year
        df.index.name = "Year"
        df = df[df.index >= 1958]
        df = df / 100
        return df

    @classmethod
    def load_data(cls) -> pd.Series:
        df = cls._clean_data()
        return df["Inflation"][:-1]
