"""
Smoke test for hmi_style + plot_helpers.

Five tags with very different magnitudes and units rendered on one chart
with independent real-value Y-axes — identical to PI ProcessBook Multiple Scale.

Run: python smoke_test_plot.py
"""

import os
import numpy as np
from datetime import datetime, timedelta

import matplotlib
matplotlib.use("Agg")

from hmi_style import apply_hmi_style, SPINE_COLOR
apply_hmi_style()

from plot_helpers import plot_normalized

import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Synthetic data — 60 minutes of 1-minute samples
# ---------------------------------------------------------------------------
N   = 60
t0  = datetime(2022, 3, 28, 11, 0, 0)
timestamps = [t0 + timedelta(minutes=i) for i in range(N)]
rng = np.random.default_rng(42)


def smooth(arr, alpha=0.25):
    out = arr.copy()
    for i in range(1, len(out)):
        out[i] = alpha * out[i] + (1 - alpha) * out[i - 1]
    return out


# Furnace temperature  ~850 °C, brief dip mid-window
furnace_temp = smooth(rng.normal(850, 15, N))
furnace_temp[25:35] -= smooth(rng.normal(70, 10, 10))

# Main steam flow  ~120 t/h
steam_flow = smooth(rng.normal(120, 3, N)) + np.linspace(0, 8, N)

# Separator level  ~50 %
level = smooth(rng.normal(50, 4, N))

# Flue gas O2  ~3.5 %, dips during the furnace dip
o2 = smooth(rng.normal(3.5, 0.3, N))
o2[22:38] -= smooth(rng.normal(1.8, 0.3, 16))

# Furnace draft pressure  ~−110 Pa (negative gauge)
pressure = smooth(rng.normal(-110, 8, N))
pressure[24:36] += smooth(rng.normal(40, 12, 12))

series = {
    "TE_FURNACE": (timestamps, furnace_temp.tolist()),
    "FT_STEAM":   (timestamps, steam_flow.tolist()),
    "LT_SEP":     (timestamps, level.tolist()),
    "AIR_O2":     (timestamps, o2.tolist()),
    "PT_FURNACE": (timestamps, pressure.tolist()),
}

tags = list(series.keys())

# Engineering ranges (zero, span) — same concept as PI tag zero/span config
ranges = {
    "TE_FURNACE": (700.0,  1000.0),
    "FT_STEAM":   (0.0,    200.0),
    "LT_SEP":     (0.0,    100.0),
    "AIR_O2":     (0.0,    10.0),
    "PT_FURNACE": (-300.0, 0.0),
}

# ---------------------------------------------------------------------------
# Render — method="range" uses engineering zero/span for each axis
# ---------------------------------------------------------------------------
fig, ax = plot_normalized(
    series,
    tags,
    method="range",
    ranges=ranges,
    title="Smoke test — five tags with independent real-value Y-axes (method='range')",
)

outdir  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plots")
os.makedirs(outdir, exist_ok=True)
outpath = os.path.join(outdir, "smoke_test.png")
fig.savefig(outpath, bbox_inches="tight")
plt.close(fig)

print(f"Smoke test passed — plot saved to: {outpath}")
