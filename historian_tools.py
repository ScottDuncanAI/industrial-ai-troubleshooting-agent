"""
Historian tool implementations for the boiler MCP server.

Covers all six historian_* tools: list_tags, search_tags, get_data_range,
get_tag_data, get_statistics, and plot_tags.

The MCP server (historian_mcp_server.py) imports and calls these directly;
this module has no knowledge of MCP types or the server protocol.
"""

import os
import re
from datetime import datetime

import duckdb
import matplotlib
matplotlib.use("Agg")
from hmi_style import apply_hmi_style, TICK_COLOR, SPINE_COLOR
apply_hmi_style()
from plot_helpers import plot_normalized

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH     = os.path.join(PROJECT_DIR, "boiler_historian.duckdb")
PLOTS_DIR   = os.path.join(PROJECT_DIR, "plots")

_JUNCTION = r"C:\boiler"

def _short_path(p: str) -> str:
    """Replace the long project root with the C:\\boiler junction, but ONLY when that
    junction actually resolves to THIS project directory.

    C:\\boiler is an optional personal convenience: a Windows junction pointing at the
    project so file links stay short. If the junction is absent (most users), or points
    at a *different* copy of the project, substituting it would produce a path that does
    not resolve, so we return the real absolute path unchanged."""
    try:
        if os.path.exists(_JUNCTION) and \
                os.path.realpath(_JUNCTION) == os.path.realpath(PROJECT_DIR):
            rel = os.path.relpath(p, PROJECT_DIR)
            return os.path.join(_JUNCTION, rel)
    except (ValueError, OSError):
        pass
    return p


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _parse_time(ts: str) -> datetime:
    """Parse and validate an ISO datetime string. Raises ValueError on bad input."""
    try:
        return datetime.fromisoformat(ts.strip())
    except ValueError:
        raise ValueError(f"Invalid datetime: {ts!r}. Expected e.g. '2022-03-29 08:00:00'")


def get_connection() -> duckdb.DuckDBPyConnection:
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(
            f"Database not found at {DB_PATH}. This file ships with the repository; "
            f"if it is missing, re-clone the project or run /setup."
        )
    return duckdb.connect(DB_PATH, read_only=True)


def _validate_tags(con: duckdb.DuckDBPyConnection, tag_names: list[str]) -> None:
    """Raise ValueError listing any tag names not present as columns in historian_data."""
    valid_cols = {
        r[0] for r in con.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_name = 'historian_data'"
        ).fetchall()
    }
    valid_cols.discard("timestamp")
    bad_tags = [t for t in tag_names if t not in valid_cols]
    if bad_tags:
        raise ValueError(f"Unknown tag(s): {bad_tags}. Use historian_list_tags to see available tags.")


# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------

def tool_list_tags() -> list[dict]:
    con = get_connection()
    rows = con.execute("""
        SELECT tag_name, description, units, sensor_type, normal_min, normal_max
        FROM tags
        ORDER BY sensor_type, tag_name
    """).fetchall()
    con.close()
    return [
        {
            "tag_name":    r[0],
            "description": r[1],
            "units":       r[2],
            "sensor_type": r[3],
            "normal_min":  r[4],
            "normal_max":  r[5],
        }
        for r in rows
    ]


def tool_search_tags(query: str) -> list[dict]:
    con = get_connection()
    q = f"%{query.lower()}%"
    rows = con.execute("""
        SELECT tag_name, description, units, sensor_type, normal_min, normal_max
        FROM tags
        WHERE LOWER(tag_name)    LIKE ?
           OR LOWER(description) LIKE ?
           OR LOWER(sensor_type) LIKE ?
        ORDER BY sensor_type, tag_name
    """, [q, q, q]).fetchall()
    con.close()
    return [
        {
            "tag_name":    r[0],
            "description": r[1],
            "units":       r[2],
            "sensor_type": r[3],
            "normal_min":  r[4],
            "normal_max":  r[5],
        }
        for r in rows
    ]


def tool_get_data_range() -> dict:
    con = get_connection()
    row = con.execute("""
        SELECT MIN(timestamp) AS earliest,
               MAX(timestamp) AS latest,
               COUNT(*)       AS total_rows
        FROM historian_data
    """).fetchone()
    con.close()
    return {
        "earliest_timestamp": str(row[0]),
        "latest_timestamp":   str(row[1]),
        "total_rows":         row[2],
        "note": (
            "This is a static 5-day snapshot. Treat 'latest_timestamp' as "
            "'now' when the user asks about relative time periods like "
            "'past 12 hours' or 'last day'."
        ),
    }


