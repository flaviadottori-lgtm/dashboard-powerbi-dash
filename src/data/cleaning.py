"""
cleaning.py
Simple cleaning utilities used before visualization.
"""
import pandas as pd

def ensure_date(df, col_candidates=["date","created_at","created","data","created_at_date"]):
    for c in col_candidates:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce", dayfirst=True)
            return c
    # try to find any datetime-like column
    for c in df.columns:
        if "date" in c.lower() or "created" in c.lower():
            df[c] = pd.to_datetime(df[c], errors="coerce", dayfirst=True)
            return c
    return None

def tidy_columns(df):
    df = df.copy()
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df
