from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

def _psi(ref: np.ndarray, cur: np.ndarray, bins: int = 10) -> float:
    ref = np.asarray(ref, dtype=float)
    cur = np.asarray(cur, dtype=float)
    q = np.linspace(0, 1, bins + 1)
    edges = np.quantile(ref, q)
    edges[0] = -np.inf
    edges[-1] = np.inf
    rc, _ = np.histogram(ref, bins=edges)
    cc, _ = np.histogram(cur, bins=edges)
    rp = rc / max(rc.sum(), 1)
    cp = cc / max(cc.sum(), 1)
    eps = 1e-6
    rp = np.clip(rp, eps, 1)
    cp = np.clip(cp, eps, 1)
    return float(np.sum((cp - rp) * np.log(cp / rp)))

def _ks_stat(ref: np.ndarray, cur: np.ndarray) -> float:
    ref = np.sort(np.asarray(ref, dtype=float))
    cur = np.sort(np.asarray(cur, dtype=float))
    xs = np.sort(np.unique(np.concatenate([ref, cur])))
    cdf_r = np.searchsorted(ref, xs, side="right") / ref.size
    cdf_c = np.searchsorted(cur, xs, side="right") / cur.size
    return float(np.max(np.abs(cdf_r - cdf_c)))

def build_drift_report(reference_csv: str, current_csv: str, feature_names_json: str, out_html: str) -> dict:
    feature_cols = json.loads(Path(feature_names_json).read_text(encoding="utf-8"))
    ref = pd.read_csv(reference_csv)
    cur = pd.read_csv(current_csv)

    rows = []
    for c in feature_cols:
        r = ref[c].astype(float).to_numpy()
        k = cur[c].astype(float).to_numpy()
        rows.append({
            "feature": c,
            "psi": _psi(r, k),
            "ks_stat": _ks_stat(r, k),
            "ref_mean": float(np.mean(r)),
            "cur_mean": float(np.mean(k)),
        })

    df = pd.DataFrame(rows).sort_values(["psi", "ks_stat"], ascending=False)
    Path(out_html).parent.mkdir(parents=True, exist_ok=True)

    html = (
        "<html><head><title>Drift Report</title>"
        "<style>"
        "body{font-family:Arial;padding:16px}"
        "table{border-collapse:collapse;width:100%}"
        "th,td{border:1px solid #ddd;padding:6px;font-size:12px}"
        "th{background:#f3f3f3}"
        "</style></head><body>"
        "<h2>Data Drift Report (PSI + KS)</h2>"
        "<p><b>PSI</b>: ~0.1 small, ~0.2 moderate, &gt;0.3 large. <b>KS</b> higher = more drift.</p>"
        + df.to_html(index=False)
        + "</body></html>"
    )
    Path(out_html).write_text(html, encoding="utf-8")
    return {"report_path": out_html, "rows_ref": int(ref.shape[0]), "rows_cur": int(cur.shape[0])}
