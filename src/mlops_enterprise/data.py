from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

from .settings import load_settings
from .utils import sha256_file


def prepare_data(config_path: str = "configs/config.yaml") -> dict:
    s = load_settings(config_path)
    cfg = s.config

    raw_path = Path(cfg["data"]["raw_path"])
    train_path = Path(cfg["data"]["train_path"])
    val_path = Path(cfg["data"]["val_path"])
    test_path = Path(cfg["data"]["test_path"])
    ref_path = Path(cfg["data"]["reference_path"])
    feat_path = Path(cfg["data"]["feature_names_path"])
    meta_path = Path(cfg["data"]["data_meta_path"])

    raw_path.parent.mkdir(parents=True, exist_ok=True)
    train_path.parent.mkdir(parents=True, exist_ok=True)

    ds = load_breast_cancer(as_frame=True)
    df = ds.frame.copy().rename(columns={"target": "label"})
    df.to_csv(raw_path, index=False)

    train_val, test = train_test_split(
        df, test_size=0.2, random_state=s.random_state, stratify=df["label"]
    )
    train, val = train_test_split(
        train_val, test_size=0.25, random_state=s.random_state, stratify=train_val["label"]
    )

    train.to_csv(train_path, index=False)
    val.to_csv(val_path, index=False)
    test.to_csv(test_path, index=False)
    train.to_csv(ref_path, index=False)

    feature_cols = [c for c in df.columns if c != "label"]
    feat_path.write_text(json.dumps(feature_cols, indent=2), encoding="utf-8")

    meta = {
        "raw_path": str(raw_path),
        "data_hash_sha256": sha256_file(str(raw_path)),
        "rows_raw": int(df.shape[0]),
        "n_features": int(len(feature_cols)),
        "split": {
            "train": int(train.shape[0]),
            "val": int(val.shape[0]),
            "test": int(test.shape[0]),
        },
    }
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return meta
