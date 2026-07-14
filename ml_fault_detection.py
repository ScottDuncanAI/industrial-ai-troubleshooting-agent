"""
ML Fault Detection — Isolation Forest anomaly detection + XGBoost feature importance.

Two-component pipeline:
  1. Isolation Forest (semi-supervised): trains on NOC data (TE_8332A in [530,545]°C),
     scores the full dataset — anomaly score > 0 flags fault periods.
  2. XGBoost (supervised): trains to predict TE_8332A out-of-range from the remaining
     29 tags, yielding gain-based feature importances — ranked early-warning indicators.

Complements MSPC (PCA-based linear detection) with non-linear multivariate detection
and interpretable fault predictor ranking.

Usage:
  python ml_fault_detection.py [--downsample-minutes 1] [--contamination 0.086] ...

Outputs JSON summary to stdout. Saves plots to plots/MLFault/ directory.
"""

import os
import sys
import json
import argparse
from datetime import datetime

import numpy as np
import pandas as pd
import duckdb
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, "boiler_historian.duckdb")
RUN_TIMESTAMP = datetime.now()
RUN_DATE = RUN_TIMESTAMP.strftime("%Y%m%d")
RUN_TIME = RUN_TIMESTAMP.strftime("%H%M%S")
PLOTS_DIR = os.path.join(
    PROJECT_DIR, "plots", "MLFault", f"MLFault_{RUN_DATE}_{RUN_TIME}"
)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args():
    p = argparse.ArgumentParser(description="ML fault detection on boiler historian data")
    p.add_argument("--downsample-minutes", type=int, default=1)
    p.add_argument("--noc-tag", default="TE_8332A")
    p.add_argument("--noc-min", type=float, default=530.0)
    p.add_argument("--noc-max", type=float, default=545.0)
    p.add_argument("--contamination", type=float, default=0.086,
                   help="Expected anomaly fraction for Isolation Forest threshold")
    p.add_argument("--n-estimators", type=int, default=200,
                   help="Number of trees in Isolation Forest")
    p.add_argument("--top-n-events", type=int, default=5,
                   help="Number of worst fault periods to surface in JSON output")
    p.add_argument("--start-time", type=str, default=None,
                   help="Start timestamp filter (YYYY-MM-DD HH:MM:SS)")
    p.add_argument("--end-time", type=str, default=None,
                   help="End timestamp filter (YYYY-MM-DD HH:MM:SS)")
    p.add_argument("--no-xgb", action="store_true",
                   help="Skip XGBoost feature importance step")
    return p.parse_args()


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_data(downsample_minutes=1, start_time=None, end_time=None):
    con = duckdb.connect(DB_PATH, read_only=True)

    tag_rows = con.execute("SELECT tag_name FROM tags ORDER BY tag_name").fetchall()
    all_tags = [r[0] for r in tag_rows]

    meta_rows = con.execute("SELECT tag_name, description, units FROM tags").fetchall()
    tag_meta = {r[0]: {"description": r[1], "units": r[2]} for r in meta_rows}

    tag_select = ", ".join([f'AVG("{t}") AS "{t}"' for t in all_tags])
    where_clauses = []
    if start_time:
        where_clauses.append(f"timestamp >= '{start_time}'")
    if end_time:
        where_clauses.append(f"timestamp <= '{end_time}'")
    where_sql = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""

    query = f"""
        SELECT
            TIME_BUCKET(INTERVAL '{downsample_minutes} minutes', timestamp) AS timestamp,
            {tag_select}
        FROM historian_data
        {where_sql}
        GROUP BY 1
        ORDER BY 1
    """
    df = con.execute(query).fetchdf()
    con.close()

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp")
    df = df.dropna()

    return df, all_tags, tag_meta


# ---------------------------------------------------------------------------
# Isolation Forest
# ---------------------------------------------------------------------------

def fit_isolation_forest(df_noc, n_estimators=200, contamination=0.086, random_state=42):
    scaler = StandardScaler()
    X_noc = scaler.fit_transform(df_noc.values)
    iforest = IsolationForest(
        n_estimators=n_estimators,
        contamination=contamination,
        random_state=random_state,
        n_jobs=-1,
    )
    iforest.fit(X_noc)
    return scaler, iforest


