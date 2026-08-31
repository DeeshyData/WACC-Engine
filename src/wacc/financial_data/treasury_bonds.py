import pandas as pd
from datetime import date

from .data_source import DataSource
from .source_config import RBA_F16

class TreasuryBonds(DataSource):
    URL = RBA_F16.URL
    PATH = RBA_F16.PATH

    _clean_df = None
    _bond_df = None
    _long_term_bonds = None

    @classmethod
    def _clean_data(cls, start_date: pd.Timestamp, end_date: pd.Timestamp) -> pd.DataFrame:
        df = super().clean(userows=slice(8, None), io=cls.PATH, usecols="A:AZ", skiprows=2)
        df.index.name = "Date"
        df = df.resample("ME").last()[:-1]

        return df.loc[start_date:end_date]

    @classmethod
    def _bond_data(cls) -> pd.DataFrame:
        import re

        df = cls._clean_df

        bond_df = []

        for col in df.columns:
            maturity = pd.to_datetime(
                    re.search(r"\d{1,2}-[A-Za-z]{3}-\d{4}", col).group(),
                    format="%d-%b-%Y"
                )

            first_date = df[col].first_valid_index()
            first_year = first_date.year if first_date is not None else None

            bond_df.append({
                "bond": col,
                "coupon": re.search(r"\d+\.\d+%", col).group(),
                "maturity": maturity,
                "term": maturity.year - first_year if first_year else None
            })

        return pd.DataFrame(bond_df)

    @classmethod
    def _get_long_term_bonds(cls) -> list[str]:
        bond_df = cls._bond_df

        return bond_df.loc[
            bond_df["term"] >= 7,
            "bond"
        ].tolist()

    @classmethod
    def _yearfrac(cls, start_date: date, end_date: date) -> float:
        import calendar

        start, end = start_date, end_date

        y1, m1, d1 = start.year, start.month, start.day
        y2, m2, d2 = end.year, end.month, end.day

        if y1 == y2:
            # Same calendar year — denominator is that year's day count
            days_in_year = 366 if calendar.isleap(y1) else 365
            result = (end - start).days / days_in_year

        elif y2 == y1 + 1 and (m1, d1) > (m2, d2):
            # Crosses exactly one year boundary but spans < 12 months
            # e.g. 2023-06-15 -> 2024-03-10
            days_y1 = 366 if calendar.isleap(y1) else 365
            days_y2 = 366 if calendar.isleap(y2) else 365
            avg_days = (days_y1 + days_y2) / 2
            result = (end - start).days / avg_days

        else:
            # Spans one full year or more
            year_count = y2 - y1 + 1
            total_days = (date(y2 + 1, 1, 1) - date(y1, 1, 1)).days
            avg_days = total_days / year_count
            result = (end - start).days / avg_days

        return result

    @classmethod
    def _mat_data(cls) -> pd.DataFrame:
        clean_df = cls._clean_df
        bond_df = cls._bond_df

        df = pd.DataFrame(
            index=clean_df.index,
            columns=clean_df.columns
        )

        for bond in bond_df.itertuples(index=False):
            col = bond.bond
            mat_date = bond.maturity

            df[col] = [
                cls._yearfrac(date, mat_date)
                if not pd.isna(clean_df.loc[date, col])
                else None
                for date in df.index
            ]

        return df[cls._long_term_bonds]

    @classmethod
    def _yld_data(cls) -> pd.DataFrame:
        df = cls._clean_df
        return df[cls._long_term_bonds]

    @classmethod
    def load_data(cls, start_date: pd.Timestamp, end_date: pd.Timestamp) -> tuple[pd.DataFrame, pd.DataFrame]:
        cls._clean_df = cls._clean_data(start_date, end_date)
        cls._bond_df = cls._bond_data()
        cls._long_term_bonds = cls._get_long_term_bonds()

        return cls._mat_data(), cls._yld_data()
