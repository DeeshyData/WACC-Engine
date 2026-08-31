from abc import ABC
from pathlib import Path

import requests
import pandas as pd

class DataSource(ABC):
    URL: str = None
    PATH: Path = None

    @classmethod
    def download(cls):
        response = requests.get(cls.URL)
        response.raise_for_status()
        cls.PATH.write_bytes(response.content)

    @classmethod
    def read(cls, engine: str = "calamine", **kwargs) -> pd.DataFrame:
        return pd.read_excel(**kwargs, engine=engine)

    @classmethod
    def clean(cls, userows: slice = slice(None), engine: str = "calamine", **kwargs) -> pd.DataFrame:
        df = cls.read(engine, **kwargs)
        df = df.iloc[userows]
        df.set_index(df.columns[0], inplace=True)
        df.index = pd.to_datetime(df.index)
        return df

