from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict

import yaml


@dataclass(frozen=True)
class Settings:
    config: Dict[str, Any]

    @property
    def random_state(self) -> int:
        return int(self.config["project"]["random_state"])

    @property
    def mlflow_tracking_uri(self) -> str:
        return os.getenv("MLFLOW_TRACKING_URI", self.config["mlflow"]["tracking_uri"])

    @property
    def experiment_name(self) -> str:
        return self.config["mlflow"]["experiment_name"]

    @property
    def model_name(self) -> str:
        return self.config["mlflow"]["registered_model_name"]

    @property
    def artifact_root(self) -> str:
        return self.config["mlflow"]["artifact_root"]


def load_settings(path: str = "configs/config.yaml") -> Settings:
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return Settings(cfg)