def tool_get_tag_data(
    tag_names: list[str],
    start_time: str,
    end_time: str,
    downsample_minutes: int | None = None,
) -> dict:
    if downsample_minutes is not None:
        if not isinstance(downsample_minutes, int) or not (1 <= downsample_minutes <= 1440):
            raise ValueError("downsample_minutes must be an integer between 1 and 1440.")

    start_dt = _parse_time(start_time)
    end_dt   = _parse_time(end_time)

    con = get_connection()
    _validate_tags(con, tag_names)

    if downsample_minutes:
        tag_select = ", ".join([f'AVG("{t}") AS "{t}"' for t in tag_names])
        query = f"""
            SELECT
                TIME_BUCKET(INTERVAL '{downsample_minutes} minutes', timestamp) AS timestamp,
                {tag_select}
            FROM historian_data
            WHERE timestamp >= ? AND timestamp <= ?
            GROUP BY 1
            ORDER BY 1
        """
    else:
        tag_select = ", ".join([f'"{t}"' for t in tag_names])
        query = f"""
            SELECT timestamp, {tag_select}
            FROM historian_data
            WHERE timestamp >= ? AND timestamp <= ?
            ORDER BY timestamp
        """

    try:
        rows = con.execute(query, [start_dt, end_dt]).fetchall()
    except Exception as e:
        # TIME_BUCKET may not be available in all DuckDB versions; fall back to date_trunc
        if downsample_minutes and "TIME_BUCKET" in str(e).upper():
            tag_select = ", ".join([f'AVG("{t}") AS "{t}"' for t in tag_names])
            query = f"""
                SELECT
                    DATE_TRUNC('minute', timestamp)
                        + INTERVAL '{downsample_minutes} minutes'
                        * (EXTRACT(MINUTE FROM timestamp)::INT / {downsample_minutes}) AS timestamp,
                    {tag_select}
                FROM historian_data
                WHERE timestamp >= ? AND timestamp <= ?
                GROUP BY 1
                ORDER BY 1
            """
            rows = con.execute(query, [start_dt, end_dt]).fetchall()
        else:
            con.close()
            raise

    con.close()

    col_names = ["timestamp"] + tag_names
    data = [dict(zip(col_names, row)) for row in rows]

    return {
        "tag_names":          tag_names,
        "start_time":         start_time,
        "end_time":           end_time,
        "downsample_minutes": downsample_minutes,
        "row_count":          len(data),
        "data":               data,
    }


def tool_get_statistics(
    tag_names: list[str],
    start_time: str,
    end_time: str,
) -> dict:
    start_dt = _parse_time(start_time)
    end_dt   = _parse_time(end_time)

    con = get_connection()
    _validate_tags(con, tag_names)

    results = {}
    for tag in tag_names:
        row = con.execute(f"""
            SELECT
                MIN("{tag}")    AS min_val,
                MAX("{tag}")    AS max_val,
                AVG("{tag}")    AS mean_val,
                STDDEV("{tag}") AS std_val,
                COUNT("{tag}")  AS count_val
            FROM historian_data
            WHERE timestamp >= ? AND timestamp <= ?
        """, [start_dt, end_dt]).fetchone()

        meta = con.execute(
            "SELECT description, units, normal_min, normal_max FROM tags WHERE tag_name = ?", [tag]
        ).fetchone()

        results[tag] = {
            "description": meta[0] if meta else None,
            "units":       meta[1] if meta else None,
            "min":         round(row[0], 4) if row[0] is not None else None,
            "max":         round(row[1], 4) if row[1] is not None else None,
            "mean":        round(row[2], 4) if row[2] is not None else None,
            "std":         round(row[3], 4) if row[3] is not None else None,
            "count":       row[4],
            "normal_min":  meta[2] if meta else None,
            "normal_max":  meta[3] if meta else None,
        }

    con.close()
    return {
        "start_time": start_time,
        "end_time":   end_time,
        "statistics": results,
    }


def _fetch_minmax_series(
    con: duckdb.DuckDBPyConnection,
    tag: str,
    start_dt: datetime,
    end_dt: datetime,
    downsample_minutes: int,
) -> tuple[list[datetime], list[float]]:
    """
    Bucket the tag into downsample_minutes-wide windows and, for each bucket,
    emit the min and max values at their actual timestamps (in chronological
    order). This mirrors PI ProcessBook/Vision "Plot" mode: a single trend
    line that still shows spikes/dips, instead of an AVG line that smooths
    them away.
    """
    query = f"""
        SELECT
            TIME_BUCKET(INTERVAL '{downsample_minutes} minutes', timestamp) AS bucket,
            arg_min(timestamp, "{tag}") AS t_lo, MIN("{tag}") AS v_lo,
            arg_max(timestamp, "{tag}") AS t_hi, MAX("{tag}") AS v_hi
        FROM historian_data
        WHERE timestamp >= ? AND timestamp <= ?
        GROUP BY 1
        ORDER BY 1
    """
    try:
        rows = con.execute(query, [start_dt, end_dt]).fetchall()
    except Exception as e:
        if "TIME_BUCKET" in str(e).upper():
            query = f"""
                SELECT
                    DATE_TRUNC('minute', timestamp)
                        + INTERVAL '{downsample_minutes} minutes'
                        * (EXTRACT(MINUTE FROM timestamp)::INT / {downsample_minutes}) AS bucket,
                    arg_min(timestamp, "{tag}") AS t_lo, MIN("{tag}") AS v_lo,
                    arg_max(timestamp, "{tag}") AS t_hi, MAX("{tag}") AS v_hi
                FROM historian_data
                WHERE timestamp >= ? AND timestamp <= ?
                GROUP BY 1
                ORDER BY 1
            """
            rows = con.execute(query, [start_dt, end_dt]).fetchall()
        else:
            raise

    timestamps: list[datetime] = []
    values: list[float] = []
    for _, t_lo, v_lo, t_hi, v_hi in rows:
        if v_lo is None:
            continue
        pts = sorted([(t_lo, v_lo), (t_hi, v_hi)], key=lambda p: p[0])
        if pts[0][0] == pts[1][0]:
            timestamps.append(pts[0][0])
            values.append(pts[0][1])
        else:
            for t, v in pts:
                timestamps.append(t)
                values.append(v)
    return timestamps, values


