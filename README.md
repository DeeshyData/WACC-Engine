# WACC Engine
A Python toolkit for estimating the Weighted Average Cost of Capital (WACC) for Australian companies, built on standard corporate finance theory (CAPM, comparable company analysis).

## Overview
WACC Engine estimates the cost of capital for Australian companies and handles two cases:
- Listed companies - cost of equity via CAPM using observed equity beta (e.g. JB Hi-Fi)
- Private companies - cost of equity via comparable company analysis, unlevering and relevering beta from a set of listed comparables (e.g. Alinta Energy)

The package computes, end to end:
- Cost of equity (CAPM)
- Cost of debt
- Market risk premium (MRP)
- Equity and asset (unlevered) beta
- WACC

## Architecture
```text
wacc_engine/
├── README.md
├── requirements.txt
├── main.ipynb
├── src/
│   └── wacc/
│       ├── calculators/
│       │   ├── calculate_wacc.py
│       │   ├── cost_of_debt.py
│       │   ├── cost_of_equity.py
│       │   └── market_risk_premium.py
│       ├── models/
│       │   ├── asset_data.py
│       │   └── private_company.py
│       └── financial_data/
│           ├── company_data.py
│           ├── corporate_bonds.py
│           ├── data_source.py
│           ├── inflation_rates.py
│           ├── market_returns.py
│           ├── risk_free_rates.py
│           ├── source_config.py
│           └── treasury_bonds.py
└── data/
    ├── raw/
    └── processed/
```

## Installation
```bash
git clone <repo-url>
cd wacc_engine
pip install -r requirements.txt
```

## Dependencies
- `yfinance` - market and pricing data
- `pandas` - data manipulation
- `requests` - fetching external data
- `numpy` - array calculations

## Quick Usage
```python
from wacc import *

# Download required data
download_all()

# Load financial data
rfr = RiskFreeRates.load_data()
inf = InflationRates.load_data()
ret = MarketReturns.load_data()
tb_mat, tb_yld = TreasuryBonds.load_data(start_date=cb.index[0], end_date=cb.index[-1])

# Calculate market risk premium
mrp = MarketRiskPremium(rfr, ret, inf)
mrp_i = mrp.ibbotson_approach()

# Instantiate cost of equity and cost of debt
coe = CostOfEquity(rfr, [mrp_i])
cod = CostOfDebt(cb, tb_mat, tb_yld)

# Pick an asset
asset = "JB Hi-Fi"
period = "10Y"
interval = "1wk"

jb_asset = AssetData(asset)
jb_data = jb_asset.get_data(period, interval)

# Calculate cost of equity and cost of debt
coe_jb = coe.get_coe(jb_data["Beta"])
cod_jb = cod.get_cod()

# Calculate WACC
wacc_jb = CalculateWACC(coe_jb, cod_jb, jb_data["Gearing"])
wacc_jb_pre_tax = wacc_jb.pre_tax()
```

## References
- [AER - Historical Excess Returns - December 2022](https://www.aer.gov.au/documents/aer-historical-excess-returns-december-2022)
- [Damodaran - Data - Current](https://pages.stern.nyu.edu/~adamodar/)
- [QCA - Rate of Return Review](https://www.qca.org.au/project/rate-of-return-matters/rate-of-return-review-2021/)
- [RBA - Historical Data](https://www.rba.gov.au/statistics/historical-data.html)
- [RBA - Statistical Tables](https://www.rba.gov.au/statistics/tables/)
- [S&P Global - All Ordinaries - Total Return Index](https://www.spglobal.com/spdji/en/indices/equity/all-ordinaries/?currency=AUD&returntype=T-#overview)
