"""
MSPC Analysis — Multivariate Statistical Process Control for the boiler historian.

Runs a PCA-based monitoring pipeline on the 5-day historian dataset:
  1. Load & downsample all 30 tags to 1-minute averages
  2. Split NOC (normal) training data using TE_8332A range [530, 545]°C
  3. Fit StandardScaler + PCA on NOC data
  4. Compute T² and SPE for the full dataset with statistical control limits
  5. Generate monitoring charts and contribution plots for worst events

Usage:
  python mspc_analysis.py [--downsample-minutes 1] [--cpv-threshold 0.85] ...

Outputs JSON summary to stdout. Saves plots to plots/ directory.
"""

import os
import sys
import json
import argparse
from datetime import datetime

import numpy as np
import pandas as pd
import duckdb
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy import stats

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, "boiler_historian.duckdb")
RUN_TIMESTAMP = datetime.now()
RUN_DATE = RUN_TIMESTAMP.strftime("%Y%m%d")
RUN_TIME = RUN_TIMESTAMP.strftime("%H%M%S")
PLOTS_DIR = os.path.join(PROJECT_DIR, "plots", "MSPC", f"MSPC_{RUN_DATE}_{RUN_TIME}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args():
    p = argparse.ArgumentParser(description="MSPC analysis on boiler historian data")
    p.add_argument("--downsample-minutes", type=int, default=1)
    p.add_argument("--noc-tag", default="TE_8332A")
    p.add_argument("--noc-min", type=float, default=530.0)
    p.add_argument("--noc-max", type=float, default=545.0)
    p.add_argument("--cpv-threshold", type=float, default=0.85)
    p.add_argument("--n-components", type=int, default=None)
    p.add_argument("--exclude-tags", type=str, default=None,
                   help="Comma-separated list of tags to exclude")
    p.add_argument("--start-time", type=str, default=None,
                   help="Start timestamp filter (YYYY-MM-DD HH:MM:SS)")
    p.add_argument("--end-time", type=str, default=None,
                   help="End timestamp filter (YYYY-MM-DD HH:MM:SS)")
    p.add_argument("--top-n-events", type=int, default=5)
    p.add_argument("--top-n-contributors", type=int, default=15)
    return p.parse_args()


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_data(downsample_minutes=1, exclude_tags=None, start_time=None, end_time=None):
    con = duckdb.connect(DB_PATH, read_only=True)

    tag_rows = con.execute("SELECT tag_name FROM tags ORDER BY tag_name").fetchall()
    all_tags = [r[0] for r in tag_rows]

    if exclude_tags:
        all_tags = [t for t in all_tags if t not in exclude_tags]

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
# Model building
# ---------------------------------------------------------------------------

def build_model(df_noc, n_components=None, cpv_threshold=0.85):
    scaler = StandardScaler()
    X_noc = scaler.fit_transform(df_noc.values)

    pca_full = PCA().fit(X_noc)
    all_eigenvalues = pca_full.explained_variance_

    if n_components is None:
        cumvar = np.cumsum(pca_full.explained_variance_ratio_)
        n_components = int(np.argmax(cumvar >= cpv_threshold) + 1)
        n_components = max(n_components, 1)

    pca = PCA(n_components=n_components).fit(X_noc)

    return {
        "scaler": scaler,
        "pca": pca,
        "pca_full": pca_full,
        "all_eigenvalues": all_eigenvalues,
        "n_components": n_components,
        "n_train": len(df_noc),
    }


# ---------------------------------------------------------------------------
# Monitoring statistics
# ---------------------------------------------------------------------------

def compute_monitoring(X_scaled, model):
    pca = model["pca"]
    eigenvalues = pca.explained_variance_

    scores = pca.transform(X_scaled)
    t2 = np.sum(scores ** 2 / eigenvalues, axis=1)

    X_hat = pca.inverse_transform(scores)
    residuals = X_scaled - X_hat
    spe = np.sum(residuals ** 2, axis=1)

    return t2, spe, scores


def compute_control_limits(model, alpha_levels=(0.05, 0.01)):
    n = model["n_train"]
    A = model["n_components"]
    residual_eig = model["all_eigenvalues"][A:]

    limits = {}
    for alpha in alpha_levels:
        conf = int((1 - alpha) * 100)

        f_val = stats.f.ppf(1 - alpha, A, n - A)
        limits[f"T2_{conf}"] = A * (n ** 2 - 1) / (n * (n - A)) * f_val

        if len(residual_eig) > 0:
            theta1 = np.sum(residual_eig)
            theta2 = np.sum(residual_eig ** 2)
            theta3 = np.sum(residual_eig ** 3)

            if theta1 > 0 and theta2 > 0:
                h0 = 1 - (2 * theta1 * theta3) / (3 * theta2 ** 2)
                c_alpha = stats.norm.ppf(1 - alpha)

                if h0 > 0:
                    term = c_alpha * np.sqrt(2 * theta2 * h0 ** 2) / theta1
                    term += 1 + theta2 * h0 * (h0 - 1) / theta1 ** 2
                    limits[f"SPE_{conf}"] = theta1 * (max(term, 0) ** (1 / h0))
                else:
                    limits[f"SPE_{conf}"] = theta1 * (
                        1 + c_alpha * np.sqrt(2 * theta2) / theta1
                    ) ** 2
            else:
                limits[f"SPE_{conf}"] = 0.0
        else:
            limits[f"SPE_{conf}"] = 0.0

    return limits


# ---------------------------------------------------------------------------
# Anomalous period detection
# ---------------------------------------------------------------------------

def find_anomalous_periods(timestamps, t2, spe, t2_limit, spe_limit):
    anomalous = (t2 > t2_limit) | (spe > spe_limit)
    periods = []
    in_period = False
    start_idx = 0

    for i in range(len(anomalous)):
        if anomalous[i] and not in_period:
            start_idx = i
            in_period = True
        elif not anomalous[i] and in_period:
            in_period = False
            _append_period(periods, timestamps, t2, spe, t2_limit, spe_limit,
                           start_idx, i - 1)

    if in_period:
        _append_period(periods, timestamps, t2, spe, t2_limit, spe_limit,
                       start_idx, len(anomalous) - 1)

    return periods


def _append_period(periods, timestamps, t2, spe, t2_limit, spe_limit, s, e):
    t2_slice = t2[s : e + 1]
    spe_slice = spe[s : e + 1]

    has_t2 = np.any(t2_slice > t2_limit)
    has_spe = np.any(spe_slice > spe_limit)
    if has_t2 and has_spe:
        atype = "T2+SPE"
        peak_idx = s + int(np.argmax(t2_slice))
    elif has_t2:
        atype = "T2"
        peak_idx = s + int(np.argmax(t2_slice))
    else:
        atype = "SPE"
        peak_idx = s + int(np.argmax(spe_slice))

    periods.append({
        "start": str(timestamps[s]),
        "end": str(timestamps[e]),
        "duration_min": round(
            (timestamps[e] - timestamps[s]).total_seconds() / 60, 1
        ),
        "type": atype,
        "max_T2": round(float(np.max(t2_slice)), 2),
        "max_SPE": round(float(np.max(spe_slice)), 2),
        "peak_idx": peak_idx,
    })


# ---------------------------------------------------------------------------
# Contribution analysis
# ---------------------------------------------------------------------------

def compute_t2_contributions(X_scaled, model):
    """Miller et al. (1998) decomposition — contributions sum exactly to T²."""
    pca = model["pca"]
    eigenvalues = pca.explained_variance_

    X_centered = X_scaled - pca.mean_
    scores = pca.transform(X_scaled)
    loadings = pca.components_.T  # (n_features, n_components)

    weight = scores / eigenvalues  # (n_obs, n_components)
    weighted_loadings = weight @ loadings.T  # (n_obs, n_features)
    return X_centered * weighted_loadings


def compute_spe_contributions(X_scaled, model):
    """Squared residuals per variable — contributions sum exactly to SPE."""
    pca = model["pca"]
    X_hat = pca.inverse_transform(pca.transform(X_scaled))
    return (X_scaled - X_hat) ** 2


# ---------------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------------

def _ensure_plots_dir():
    os.makedirs(PLOTS_DIR, exist_ok=True)


def plot_scree(model):
    _ensure_plots_dir()
    pca_full = model["pca_full"]
    n_retained = model["n_components"]

    n_show = min(len(pca_full.explained_variance_ratio_), 20)
    components = range(1, n_show + 1)
    var_pct = pca_full.explained_variance_ratio_[:n_show] * 100
    cumvar_pct = np.cumsum(pca_full.explained_variance_ratio_)[:n_show] * 100

    fig, ax1 = plt.subplots(figsize=(10, 5))

    bars = ax1.bar(components, var_pct, color="#1f77b4", alpha=0.7, label="Individual")
    for i in range(min(n_retained, len(bars))):
        bars[i].set_color("#2ca02c")
    ax1.set_xlabel("Principal Component")
    ax1.set_ylabel("Explained Variance (%)")
    ax1.set_xticks(list(components))

    ax2 = ax1.twinx()
    ax2.plot(components, cumvar_pct, "o-", color="#d62728", linewidth=1.5,
             markersize=4, label="Cumulative")
    ax2.set_ylabel("Cumulative Variance (%)")
    ax2.axhline(y=cumvar_pct[n_retained - 1], color="#d62728",
                linestyle="--", alpha=0.4)

    ax1.set_title(
        f"PCA Scree Plot — {n_retained} components retained "
        f"({cumvar_pct[n_retained - 1]:.1f}% variance)"
    )

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="center right")

    plt.tight_layout()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(PLOTS_DIR, f"mspc_scree_{ts}.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_monitoring(timestamps, te_values, t2, spe, limits, noc_min, noc_max):
    _ensure_plots_dir()

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 10), sharex=True)
    ts_arr = np.array(timestamps)

    # --- Panel 1: TE_8332A ---
    ax1.plot(timestamps, te_values, linewidth=0.6, color="#1f77b4")
    ax1.axhspan(noc_min, noc_max, alpha=0.15, color="green",
                label=f"Normal ({noc_min}–{noc_max}°C)")
    ax1.set_ylabel("TE_8332A (°C)")
    ax1.set_title("Boiler Outlet Steam Temperature", fontsize=9, loc="left")
    ax1.legend(fontsize=8, loc="upper right")
    ax1.grid(True, alpha=0.3)

    # --- Panel 2: T² ---
    ax2.plot(timestamps, t2, linewidth=0.6, color="#1f77b4")
    ax2.axhline(y=limits["T2_95"], color="#ff7f0e", linestyle="--", linewidth=1,
                label=f"95% ({limits['T2_95']:.1f})")
    ax2.axhline(y=limits["T2_99"], color="#d62728", linestyle="--", linewidth=1,
                label=f"99% ({limits['T2_99']:.1f})")

    mask_95 = t2 > limits["T2_95"]
    mask_99 = t2 > limits["T2_99"]
    if np.any(mask_95 & ~mask_99):
        ax2.scatter(ts_arr[mask_95 & ~mask_99], t2[mask_95 & ~mask_99],
                    s=3, c="#ff7f0e", zorder=5, alpha=0.5)
    if np.any(mask_99):
        ax2.scatter(ts_arr[mask_99], t2[mask_99],
                    s=3, c="#d62728", zorder=5, alpha=0.5)

    ax2.set_ylabel("Hotelling's T²")
    ax2.set_title("T² Statistic (within-model variation)", fontsize=9, loc="left")
    ax2.legend(fontsize=8, loc="upper right")
    ax2.grid(True, alpha=0.3)

    # --- Panel 3: SPE ---
    ax3.plot(timestamps, spe, linewidth=0.6, color="#1f77b4")
    ax3.axhline(y=limits["SPE_95"], color="#ff7f0e", linestyle="--", linewidth=1,
                label=f"95% ({limits['SPE_95']:.1f})")
    ax3.axhline(y=limits["SPE_99"], color="#d62728", linestyle="--", linewidth=1,
                label=f"99% ({limits['SPE_99']:.1f})")

    mask_95s = spe > limits["SPE_95"]
    mask_99s = spe > limits["SPE_99"]
    if np.any(mask_95s & ~mask_99s):
        ax3.scatter(ts_arr[mask_95s & ~mask_99s], spe[mask_95s & ~mask_99s],
                    s=3, c="#ff7f0e", zorder=5, alpha=0.5)
    if np.any(mask_99s):
        ax3.scatter(ts_arr[mask_99s], spe[mask_99s],
                    s=3, c="#d62728", zorder=5, alpha=0.5)

    ax3.set_ylabel("SPE / Q")
    ax3.set_title("SPE Statistic (outside-model variation)", fontsize=9, loc="left")
    ax3.legend(fontsize=8, loc="upper right")
    ax3.grid(True, alpha=0.3)

    # --- Shade anomalous regions across all panels ---
    anomalous = (t2 > limits["T2_95"]) | (spe > limits["SPE_95"])
    diff = np.diff(anomalous.astype(int))
    starts = np.where(diff == 1)[0] + 1
    ends = np.where(diff == -1)[0] + 1

    if anomalous[0]:
        starts = np.insert(starts, 0, 0)
    if anomalous[-1]:
        ends = np.append(ends, len(anomalous))

    for s, e in zip(starts, ends):
        e_clamp = min(e, len(timestamps) - 1)
        for ax in (ax1, ax2, ax3):
            ax.axvspan(timestamps[s], timestamps[e_clamp], alpha=0.08, color="red")

    ax3.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M"))
    fig.autofmt_xdate(rotation=30)
    fig.suptitle("MSPC Monitoring — Boiler Historian (5-Day Dataset)",
                 fontsize=11, fontweight="bold")
    plt.tight_layout()

    ts_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(PLOTS_DIR, f"mspc_monitoring_{ts_str}.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_contribution(timestamp_str, t2_val, spe_val, t2_contribs, spe_contribs,
                      tag_names, tag_meta, top_n=15, limits=None):
    _ensure_plots_dir()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, max(6, top_n * 0.35)))

    for ax, contribs, stat_name, stat_val, limit_key in [
        (ax1, t2_contribs, "T²", t2_val, "T2_99"),
        (ax2, spe_contribs, "SPE", spe_val, "SPE_99"),
    ]:
        sorted_idx = np.argsort(np.abs(contribs))[::-1][:top_n]
        sorted_vals = contribs[sorted_idx]
        sorted_tags = [tag_names[i] for i in sorted_idx]

        labels = []
        for tag in sorted_tags:
            desc = tag_meta.get(tag, {}).get("description", tag)
            if len(desc) > 35:
                desc = desc[:32] + "..."
            labels.append(f"{desc}\n({tag})")

        colors = ["#d62728" if v > 0 else "#1f77b4" for v in sorted_vals]

        y_pos = range(len(sorted_vals))
        ax.barh(y_pos, sorted_vals, color=colors, alpha=0.8)
        ax.set_yticks(list(y_pos))
        ax.set_yticklabels(labels, fontsize=7)
        ax.invert_yaxis()
        ax.axvline(x=0, color="black", linewidth=0.5)
        ax.grid(True, alpha=0.3, axis="x")

        lim_str = ""
        if limits and limit_key in limits:
            lim_str = f"  |  limit₉₉ = {limits[limit_key]:.1f}"
        ax.set_title(f"{stat_name} = {stat_val:.1f}{lim_str}",
                     fontsize=9, fontweight="bold")
        ax.set_xlabel(f"{stat_name} Contribution")

    fig.suptitle(f"MSPC Contributions at {timestamp_str}",
                 fontsize=11, fontweight="bold")
    plt.tight_layout()

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_ts = timestamp_str.replace(":", "").replace(" ", "_").replace("-", "")
    path = os.path.join(PLOTS_DIR, f"mspc_contrib_{safe_ts}_{ts}.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


# ---------------------------------------------------------------------------
# Fault report
# ---------------------------------------------------------------------------

def generate_fault_report(periods, limits, model, plots_dir,
                          t2_contribs_all, spe_contribs_all, tag_names):
    os.makedirs(plots_dir, exist_ok=True)
    lines = [
        f"# MSPC Fault Report — {RUN_DATE[:4]}-{RUN_DATE[4:6]}-{RUN_DATE[6:]}",
        "",
        f"**Model:** {model['n_components']} PCA components  ",
        f"**T² 95% limit:** {limits['T2_95']:.2f}  ",
        f"**SPE 95% limit:** {limits['SPE_95']:.2f}  ",
        f"**Faults detected:** {len(periods)}",
        "",
        "## Detected Faults",
        "",
        "| # | Start | End | Duration (min) | Type | Max T² | Max SPE | Top Contributor |",
        "|---|-------|-----|----------------|------|--------|---------|-----------------|",
    ]

    for i, p in enumerate(periods, 1):
        idx = p["peak_idx"]
        if p["type"] in ("T2", "T2+SPE"):
            top_tag = tag_names[int(np.argmax(np.abs(t2_contribs_all[idx])))]
        else:
            top_tag = tag_names[int(np.argmax(spe_contribs_all[idx]))]
        lines.append(
            f"| {i} | {p['start']} | {p['end']} | {p['duration_min']} "
            f"| {p['type']} | {p['max_T2']} | {p['max_SPE']} | {top_tag} |"
        )

    lines.append("")

    path = os.path.join(plots_dir, "fault_report.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return path


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def main():
    args = parse_args()

    exclude_tags = None
    if args.exclude_tags:
        exclude_tags = [t.strip() for t in args.exclude_tags.split(",")]

    # 1. Load data
    print("Loading historian data...", file=sys.stderr)
    df, tag_names, tag_meta = load_data(args.downsample_minutes, exclude_tags,
                                        args.start_time, args.end_time)

    if args.noc_tag not in tag_names:
        print(f"ERROR: NOC tag '{args.noc_tag}' not in dataset "
              f"(excluded or missing).", file=sys.stderr)
        sys.exit(1)

    # 2. NOC split
    noc_mask = (df[args.noc_tag] >= args.noc_min) & (df[args.noc_tag] <= args.noc_max)
    df_noc = df[noc_mask]
    print(f"NOC split: {len(df_noc)}/{len(df)} rows "
          f"({len(df_noc)/len(df)*100:.1f}%) in normal range.", file=sys.stderr)

    # 3. Build model
    print("Fitting PCA model...", file=sys.stderr)
    model = build_model(df_noc, args.n_components, args.cpv_threshold)
    cumvar = np.cumsum(model["pca_full"].explained_variance_ratio_)
    print(f"Retained {model['n_components']} components "
          f"({cumvar[model['n_components']-1]*100:.1f}% variance).", file=sys.stderr)

    # 4. Monitor full dataset
    print("Computing monitoring statistics...", file=sys.stderr)
    X_full = model["scaler"].transform(df.values)
    t2, spe, scores = compute_monitoring(X_full, model)
    limits = compute_control_limits(model)

    # 5. Find anomalous periods
    timestamps = df.index.tolist()
    periods = find_anomalous_periods(timestamps, t2, spe,
                                     limits["T2_95"], limits["SPE_95"])

    # 5b. Contribution arrays (needed for fault report and worst-event plots)
    print("Computing contributions for worst events...", file=sys.stderr)
    t2_contribs_all = compute_t2_contributions(X_full, model)
    spe_contribs_all = compute_spe_contributions(X_full, model)

    # 5c. Fault report
    print("Generating fault report...", file=sys.stderr)
    report_path = generate_fault_report(periods, limits, model, PLOTS_DIR,
                                        t2_contribs_all, spe_contribs_all, tag_names)

    # 6. Plots
    print("Generating scree plot...", file=sys.stderr)
    scree_path = plot_scree(model)

    print("Generating monitoring chart...", file=sys.stderr)
    monitoring_path = plot_monitoring(
        timestamps, df[args.noc_tag].values,
        t2, spe, limits, args.noc_min, args.noc_max,
    )

    # 7. Contribution plots for worst events
    worst_t2_idx = np.argsort(t2)[::-1][: args.top_n_events]
    worst_spe_idx = np.argsort(spe)[::-1][: args.top_n_events]

    contribution_plots = []
    worst_t2_events = []
    worst_spe_events = []

    plotted_indices = set()

    for idx in worst_t2_idx:
        ts_str = str(timestamps[idx])
        path = plot_contribution(
            ts_str, t2[idx], spe[idx],
            t2_contribs_all[idx], spe_contribs_all[idx],
            tag_names, tag_meta, args.top_n_contributors, limits,
        )
        contribution_plots.append(path)
        plotted_indices.add(idx)

        top_idx = np.argsort(np.abs(t2_contribs_all[idx]))[::-1][:5]
        worst_t2_events.append({
            "timestamp": ts_str,
            "T2_value": round(float(t2[idx]), 2),
            "SPE_value": round(float(spe[idx]), 2),
            "top_contributors": [
                {"tag": tag_names[i],
                 "contribution": round(float(t2_contribs_all[idx][i]), 3)}
                for i in top_idx
            ],
        })

    for idx in worst_spe_idx:
        ts_str = str(timestamps[idx])

        if idx not in plotted_indices:
            path = plot_contribution(
                ts_str, t2[idx], spe[idx],
                t2_contribs_all[idx], spe_contribs_all[idx],
                tag_names, tag_meta, args.top_n_contributors, limits,
            )
            contribution_plots.append(path)
            plotted_indices.add(idx)

        top_idx = np.argsort(spe_contribs_all[idx])[::-1][:5]
        worst_spe_events.append({
            "timestamp": ts_str,
            "SPE_value": round(float(spe[idx]), 2),
            "T2_value": round(float(t2[idx]), 2),
            "top_contributors": [
                {"tag": tag_names[i],
                 "contribution": round(float(spe_contribs_all[idx][i]), 3)}
                for i in top_idx
            ],
        })

    # 8. Build summary
    summary = {
        "model": {
            "n_components": model["n_components"],
            "cumulative_variance": round(
                float(cumvar[model["n_components"] - 1]), 4
            ),
            "explained_variance_per_component": [
                round(float(v), 4)
                for v in model["pca_full"].explained_variance_ratio_[
                    : model["n_components"]
                ]
            ],
            "training_rows": model["n_train"],
            "total_rows": len(df),
            "noc_criteria": {
                "tag": args.noc_tag,
                "min": args.noc_min,
                "max": args.noc_max,
            },
            "tags_used": tag_names,
            "downsample_minutes": args.downsample_minutes,
        },
        "control_limits": {k: round(float(v), 4) for k, v in limits.items()},
        "results": {
            "T2_exceedance_95_pct": round(
                float(np.mean(t2 > limits["T2_95"]) * 100), 2
            ),
            "T2_exceedance_99_pct": round(
                float(np.mean(t2 > limits["T2_99"]) * 100), 2
            ),
            "SPE_exceedance_95_pct": round(
                float(np.mean(spe > limits["SPE_95"]) * 100), 2
            ),
            "SPE_exceedance_99_pct": round(
                float(np.mean(spe > limits["SPE_99"]) * 100), 2
            ),
            "either_exceedance_95_pct": round(
                float(
                    np.mean(
                        (t2 > limits["T2_95"]) | (spe > limits["SPE_95"])
                    )
                    * 100
                ),
                2,
            ),
            "anomalous_periods": periods,
        },
        "worst_events": {
            "T2": worst_t2_events,
            "SPE": worst_spe_events,
        },
        "plots": {
            "scree": scree_path,
            "monitoring": monitoring_path,
            "contributions": contribution_plots,
            "fault_report": report_path,
        },
    }

    print(f"\nDone. {len(contribution_plots)} contribution plots generated.",
          file=sys.stderr)
    print(json.dumps(summary, indent=2, default=str))


if __name__ == "__main__":
    main()
