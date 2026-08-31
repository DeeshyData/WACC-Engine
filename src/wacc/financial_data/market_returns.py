import pandas as pd

from .data_source import DataSource
from .source_config import AER_PATH
from .source_config import SNP_PATH

class MarketReturns(DataSource):
    PATH1 = AER_PATH
    PATH2 = SNP_PATH

    @classmethod
    def _get_aer_data(cls) -> pd.DataFrame:
        df = super().read(io=cls.PATH1, usecols="A:B", skiprows=1, nrows=134)
        df = df[df["Year"] >= 1958]
        df.set_index("Year", inplace=True)
        return df

    @classmethod
    def _get_snp_data(cls) -> pd.DataFrame:
        df = super().read(io=cls.PATH2, skiprows=6).dropna()
        df.columns = ["Year", "Stock accumulation index"]
        df["Year"] = pd.to_datetime(df["Year"])
        df.set_index("Year", inplace=True)

        df = df.resample("ME").mean().resample("YE").last()[:-1]
        df = df.pct_change().dropna()

        df.index = df.index.year

        return df

    @classmethod
    def load_data(cls) -> pd.Series:
        df1 = cls._get_aer_data()
        df2 = cls._get_snp_data()
        return pd.concat([df1, df2])["Stock accumulation index"]