def tool_plot_tags(
    tag_names: list[str],
    start_time: str,
    end_time: str,
    title: str | None = None,
    downsample_minutes: int | None = None,
    show_normal_range: bool = False,
) -> dict:
    if downsample_minutes is not None:
        if not isinstance(downsample_minutes, int) or not (1 <= downsample_minutes <= 1440):
            raise ValueError("downsample_minutes must be an integer between 1 and 1440.")

    import matplotlib.pyplot as plt

    start_dt = _parse_time(start_time)
    end_dt   = _parse_time(end_time)

    con = get_connection()
    _validate_tags(con, tag_names)

    if downsample_minutes:
        series = {
            tag: _fetch_minmax_series(con, tag, start_dt, end_dt, downsample_minutes)
            for tag in tag_names
        }
        row_count = max((len(ts) for ts, _ in series.values()), default=0)
    else:
        rows = con.execute(
            f"""
            SELECT timestamp, {", ".join(f'"{t}"' for t in tag_names)}
            FROM historian_data
            WHERE timestamp >= ? AND timestamp <= ?
            ORDER BY timestamp
            """,
            [start_dt, end_dt],
        ).fetchall()
        timestamps = [r[0] for r in rows]
        series = {
            tag: (timestamps, [r[i + 1] for r in rows])
            for i, tag in enumerate(tag_names)
        }
        row_count = len(rows)

    if row_count == 0:
        con.close()
        return {"error": "No data found for the specified time range."}

    meta_rows = con.execute(
        f"SELECT tag_name, description, units, normal_min, normal_max "
        f"FROM tags WHERE tag_name IN ({','.join(['?'] * len(tag_names))})",
        tag_names,
    ).fetchall()
    con.close()
    meta = {
        r[0]: {"description": r[1], "units": r[2], "normal_min": r[3], "normal_max": r[4]}
        for r in meta_rows
    }

    # Determine scaling method: use "range" only when every tag has engineering
    # limits stored; fall back to "minmax" when any tag is unconfigured.
    ranges: dict[str, tuple[float, float]] = {}
    for tag in tag_names:
        m  = meta.get(tag, {})
        lo = m.get("normal_min")
        hi = m.get("normal_max")
        if lo is not None and hi is not None:
            ranges[tag] = (float(lo), float(hi))

    if len(ranges) == len(tag_names):
        method = "range"
    else:
        method = "minmax"
        ranges = None  # type: ignore[assignment]

    fig, ax = plot_normalized(
        series, tag_names,
        method=method,
        ranges=ranges,
    )

    # In range mode, draw faint boundary lines at the actual normal_min/normal_max
    # engineering values so that excursions beyond normal limits are visible.
    if show_normal_range and method == "range":
        first_meta = meta.get(tag_names[0], {})
        norm_lo = first_meta.get("normal_min")
        norm_hi = first_meta.get("normal_max")
        if norm_lo is not None:
            ax.axhline(float(norm_lo), color=SPINE_COLOR, linewidth=0.8, linestyle=":", zorder=1)
        if norm_hi is not None:
            ax.axhline(float(norm_hi), color=SPINE_COLOR, linewidth=0.8, linestyle=":", zorder=1)

    resample_note = (
        f"  ·  downsampled to {downsample_minutes}-min min/max envelope"
        if downsample_minutes else "  ·  raw 5-sec data"
    )
    fig.text(
        0.5, -0.02,
        f"{start_time}  →  {end_time}{resample_note}",
        ha="center", fontsize=7.5, color=TICK_COLOR,
        transform=fig.transFigure,
    )

    os.makedirs(PLOTS_DIR, exist_ok=True)
    safe_tags     = "_".join(re.sub(r"[^\w\-]", "", t) for t in tag_names)
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath      = os.path.join(PLOTS_DIR, f"{safe_tags}_{timestamp_str}.png")
    fig.savefig(filepath, bbox_inches="tight")
    plt.close(fig)

    short = _short_path(filepath)
    return {
        "plot_path":   short,
        "message":     f"Plot saved to {short}. Open this file to view the chart.",
        "tag_names":   tag_names,
        "start_time":  start_time,
        "end_time":    end_time,
        "data_points": row_count,
    }
