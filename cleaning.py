import pandas as pd
from pathlib import Path
from config import EXCEL_PATH, RAW_COLUMNS, COLUMN_MAP

TIME_COLS = ["Hours", "Min", "Sec"]

def load_excel(path: Path = EXCEL_PATH) -> pd.DataFrame:
    df = pd.read_excel(path)
    return df

def drop_irrelevant_time(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop(columns=TIME_COLS, errors="ignore")

def ensure_expected_columns(df: pd.DataFrame) -> None:
    missing = [c for c in RAW_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing expected columns: {missing}. Found: {list(df.columns)}")

def coerce_numeric_and_filter(df: pd.DataFrame) -> pd.DataFrame:
    # Keep only expected sensor columns
    sub = df[RAW_COLUMNS].apply(lambda s: pd.to_numeric(s, errors="coerce"))
    # Drop rows with any NaN in the 9 key columns
    sub = sub.dropna(axis=0, how="any")
    # Drop rows where all 9 are zero
    all_zero_mask = (sub == 0).all(axis=1)
    sub = sub[~all_zero_mask].copy()
    # Rename to internal names
    sub = sub.rename(columns=COLUMN_MAP)
    return sub

def clean_data(path: Path = EXCEL_PATH) -> pd.DataFrame:
    df = load_excel(path)
    df = drop_irrelevant_time(df)
    ensure_expected_columns(df)
    clean = coerce_numeric_and_filter(df)
    if len(clean) < 10:
        raise ValueError(f"Not enough valid rows after cleaning: {len(clean)}")
    return clean