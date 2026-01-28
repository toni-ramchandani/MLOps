from __future__ import annotations
import numpy as np
import pandas as pd


class DataValidationError(ValueError):
    pass


def validate_df(df: pd.DataFrame, feature_cols: list[str]) -> pd.DataFrame:
    df = df.copy()
    required = set(feature_cols + ["label"])

    missing = sorted(list(required - set(df.columns)))
    if missing:
        raise DataValidationError(f"Missing columns: {missing}")

    if df[list(required)].isna().any().any():
        raise DataValidationError("Null values found in required columns.")

    for c in feature_cols:
        s = pd.to_numeric(df[c], errors="coerce")
        if s.isna().any():
            raise DataValidationError(f"Non-numeric values in feature '{c}'.")
        if not np.isfinite(s.to_numpy()).all():
            raise DataValidationError(f"Non-finite values in feature '{c}'.")
        df[c] = s.astype(float)

    y = pd.to_numeric(df["label"], errors="coerce")
    if y.isna().any():
        raise DataValidationError("Non-numeric values in label.")
    y = y.astype(int)
    if not set(y.unique()).issubset({0, 1}):
        raise DataValidationError(f"Label must be in {{0,1}}, got {sorted(y.unique().tolist())}.")
    df["label"] = y
    return df
