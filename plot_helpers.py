"""
Multi-axis overlay plotting for the boiler historian.

Main entry point: plot_normalized()

Each tag gets its own independent Y-axis scaled to real engineering values,
all sharing one time (X) axis and one plot area — identical to PI ProcessBook
"Multiple Scale" mode.  No normalization; operators read actual units.

Three scaling modes control where each tag's Y-axis zero and span come from:
  "range"  — (zero, span) supplied via the ranges dict — fixed across windows
  "minmax" — derived from the tag's data in the queried window (PI Autorange)
  "zscore" — (mean-3σ, mean+3σ) derived from data; draws a mean reference line

Y-axes alternate left / right.  Each axis spine and tick labels are
colour-matched to the trace so operators can pair them at a glance.
"""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from itertools import cycle
from typing import Union

from hmi_style import PALETTE, BG_COLOR, TICK_COLOR, GRID_COLOR, SPINE_COLOR

SeriesDict = dict[str, tuple[list, list]]

# How far to push each successive axis off the plot edge (points)
_AXIS_OFFSET_PTS = 55


def _extract(data: Union["pd.DataFrame", SeriesDict], tag: str) -> tuple[list, list]:
    try:
        import pandas as pd
        if isinstance(data, pd.DataFrame):
            col = data[tag].dropna()
            return data.loc[col.index, "timestamp"].tolist(), col.tolist()
    except ImportError:
        pass
    return data[tag]


def _pad(lo: float, hi: float, frac: float = 0.08) -> tuple[float, float]:
    """Add symmetric padding so traces don't sit on the axis edges."""
    span = (hi - lo) or abs(lo) or 1.0
    pad  = span * frac
    return lo - pad, hi + pad