def score_all(df, scaler, iforest):
    """Return anomaly scores (positive = anomalous) and binary predictions (-1/1)."""
    X = scaler.transform(df.values)
    # decision_function: values < 0 are anomalies. Negate so positive = anomalous.
    scores = -iforest.decision_function(X)
    predictions = iforest.predict(X)  # -1 = anomaly, 1 = normal
    return scores, predictions


# ---------------------------------------------------------------------------
# Fault period detection
# ---------------------------------------------------------------------------

def find_fault_periods(timestamps, scores, predictions):
    anomalous = predictions == -1
    periods = []
    in_period = False
    start_idx = 0

    for i in range(len(anomalous)):
        if anomalous[i] and not in_period:
            start_idx = i
            in_period = True
        elif not anomalous[i] and in_period:
            in_period = False
            _append_period(periods, timestamps, scores, start_idx, i - 1)

    if in_period:
        _append_period(periods, timestamps, scores, start_idx, len(anomalous) - 1)

    return periods


def _append_period(periods, timestamps, scores, s, e):
    score_slice = scores[s : e + 1]
    peak_idx = s + int(np.argmax(score_slice))
    periods.append({
        "start": str(timestamps[s]),
        "end": str(timestamps[e]),
        "duration_min": round(
            (timestamps[e] - timestamps[s]).total_seconds() / 60, 1
        ),
        "mean_score": round(float(np.mean(score_slice)), 4),
        "max_score": round(float(np.max(score_slice)), 4),
        "peak_idx": peak_idx,
    })


# ---------------------------------------------------------------------------
# XGBoost feature importance
# ---------------------------------------------------------------------------

def fit_xgb_importance(df, noc_tag, noc_min, noc_max, no_xgb=False):
    """
    Train classifier to predict noc_tag out-of-range from the other 29 tags.
    Returns (ranked_features, model_name). Falls back to GradientBoostingClassifier
    if xgboost is not installed.
    """
    if no_xgb:
        return [], "skipped"

    feature_tags = [t for t in df.columns if t != noc_tag]
    X = df[feature_tags].values
    y = ((df[noc_tag] < noc_min) | (df[noc_tag] > noc_max)).astype(int).values

    if y.sum() == 0 or y.sum() == len(y):
        print("WARNING: XGBoost skipped — all labels are the same class.", file=sys.stderr)
        return [], "skipped"

    # Try XGBoost first, falling back to GradientBoostingClassifier on ANY failure.
    # The fallback must wrap both construction AND fit: on macOS, xgboost imports and
    # constructs fine but raises XGBoostError at fit() time when libomp is missing —
    # that is not an ImportError, so catching only ImportError would let it crash.
    try:
        from xgboost import XGBClassifier
        clf = XGBClassifier(
            n_estimators=200,
            max_depth=4,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            importance_type="gain",
            eval_metric="logloss",
            random_state=42,
            n_jobs=-1,
        )
        clf.fit(X, y)
        model_name = "XGBoostClassifier"
    except Exception as exc:
        print(f"xgboost unavailable ({type(exc).__name__}: {exc}); "
              "falling back to GradientBoostingClassifier.", file=sys.stderr)
        from sklearn.ensemble import GradientBoostingClassifier
        clf = GradientBoostingClassifier(
            n_estimators=200,
            max_depth=4,
            learning_rate=0.05,
            subsample=0.8,
            random_state=42,
        )
        clf.fit(X, y)
        model_name = "GradientBoostingClassifier"

    importances = clf.feature_importances_

    total = importances.sum()
    if total > 0:
        importances = importances / total

    ranked = sorted(zip(feature_tags, importances), key=lambda x: x[1], reverse=True)
    return [
        {"tag": tag, "importance": round(float(imp), 5)} for tag, imp in ranked
    ], model_name


# ---------------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------------

def _ensure_plots_dir():
    os.makedirs(PLOTS_DIR, exist_ok=True)


