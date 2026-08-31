from dataclasses import dataclass
from pathlib import Path

# Filenames
F02HIST = "f02hist.xlsx"
F03HIST = "f03hist.xlsx"
F16 = "f16.xlsx"
G01HIST = "g01hist.xlsx"

RBA_URL = "https://www.rba.gov.au/statistics/tables/xls"

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

@dataclass(frozen=True)
class Source:
    URL: str
    PATH: Path

def rba_source(filename: str) -> Source:
    return Source(
        URL=f"{RBA_URL}/{filename}",
        PATH=RAW_DATA_DIR / filename
    )

RBA_F02HIST = rba_source(F02HIST)
RBA_F02HISTHIST = PROCESSED_DATA_DIR / "f02histhist.xls"
RBA_F03HIST = rba_source(F03HIST)
RBA_F16 = rba_source(F16)
RBA_G01HIST = rba_source(G01HIST)

ASX_COMPANIES = Source(
    URL="https://asx.api.markitdigital.com/asx-research/1.0/companies/directory/file",
    PATH=RAW_DATA_DIR / "ASX_Listed_Companies_04-08-2026_02-44-39_AEST"
)

AER_PATH = PROCESSED_DATA_DIR / "AER.xlsx"
SNP_PATH = PROCESSED_DATA_DIR / "PerformanceGraphExport.xls"
DAMODARAN_PATH = PROCESSED_DATA_DIR / "ctrypremJuly26.xlsx"
