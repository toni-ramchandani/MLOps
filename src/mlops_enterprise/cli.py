from __future__ import annotations

import typer

from .data import prepare_data
from .monitoring import build_drift_report
from .registry import register_best_to_production
from .settings import load_settings
from .train import train_and_log

app = typer.Typer(help="Enterprise OSS MLOps CLI (Colab-safe)")


@app.command("data")
def data_cmd():
    print(prepare_data("configs/config.yaml"))


@app.command("train")
def train_cmd():
    print(train_and_log("configs/config.yaml"))


@app.command("register")
def register_cmd():
    print(register_best_to_production("configs/config.yaml"))


@app.command("monitor")
def monitor_cmd():
    s = load_settings("configs/config.yaml")
    cfg = s.config
    print(
        build_drift_report(
            reference_csv=cfg["data"]["reference_path"],
            current_csv=cfg["data"]["test_path"],
            feature_names_json=cfg["data"]["feature_names_path"],
            out_html="reports/drift_report.html",
        )
    )
