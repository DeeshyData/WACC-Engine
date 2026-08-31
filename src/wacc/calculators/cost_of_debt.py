import pandas as pd

class CostOfDebt:
    """
    Calculates the Cost of Debt of the company

    Attributes:
        cb_df: A dataframe of the corporate bonds
        tb_mat_df: A dataframe of the maturities for treasury bonds
        tb_yld_df: A dataframe of the yields of treasury bonds
    """

    def __init__(self, cb_df: pd.DataFrame, tb_mat_df: pd.DataFrame, tb_yld_df: pd.DataFrame):
        self.cb_df = cb_df
        self.tb_mat_df = tb_mat_df
        self.tb_yld_df = tb_yld_df
        self.term_10y = pd.Series(len(self.cb_df) * [10], index=self.cb_df.index, name="10Y Term")

    def _interpolate(self, target_data: pd.Series) -> pd.DataFrame:
        """
        Use linear interpolation to find what proportion of treasury bonds are associated with the maturities of corporate bonds

        :param target_data: The effective tenors of corporate bonds
        :return: A dataframe of AGS rates
        """

        results = []

        for date in target_data.index:
            # Select data within date from target data
            target_mat = target_data[date]
            mats = self.tb_mat_df.loc[date]
            ylds = self.tb_yld_df.loc[date]

            # Pair maturities with yields
            pairs = [(m, y) for m, y in zip(mats, ylds) if pd.notna(m) and pd.notna(y)]

            value = None
            for i in range(1, len(pairs)):
                prev_mat, prev_yld = pairs[i - 1]
                curr_mat, curr_yld = pairs[i]

                if curr_mat > target_mat:
                    w = (target_mat - prev_mat) / (curr_mat - prev_mat)
                    value = w * curr_yld + (1 - w) * prev_yld
                    break

            results.append(value)

        return pd.DataFrame({f"AGS {target_data.name}": results}, index=target_data.index)

    def _get_ags_data(self) -> pd.DataFrame:
        df1 = self._interpolate(self.cb_df["7Y Effective Tenor"])
        df2 = self._interpolate(self.cb_df["10Y Effective Tenor"])
        df3 = self._interpolate(self.term_10y)

        return pd.concat([df1, df2, df3], axis=1)

    def _get_spreads(self) -> pd.DataFrame:
        ags_data = self._get_ags_data()

        spread_7y = self.cb_df["7Y Yield"] - ags_data["AGS 7Y Effective Tenor"]
        spread_7y.name = "spread_7y"

        spread_10y = self.cb_df["10Y Yield"] - ags_data["AGS 10Y Effective Tenor"]
        spread_10y.name = "spread_10y"

        return pd.concat([spread_7y, spread_10y], axis=1)

    def get_cod(self) -> float:
        spreads = self._get_spreads()
        drp_10y = ((10 - self.cb_df["10Y Effective Tenor"]) *
                   (spreads["spread_10y"] - spreads["spread_7y"]) /
                   (self.cb_df["10Y Effective Tenor"] - self.cb_df["7Y Effective Tenor"]) +
                   spreads["spread_10y"])

        bond_yield_10y = drp_10y + self._get_ags_data()["AGS 10Y Term"]

        annualised = ((1 + bond_yield_10y / 200)**2 - 1) * 100
        return annualised.mean() / 100
