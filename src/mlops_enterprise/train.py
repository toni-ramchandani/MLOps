from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, accuracy_score, f1_score

from .settings import load_settings
from .validation import validate_df


def _ensure_experiment(name: str, artifact_root: str) -> None:
    exp = mlflow.get_experiment_by_name(name)
    if exp is None:
        mlflow.create_experiment(name=name, artifact_location=artifact_root)


def train_and_log(config_path: str = "configs/config.yaml") -> dict:
    s = load_settings(config_path)
    cfg = s.config

    mlflow.set_tracking_uri(s.mlflow_tracking_uri)
    mlflow.set_registry_uri(s.mlflow_tracking_uri)

    _ensure_experiment(s.experiment_name, s.artifact_root)
    mlflow.set_experiment(s.experiment_name)

    feature_cols = json.loads(Path(cfg["data"]["feature_names_path"]).read_text(encoding="utf-8"))
    train_df = pd.read_csv(cfg["data"]["train_path"])
    val_df = pd.read_csv(cfg["data"]["val_path"])

    train_df = validate_df(train_df, feature_cols)
    val_df = validate_df(val_df, feature_cols)

    X_train, y_train = train_df[feature_cols], train_df["label"]
    X_val, y_val = val_df[feature_cols], val_df["label"]

    params = cfg["training"]["params"]
    pipe = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(**params, random_state=s.random_state)),
        ]
    )

    with mlflow.start_run(run_name="logreg_production_style") as run:
        pipe.fit(X_train, y_train)

        proba = pipe.predict_proba(X_val)[:, 1]
        pred = (proba >= 0.5).astype(int)

        metrics = {
            "val_roc_auc": float(roc_auc_score(y_val, proba)),
            "val_accuracy": float(accuracy_score(y_val, pred)),
            "val_f1": float(f1_score(y_val, pred)),
        }

        gate = float(cfg["quality_gates"]["min_val_roc_auc"])
        if metrics["val_roc_auc"] < gate:
            raise RuntimeError(
                f"QUALITY GATE FAILED: val_roc_auc={metrics['val_roc_auc']:.4f} < {gate:.4f}"
            )

        mlflow.log_params(params)
        mlflow.log_param("random_state", s.random_state)
        mlflow.log_metrics(metrics)

        mlflow.log_dict(
            json.loads(Path(cfg["data"]["data_meta_path"]).read_text(encoding="utf-8")),
            "data_meta.json",
        )
        mlflow.log_dict({"feature_cols": feature_cols}, "feature_names.json")

        signature = infer_signature(X_train, np.asarray(pipe.predict_proba(X_train)[:, 1]))
        mlflow.sklearn.log_model(
            pipe, artifact_path="model", signature=signature, input_example=X_train.iloc[:5]
        )

        return {"run_id": run.info.run_id, **metrics}
