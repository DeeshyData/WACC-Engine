import numpy as np
import pandas as pd

class CostOfEquity:
    """
    Calculates the Cost of Equity of the company

    Attributes:
        rfr_df: A series of risk-free rates with a given maturity
        mrp_array: Array of market risk premiums to average
    """

    def __init__(self, rfr_df: pd.Series, mrp_array: list[float]):
        self.rfr_df = rfr_df
        self.mrp_array = mrp_array

    def _mrp_avg(self) -> float:
        return np.mean(self.mrp_array)

    def get_coe(self, beta: float) -> float:
        return self.rfr_df.iloc[-1] + beta * self._mrp_avg()
