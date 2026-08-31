import pandas as pd

from .data_source import DataSource
from .source_config import ASX_COMPANIES

class CompanyData(DataSource):
    HEADERS = {"User-Agent": "Mozilla/5.0"}
    URL = ASX_COMPANIES.URL
    PATH = ASX_COMPANIES.PATH

    @classmethod
    def _clean_data(cls) -> pd.DataFrame:
        df = pd.read_csv(cls.PATH)
        df = df.drop(columns=["Listing date", "Market Cap"])
        df.columns = ["Symbol", "Company Name", "Industry"]
        df["Symbol"] = df["Symbol"] + ".AX"
        return df

    @classmethod
    def get_data(cls) -> pd.DataFrame:
        return cls._clean_data()
