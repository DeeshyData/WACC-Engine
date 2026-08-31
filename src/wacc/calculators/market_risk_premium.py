import pandas as pd

from ..financial_data.source_config import DAMODARAN_PATH

class MarketRiskPremium:
    """
    Calculate market risk premium using different approaches

    Attributes:
        rfr_df: A series of risk-free rates with a given maturity
        ret_df: A series of market returns
        inf_df: A series of inflation rates
    """

    def __init__(self, rfr_df: pd.Series, ret_df: pd.Series, inf_df: pd.Series):
        self.rfr_df = rfr_df
        self.ret_df = ret_df
        self.inf_df = inf_df

    def ibbotson_approach(self) -> float:
        # Set the same date range across risk-free rates and market returns
        if self.rfr_df.index[0] < self.ret_df.index[0]:
            rfr_df = self.rfr_df[self.ret_df.index]
            ret_df = self.ret_df
        else:
            rfr_df = self.rfr_df
            ret_df = self.ret_df[self.rfr_df.index]

        # Return the mean of the differences for each year
        return (ret_df - rfr_df).mean()

    def wright_approach(self, exp_inf_df: float) -> float:
        if self.inf_df.index[0] < self.ret_df.index[0]:
            inf_df = self.inf_df[self.ret_df.index]
            ret_df = self.ret_df
        else:
            inf_df = self.inf_df
            ret_df = self.ret_df[self.inf_df.index]

        real_market_return = (1 + ret_df) / (1 + inf_df) - 1
        average_real_return = real_market_return.mean()

        implied_nominal_market = (1 + average_real_return) * (1 + exp_inf_df) - 1
        return implied_nominal_market - self.rfr_df.iloc[-1]

    def damodaran_approach(self) -> float:
        df = pd.read_excel(DAMODARAN_PATH, sheet_name="ERPs by country", usecols="A,H", engine="calamine", skiprows=7)
        df = df[df["Country"] == "Australia"].set_index("Country")

        return df.iloc[0, 0]
