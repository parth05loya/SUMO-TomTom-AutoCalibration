from __future__ import annotations
from pathlib import Path
import pandas as pd
REQUIRED_COLUMNS={"origin_lon","origin_lat","destination_lon","destination_lat"}

def validate_od(df: pd.DataFrame)->None:
    missing=REQUIRED_COLUMNS-set(df.columns)
    if missing: raise ValueError(f"Missing OD columns: {sorted(missing)}")
    if df.empty: raise ValueError("OD table is empty.")
    for col in REQUIRED_COLUMNS:
        if not pd.api.types.is_numeric_dtype(df[col]): raise TypeError(f"OD column must be numeric: {col}")

def load_od_csv(path: str|Path)->pd.DataFrame:
    df=pd.read_csv(path)
    if "od_id" not in df.columns: df.insert(0,"od_id",range(1,len(df)+1))
    validate_od(df)
    return df
