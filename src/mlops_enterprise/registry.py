from __future__ import annotations

import time

import mlflow
from mlflow.tracking import MlflowClient

from .settings import load_settings


def _wait_ready(client: MlflowClient, name: str, version: str, timeout_s: int = 120) -> None:
    start = time.time()
    while True:
        mv = client.get_model_version(name=name, version=version)
        if mv.status == "READY":
            return
        if time.time() - start > timeout_s:
            raise RuntimeError(f"Model version not READY after {timeout_s}s (status={mv.status})")
        time.sleep(1)


def register_best_to_production(config_path: str = "configs/config.yaml") -> dict:
    s = load_settings(config_path)

    mlflow.set_tracking_uri(s.mlflow_tracking_uri)
    mlflow.set_registry_uri(s.mlflow_tracking_uri)

    exp = mlflow.get_experiment_by_name(s.experiment_name)
    if exp is None:
        raise RuntimeError("Experiment not found. Run train first.")

    runs = mlflow.search_runs(
        [exp.experiment_id], order_by=["metrics.val_roc_auc DESC"], max_results=50
    )
    if runs.empty:
        raise RuntimeError("No runs found. Run train first.")

    best = runs.iloc[0]
    run_id = best["run_id"]
    model_uri = f"runs:/{run_id}/model"

    client = MlflowClient()
    mv = mlflow.register_model(model_uri=model_uri, name=s.model_name)
    _wait_ready(client, s.model_name, mv.version)

    client.transition_model_version_stage(
        name=s.model_name,
        version=mv.version,
        stage="Production",
        archive_existing_versions=True,
    )

    return {
        "model_name": s.model_name,
        "version": mv.version,
        "run_id": run_id,
        "best_val_roc_auc": float(best["metrics.val_roc_auc"]),
    }