def plot_normalized(
    df: Union["pd.DataFrame", SeriesDict],
    tags: list[str],
    method: str = "range",
    ranges: dict[str, tuple[float, float]] | None = None,
    ax: plt.Axes | None = None,
    title: str | None = None,
) -> tuple[plt.Figure, plt.Axes]:
    """
    Overlay multiple tags with independent Y-axes showing real engineering values.

    Each tag's Y-axis is scaled so its zero/span fills the full plot height —
    identical to PI ProcessBook "Multiple Scale" / "Autorange" behaviour.
    Operators read actual units; trends are visually proportional across tags.

    Parameters
    ----------
    df : DataFrame (columns: 'timestamp', *tags) or dict {tag: (ts_list, val_list)}
    tags : tag names to plot, in order
    method : "range" | "minmax" | "zscore"
    ranges : {tag: (zero, span)} — required when method="range".
             Example: {"TE_8332A": (480.0, 600.0)}
    ax : host Axes to draw on; if None a new figure is created
    title : chart title (left-aligned via rcParams)

    Returns
    -------
    (fig, host_ax)  — host_ax is the first (left) Y-axis
    """
    if method not in ("minmax", "zscore", "range"):
        raise ValueError(
            f"Unknown method {method!r}. Choose 'range', 'minmax', or 'zscore'."
        )
    if method == "range":
        if ranges is None:
            raise ValueError(
                "method='range' requires a ranges dict: {tag: (zero, span)}."
            )
        missing = [t for t in tags if t not in ranges]
        if missing:
            raise ValueError(
                f"method='range': missing ranges for {missing}. "
                "Provide (zero, span) for every tag or switch to method='minmax'."
            )

    # ── Figure / host axes ───────────────────────────────────────────────────
    if ax is None:
        fig, host = plt.subplots(figsize=(14, 5))
    else:
        host = ax
        fig  = ax.figure

    # The host axes draws the background and the first trace.
    # All twin axes share the same x-axis and the same rectangular plot area.
    host.set_xlabel("")

    color_cycle = cycle(PALETTE)
    all_axes    = []  # (twin_ax, color, tag) in order

    for i, tag in enumerate(tags):
        color = next(color_cycle)
        ts, vals = _extract(df, tag)
        arr = np.array(vals, dtype=float)

        # ── Y-axis limits for this tag ────────────────────────────────────
        if method == "range":
            zero, span = ranges[tag]
            data_lo = float(np.nanmin(arr))
            data_hi = float(np.nanmax(arr))
            lo, hi = _pad(min(zero, data_lo), max(span, data_hi))
            mid_label = None
        elif method == "zscore":
            mu    = float(np.nanmean(arr))
            sigma = float(np.nanstd(arr)) or 1.0
            zero, span = mu - 3 * sigma, mu + 3 * sigma
            lo, hi = _pad(zero, span)
            mid_label = mu          # draw a mean reference line
        else:  # minmax
            zero = float(np.nanmin(arr))
            span = float(np.nanmax(arr))
            lo, hi = _pad(zero, span)
            mid_label = None

        # ── Pick or create the axes for this trace ────────────────────────
        if i == 0:
            cur_ax = host
        else:
            cur_ax = host.twinx()
            # Hide the default right spine that twinx creates
            cur_ax.spines["right"].set_visible(False)
            cur_ax.spines["left"].set_visible(False)

        # Alternate: even indices → left, odd → right
        side  = "left" if i % 2 == 0 else "right"
        # How many axes are already on this side?
        same_side = sum(1 for _, _, _, s in all_axes if s == side)
        offset    = same_side * _AXIS_OFFSET_PTS   # 0 for the first on each side

        if i == 0:
            # Host axis — already on the left at offset 0, no repositioning needed
            cur_ax.yaxis.set_ticks_position("left")
            cur_ax.yaxis.set_label_position("left")
        else:
            cur_ax.yaxis.set_ticks_position(side)
            cur_ax.yaxis.set_label_position(side)
            spine = cur_ax.spines[side]
            spine.set_visible(True)
            if offset > 0:
                spine.set_position(("outward", offset))
            # Hide the unused opposite spine
            opposite = "right" if side == "left" else "left"
            cur_ax.spines[opposite].set_visible(False)

        # Colour the spine and tick labels to match the trace
        cur_ax.spines[side].set_edgecolor(color)
        cur_ax.tick_params(axis="y", colors=color, labelsize=8)
        cur_ax.yaxis.label.set_color(color)

        cur_ax.set_ylim(lo, hi)

        # Plot trace
        cur_ax.plot(ts, arr, color=color, zorder=3)

        # Mean reference line for zscore mode
        if mid_label is not None:
            cur_ax.axhline(mid_label, color=color, linewidth=0.6,
                           linestyle="--", alpha=0.5, zorder=2)

        all_axes.append((cur_ax, color, tag, side))

    # ── Hide host grid on twin axes (host draws it) ──────────────────────────
    for cur_ax, _, _, _ in all_axes[1:]:
        cur_ax.grid(False)

    # ── X-axis formatting on host ────────────────────────────────────────────
    host.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M"))
    for lbl in host.get_xticklabels():
        lbl.set_rotation(30)
        lbl.set_ha("right")

    # ── Legend — one entry per tag, colour-matched, just above axes ──────────
    legend_lines  = [a[0].get_lines()[0] for a in all_axes]
    legend_labels = []
    for cur_ax, color, tag, side in all_axes:
        arr    = np.array(_extract(df, tag)[1], dtype=float)
        lo_val = float(np.nanmin(arr))
        hi_val = float(np.nanmax(arr))
        if method == "range" and ranges:
            zero, span = ranges[tag]
            legend_labels.append(f"{tag}  [{zero:.4g} – {span:.4g}]")
        elif method == "zscore":
            mu    = float(np.nanmean(arr))
            sigma = float(np.nanstd(arr))
            legend_labels.append(f"{tag}  (μ={mu:.4g}, σ={sigma:.3g})")
        else:
            legend_labels.append(f"{tag}  [{lo_val:.4g} – {hi_val:.4g}]")

    host.legend(
        legend_lines, legend_labels,
        loc="lower left",
        bbox_to_anchor=(0.0, 1.0),
        ncol=min(len(tags), 4),
        fontsize=8,
        frameon=False,
        borderaxespad=0,
    )

    return fig, host
