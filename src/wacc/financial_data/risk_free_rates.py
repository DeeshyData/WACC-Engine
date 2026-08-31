import pandas as pd
from pathlib import Path

from .data_source import DataSource
from .source_config import RBA_F02HIST, RBA_F02HISTHIST

class RiskFreeRates(DataSource):
    URL = RBA_F02HIST.URL
    PATH = RBA_F02HIST.PATH
    PATH_HIST = RBA_F02HISTHIST
    COLUMNS = ["2Y", "3Y", "5Y", "10Y"]

    @classmethod
    def _clean_data(cls, path: Path, engine: str, skiprows: int) -> pd.DataFrame:
        df = super().clean(io=path, engine=engine, usecols="A:E", skiprows=skiprows)
        df.columns = cls.COLUMNS
        df = df.resample("YE").last()
        df.index = df.index.year
        df.index.name = "Year"
        return df

    @classmethod
    def load_data(cls, maturity: str = "10Y") -> pd.Series:
        df1 = cls._clean_data(cls.PATH_HIST, "xlrd", 10)
        df2 = cls._clean_data(cls.PATH, "calamine", 11)

        df = pd.concat([df1, df2])
        df = df[~df.index.duplicated(keep="first")]

        data = (1 + df[maturity] / 200)**2 - 1

        return data[:-1]
