"""
Dark control-room theme for matplotlib.

Call apply_hmi_style() once at process startup (before any plt.subplots call).
Import BG_COLOR, TEXT_COLOR, etc. or PALETTE for use in custom drawing code.
"""

import matplotlib

# ---------------------------------------------------------------------------
# Colour constants
# ---------------------------------------------------------------------------
BG_COLOR    = "#0e1117"
TEXT_COLOR  = "#c8cdd6"
TICK_COLOR  = "#8a91a0"
GRID_COLOR  = "#222834"
SPINE_COLOR = "#3a4151"

PALETTE = [
    "#4dd0e1",  # cyan
    "#ffb74d",  # amber
    "#81c784",  # green
    "#e57373",  # red
    "#ba9cf0",  # purple
    "#64b5f6",  # blue
    "#fff176",  # yellow
    "#f06292",  # pink
]


def apply_hmi_style() -> None:
    """Apply the dark HMI theme globally via matplotlib rcParams."""
    matplotlib.rcParams.update({
        # Backgrounds
        "figure.facecolor":              BG_COLOR,
        "axes.facecolor":                BG_COLOR,

        # Text
        "text.color":                    TEXT_COLOR,
        "axes.labelcolor":               TEXT_COLOR,
        "xtick.color":                   TICK_COLOR,
        "ytick.color":                   TICK_COLOR,
        "xtick.labelcolor":              TICK_COLOR,
        "ytick.labelcolor":              TICK_COLOR,

        # Grid — y-only, drawn behind data
        "axes.grid":                     True,
        "axes.grid.axis":                "y",
        "grid.color":                    GRID_COLOR,
        "grid.linewidth":                0.6,
        "axes.axisbelow":                True,

        # Spines — hide top/right, style left/bottom
        "axes.spines.top":               False,
        "axes.spines.right":             False,
        "axes.edgecolor":                SPINE_COLOR,

        # Color cycle
        "axes.prop_cycle":               matplotlib.cycler("color", PALETTE),

        # Title: left-aligned, semibold, with padding
        "axes.titlelocation":            "left",
        "axes.titleweight":              "semibold",
        "axes.titlepad":                 10.0,
        "axes.titlecolor":               TEXT_COLOR,

        # Legend: frameless
        "legend.frameon":                False,
        "legend.labelcolor":             TEXT_COLOR,

        # Layout
        "figure.constrained_layout.use": True,

        # Lines: 1.6 pt, round caps
        "lines.linewidth":               1.6,
        "lines.solid_capstyle":          "round",

        # DPI
        "figure.dpi":                    120,
        "savefig.dpi":                   160,
        "savefig.facecolor":             BG_COLOR,

        # Font
        "font.family":                   "sans-serif",
        "font.sans-serif":               ["Inter", "Roboto", "DejaVu Sans"],
    })
