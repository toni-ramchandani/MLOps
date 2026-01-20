from __future__ import annotations
import json
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

import mlflow
from .settings import load_settings

app = FastAPI(title="Enterprise OSS MLOps API", version="1.0.0")

REQUESTS = Counter("predict_requests_total", "Total prediction requests")
LATENCY = Histogram("predict_latency_seconds", "Prediction latency in seconds")

class PredictRequest(BaseModel):
    rows: List[Dict[str, Any]]

_lock = threading.Lock()
_model = None
_feature_cols: Optional[List[str]] = None
_model_uri: Optional[str] = None
_load_error: Optional[str] = None

def _load_if_needed():
    global _model, _feature_cols, _model_uri, _load_error
    if _model is not None and _feature_cols is not None:
        return
    with _lock:
        if _model is not None and _feature_cols is not None:
            return
        try:
            s = load_settings("configs/config.yaml")
            mlflow.set_tracking_uri(s.mlflow_tracking_uri)
            mlflow.set_registry_uri(s.mlflow_tracking_uri)
            _model_uri = f"models:/{s.model_name}/Production"
            _model = mlflow.pyfunc.load_model(_model_uri)
            cfg = s.config
            _feature_cols = json.loads(Path(cfg["data"]["feature_names_path"]).read_text(encoding="utf-8"))
            _load_error = None
        except Exception as e:
            _model = None
            _feature_cols = None
            _load_error = repr(e)

@app.get("/health")
def health():
    return {"status": "ready" if (_model is not None) else "not_ready", "model_uri": _model_uri, "load_error": _load_error}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/predict")
def predict(req: PredictRequest):
    REQUESTS.inc()
    with LATENCY.time():
        _load_if_needed()
        if _model is None or _feature_cols is None:
            return {"error": "Model not ready. Run data/train/register first.", "model_uri": _model_uri, "load_error": _load_error}
        df = pd.DataFrame(req.rows)
        missing = [c for c in _feature_cols if c not in df.columns]
        if missing:
            return {"error": f"Missing columns: {missing}", "model_uri": _model_uri}
        X = df[_feature_cols].astype(float)
        proba = np.asarray(_model.predict(X)).reshape(-1)
        preds = (proba >= 0.5).astype(int)
        return {"model_uri": _model_uri, "predictions": [{"pred_proba": float(p), "pred_label": int(y)} for p, y in zip(proba, preds)]}
