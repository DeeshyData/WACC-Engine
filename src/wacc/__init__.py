from .calculators import *
from .models import *
from .financial_data import *

import time

DATA_SOURCES = [
    RiskFreeRates,
    InflationRates,
    CorporateBonds,
    TreasuryBonds,
    CompanyData
]

def download_all():
    for source in DATA_SOURCES:
        print(source.__name__)
        start = time.perf_counter()
        source.download()
        print(f"{time.perf_counter() - start:.3f}s")
