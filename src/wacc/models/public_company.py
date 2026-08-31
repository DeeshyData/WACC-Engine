import yfinance as yf
import pandas as pd

class PublicCompany:
    """
    Get data for a public company

    Attributes:
        company: The name of the company
        symbol: The ticker of the company
        stock: A Ticker object
        period: The given period of time to extract data from
        interval: The increments between data points
    """

    AUS_EXCHANGES = ["ASX", "CXA"]

    def __init__(self, company: str):
        self.company = company
        self.symbol = None
        self.stock = None
        self.period = None
        self.interval = None

    def _get_quote(self) -> dict | None:
        quotes = yf.Search(self.company).quotes
        equities = [q for q in quotes if q.get("quoteType") == "EQUITY"]
        pool = equities or quotes

        aus_matches = [q for q in pool if q.get("exchange") in self.AUS_EXCHANGES]
        if aus_matches:
            aus_matches.sort(key=lambda q: self.AUS_EXCHANGES.index(q["exchange"]))
            return aus_matches[0]

        return pool[0] if pool else None

    def _get_gearing(self) -> float | None:
        try:
            bs = self.stock.balance_sheet
            total_debt = bs.loc["Total Debt"].iloc[0]
            equity = bs.loc["Stockholders Equity"].iloc[0]
        except (KeyError, IndexError):
            return None

        if equity == 0:
            return None

        return float(total_debt / (total_debt + equity))

    def _get_de_ratio(self) -> float | None:
        return self._get_gearing() / (1 - self._get_gearing())

    @staticmethod
    def get_market_returns(period: str, interval: str):
        market = yf.Ticker("^AORD")
        market_history = market.history(period=period, interval=interval)["Close"]
        return market_history.pct_change().dropna()

    def _get_equity_beta(self, market_returns: pd.Series | None = None) -> float | None:
        if market_returns is None:
            market_returns = self.get_market_returns(self.period, self.interval)

        stock = yf.Ticker(self.symbol)
        stock_history = stock.history(period=self.period, interval=self.interval)["Close"]
        stock_returns = stock_history.pct_change().dropna()

        cov = stock_returns.cov(market_returns)
        var = market_returns.var()
        if var == 0 or pd.isna(cov):
            return None

        beta = float(cov / var)
        return beta

    def _get_asset_beta(self, t=0.3):
        return self._get_equity_beta() / (1 + (1 - t) * self._get_de_ratio())

    def get_data(self, period: str, interval: str, market_returns: pd.Series | None = None) -> dict:
        self.period = period
        self.interval = interval

        quote = self._get_quote()
        if quote is None:
            return {}

        self.symbol = quote.get("symbol")
        self.stock = yf.Ticker(self.symbol)

        if quote.get("exchange") not in self.AUS_EXCHANGES:
            print("The given company is not Australian-based")
            return {}

        gearing = self._get_gearing()
        if gearing is None:
            return {}

        equity_beta = self._get_equity_beta(market_returns)
        if equity_beta is None:
            return {}

        return {
            "Symbol": self.symbol,
            "Industry": quote.get("industry"),
            "Equity Beta": equity_beta,
            "Asset Beta": self._get_asset_beta(),
            "Gearing Ratio": gearing,
            "Debt to Equity Ratio": self._get_de_ratio(),
        }
