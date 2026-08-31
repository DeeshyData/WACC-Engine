import pandas as pd
from .public_company import PublicCompany

class PrivateCompany:
    """
    Find the equity beta of a private company using comparable company analysis

    Attributes:
        name: The name of the company
        industry: The industry of the company
        de_ratio: The debt-to-equity ratio of the company
        companies: A dataframe of all public companies
    """

    def __init__(self, name: str, industry: str, de_ratio: float, companies: pd.DataFrame):
        self.name = name
        self.industry = industry
        self.de_ratio = de_ratio
        self.companies = companies
        self.pattern = "|".join(industry.split())

    def _get_similar_companies(self) -> pd.DataFrame:
        return self.companies[
            self.companies["Industry"].str.contains(self.pattern, case=False, na=False)
        ].reset_index(drop=True)

    def _get_company_data(self, period: str, interval: str) -> pd.DataFrame:
        similar_companies = self._get_similar_companies()
        symbols = similar_companies["Symbol"].tolist()

        market_returns = PublicCompany.get_market_returns(period, interval)

        rows = []
        for symbol in symbols:
            asset_data = PublicCompany(symbol).get_data(period, interval, market_returns)
            if asset_data:
                rows.append(asset_data)

        return pd.DataFrame(rows).reset_index(drop=True)

    def get_comparables(self, period: str, interval: str) -> pd.DataFrame:
        company_data = self._get_company_data(period, interval)
        comparables = company_data[
            (company_data["Debt to Equity Ratio"] >= 0.2) &
            (company_data["Debt to Equity Ratio"] <= 0.9) &
            (company_data["Equity Beta"] > 0) &
            (company_data["Equity Beta"] < 1.2)
        ].reset_index(drop=True)
        return comparables

    def get_asset_beta(self, comparables: pd.DataFrame) -> float:
        return float(comparables["Asset Beta"].mean())

    def get_equity_beta(self, asset_beta: float, t: float = 0.3) -> float:
        return float(asset_beta * (1 + (1 - t) * self.de_ratio))