def plot_monitoring(timestamps, te_values, scores, predictions,
                    noc_min, noc_max, noc_tag):
    _ensure_plots_dir()

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)
    ts_arr = np.array(timestamps)
    anomalous = predictions == -1

    # --- Panel 1: NOC tag ---
    ax1.plot(timestamps, te_values, linewidth=0.6, color="#1f77b4")
    ax1.axhspan(noc_min, noc_max, alpha=0.15, color="green",
                label=f"Normal ({noc_min}–{noc_max}°C)")
    ax1.set_ylabel(f"{noc_tag} (°C)")
    ax1.set_title("Boiler Outlet Steam Temperature", fontsize=9, loc="left")
    ax1.legend(fontsize=8, loc="upper right")
    ax1.grid(True, alpha=0.3)

    # --- Panel 2: Anomaly score (0 = anomaly boundary, positive = anomalous) ---
    ax2.plot(timestamps, scores, linewidth=0.6, color="#1f77b4", label="Anomaly score")
    ax2.axhline(y=0, color="#d62728", linestyle="--", linewidth=1,
                label="Anomaly threshold (score = 0)")
    mask_anom = scores > 0
    if np.any(mask_anom):
        ax2.scatter(ts_arr[mask_anom], scores[mask_anom],
                    s=3, c="#d62728", zorder=5, alpha=0.5)
    ax2.set_ylabel("Anomaly Score  (positive = fault)")
    ax2.set_title("Isolation Forest Anomaly Score", fontsize=9, loc="left")
    ax2.legend(fontsize=8, loc="upper right")
    ax2.grid(True, alpha=0.3)

    # --- Shade fault regions ---
    diff = np.diff(anomalous.astype(int))
    starts = np.where(diff == 1)[0] + 1
    ends = np.where(diff == -1)[0] + 1
    if anomalous[0]:
        starts = np.insert(starts, 0, 0)
    if anomalous[-1]:
        ends = np.append(ends, len(anomalous))

    for s, e in zip(starts, ends):
        e_clamp = min(e, len(timestamps) - 1)
        for ax in (ax1, ax2):
            ax.axvspan(timestamps[s], timestamps[e_clamp], alpha=0.08, color="red")

    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M"))
    fig.autofmt_xdate(rotation=30)
    fig.suptitle(
        "ML Fault Detection — Isolation Forest Monitoring (5-Day Dataset)",
        fontsize=11, fontweight="bold",
    )
    plt.tight_layout()

    ts_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(PLOTS_DIR, f"ml_monitoring_{ts_str}.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_feature_importance(top_features, tag_meta, model_name, noc_tag, top_n=15):
    _ensure_plots_dir()

    features = top_features[:top_n]
    tags = [f["tag"] for f in features]
    importances = [f["importance"] for f in features]

    labels = []
    for tag in tags:
        desc = tag_meta.get(tag, {}).get("description", tag)
        if len(desc) > 40:
            desc = desc[:37] + "..."
        labels.append(f"{desc}\n({tag})")

    uniform_baseline = 1.0 / len(top_features) if top_features else 0
    colors = [
        "#d62728" if imp > 0.05 else "#ff7f0e" if imp > 0.02 else "#1f77b4"
        for imp in importances
    ]

    fig, ax = plt.subplots(figsize=(10, max(5, len(features) * 0.45)))
    y_pos = range(len(features))
    ax.barh(list(y_pos), importances, color=colors, alpha=0.85)
    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(labels, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("Feature Importance (normalised gain)")
    ax.set_title(
        f"{model_name} Feature Importance\n"
        f"Predicting {noc_tag} fault (out of [530–545°C]) from remaining tags",
        fontsize=10, fontweight="bold",
    )
    ax.axvline(x=uniform_baseline, color="grey", linestyle="--", linewidth=0.8,
               alpha=0.6, label=f"Uniform baseline ({uniform_baseline:.3f})")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3, axis="x")
    plt.tight_layout()

    ts_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(PLOTS_DIR, f"ml_feature_importance_{ts_str}.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


# ---------------------------------------------------------------------------
# Fault report
# ---------------------------------------------------------------------------

def generate_fault_report(periods, total_rows, anomaly_rate_pct):
    _ensure_plots_dir()
    date_str = f"{RUN_DATE[:4]}-{RUN_DATE[4:6]}-{RUN_DATE[6:]}"
    lines = [
        f"# ML Fault Detection Report — {date_str}",
        "",
        f"**Method:** Isolation Forest (semi-supervised, trained on NOC data)  ",
        f"**Total observations:** {total_rows}  ",
        f"**Anomaly rate:** {anomaly_rate_pct:.1f}%  ",
        f"**Fault periods detected:** {len(periods)}",
        "",
        "## Detected Fault Periods",
        "",
        "| # | Start | End | Duration (min) | Mean Score | Max Score |",
        "|---|-------|-----|----------------|------------|-----------|",
    ]
    for i, p in enumerate(periods, 1):
        lines.append(
            f"| {i} | {p['start']} | {p['end']} | {p['duration_min']} "
            f"| {p['mean_score']} | {p['max_score']} |"
        )
    lines.append("")

    path = os.path.join(PLOTS_DIR, "fault_report.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return path


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def main():
    args = parse_args()

    # 1. Load data
    print("Loading historian data...", file=sys.stderr)
    df, all_tags, tag_meta = load_data(
        args.downsample_minutes, args.start_time, args.end_time
    )
    print(
        f"Loaded {len(df)} rows × {len(all_tags)} tags "
        f"(downsampled to {args.downsample_minutes}-min averages).",
        file=sys.stderr,
    )

    if args.noc_tag not in df.columns:
        print(f"ERROR: NOC tag '{args.noc_tag}' not found in dataset.", file=sys.stderr)
        sys.exit(1)

    # 2. NOC split
    noc_mask = (df[args.noc_tag] >= args.noc_min) & (df[args.noc_tag] <= args.noc_max)
    df_noc = df[noc_mask]
    print(
        f"NOC split: {len(df_noc)}/{len(df)} rows "
        f"({len(df_noc)/len(df)*100:.1f}%) in normal range.",
        file=sys.stderr,
    )

    # 3. Fit Isolation Forest on NOC data
    print(
        f"Fitting Isolation Forest ({args.n_estimators} trees, "
        f"contamination={args.contamination})...",
        file=sys.stderr,
    )
    scaler, iforest = fit_isolation_forest(
        df_noc, args.n_estimators, args.contamination
    )

    # 4. Score full dataset
    print("Scoring full dataset...", file=sys.stderr)
    scores, predictions = score_all(df, scaler, iforest)
    anomaly_rate = float(np.mean(predictions == -1)) * 100
    print(f"Anomaly rate: {anomaly_rate:.1f}%", file=sys.stderr)

    # 5. Find fault periods
    timestamps = df.index.tolist()
    periods = find_fault_periods(timestamps, scores, predictions)
    print(f"Fault periods detected: {len(periods)}", file=sys.stderr)

    periods_by_severity = sorted(periods, key=lambda p: p["mean_score"], reverse=True)
    worst_events = periods_by_severity[: args.top_n_events]

    # 6. XGBoost feature importance
    print("Running XGBoost feature importance...", file=sys.stderr)
    top_features, xgb_model_name = fit_xgb_importance(
        df, args.noc_tag, args.noc_min, args.noc_max, args.no_xgb
    )
    if top_features:
        print(
            f"Top feature: {top_features[0]['tag']} "
            f"(importance={top_features[0]['importance']:.4f})",
            file=sys.stderr,
        )

    # 7. Plots
    print("Generating monitoring chart...", file=sys.stderr)
    monitoring_path = plot_monitoring(
        timestamps,
        df[args.noc_tag].values,
        scores,
        predictions,
        args.noc_min,
        args.noc_max,
        args.noc_tag,
    )

    feature_importance_path = None
    if top_features:
        print("Generating feature importance chart...", file=sys.stderr)
        feature_importance_path = plot_feature_importance(
            top_features, tag_meta, xgb_model_name, args.noc_tag
        )

    # 8. Fault report
    print("Generating fault report...", file=sys.stderr)
    report_path = generate_fault_report(periods, len(df), anomaly_rate)

    # 9. JSON summary
    summary = {
        "model": {
            "type": "IsolationForest",
            "n_estimators": args.n_estimators,
            "contamination": args.contamination,
            "noc_criteria": {
                "tag": args.noc_tag,
                "min": args.noc_min,
                "max": args.noc_max,
            },
            "noc_rows": len(df_noc),
            "total_rows": len(df),
            "tags_used": all_tags,
            "downsample_minutes": args.downsample_minutes,
        },
        "results": {
            "anomaly_rate_pct": round(anomaly_rate, 2),
            "n_fault_periods": len(periods),
            "fault_periods": periods,
        },
        "feature_importance": {
            "model": xgb_model_name,
            "target_tag": args.noc_tag,
            "top_features": top_features,
        },
        "worst_events": worst_events,
        "plots": {
            "monitoring": monitoring_path,
            "feature_importance": feature_importance_path,
            "fault_report": report_path,
        },
    }

    print(f"\nDone. Plots saved to {PLOTS_DIR}", file=sys.stderr)
    print(json.dumps(summary, indent=2, default=str))


if __name__ == "__main__":
    main()
