"""
Alarm log tool implementations for the boiler MCP server.

Covers all five alarm_* tools: query, get_statistics, get_active_at,
search_context, and detect_flood.

The MCP server (historian_mcp_server.py) imports and calls these directly;
this module has no knowledge of MCP types or the server protocol.

_parse_time is imported from historian_tools to avoid duplication.
"""

import os
from datetime import datetime, timedelta

import duckdb

from historian_tools import _parse_time

PROJECT_DIR   = os.path.dirname(os.path.abspath(__file__))
ALARM_DB_PATH = os.path.join(PROJECT_DIR, "boiler_alarms.duckdb")

_ALARM_ROW_KEYS = [
    "alarm_id", "tag_name", "alarm_level", "priority", "message",
    "setpoint", "activated_at", "activated_value", "acknowledged_at",
    "cleared_at", "duration_sec", "max_deviation",
]


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def get_alarm_connection() -> duckdb.DuckDBPyConnection:
    if not os.path.exists(ALARM_DB_PATH):
        raise FileNotFoundError(
            f"Alarm database not found at {ALARM_DB_PATH}. "
            "Run: python generate_alarms.py"
        )
    return duckdb.connect(ALARM_DB_PATH, read_only=True)


def _rows_to_dicts(rows: list) -> list[dict]:
    return [dict(zip(_ALARM_ROW_KEYS, r)) for r in rows]


def _to_dt(val) -> datetime:
    if isinstance(val, datetime):
        return val
    return datetime.fromisoformat(str(val))


# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------

def tool_alarm_query(
    start_time: str,
    end_time: str,
    tag_names: list[str] | None = None,
    alarm_level: str | None = None,
    priority: str | None = None,
    state: str = "ANY",
    limit: int = 100,
) -> dict:
    start_dt = _parse_time(start_time)
    end_dt   = _parse_time(end_time)
    limit    = max(1, min(limit, 1000))

    where: list[str] = ["activated_at >= ? AND activated_at <= ?"]
    params: list     = [start_dt, end_dt]

    if tag_names:
        where.append(f"tag_name IN ({', '.join(['?'] * len(tag_names))})")
        params.extend(tag_names)
    if alarm_level:
        where.append("alarm_level = ?")
        params.append(alarm_level)
    if priority:
        where.append("priority = ?")
        params.append(priority)
    if state == "ACTIVE":
        where.append("cleared_at IS NULL")
    elif state == "CLEARED":
        where.append("cleared_at IS NOT NULL")
    elif state == "UNACKNOWLEDGED":
        where.append("acknowledged_at IS NULL")

    where_clause = " AND ".join(where)
    sql = f"""
        SELECT {', '.join(_ALARM_ROW_KEYS)}
        FROM alarm_events
        WHERE {where_clause}
        ORDER BY activated_at DESC
        LIMIT {limit}
    """
    con = get_alarm_connection()
    try:
        rows  = con.execute(sql, params).fetchall()
        total = con.execute(
            f"SELECT COUNT(*) FROM alarm_events WHERE {where_clause}", params
        ).fetchone()[0]
    finally:
        con.close()

    return {
        "start_time":      start_time,
        "end_time":        end_time,
        "total_matching":  total,
        "returned":        len(rows),
        "limit":           limit,
        "alarms":          _rows_to_dicts(rows),
    }


def tool_alarm_get_statistics(
    start_time: str,
    end_time: str,
    tag_names: list[str] | None = None,
) -> dict:
    start_dt = _parse_time(start_time)
    end_dt   = _parse_time(end_time)

    params_base: list = [start_dt, end_dt]
    tag_filter = ""
    if tag_names:
        tag_filter = f"AND tag_name IN ({', '.join(['?'] * len(tag_names))})"
        params_base.extend(tag_names)

    base_where = f"activated_at >= ? AND activated_at <= ? {tag_filter}"

    con = get_alarm_connection()
    try:
        total = con.execute(
            f"SELECT COUNT(*) FROM alarm_events WHERE {base_where}", params_base
        ).fetchone()[0]

        ack_count = con.execute(
            f"SELECT COUNT(*) FROM alarm_events WHERE {base_where} AND acknowledged_at IS NOT NULL",
            params_base,
        ).fetchone()[0]

        by_tag = con.execute(f"""
            SELECT tag_name,
                   COUNT(*)             AS alarm_count,
                   AVG(duration_sec) / 60.0 AS avg_duration_min,
                   MAX(duration_sec) / 60.0 AS max_duration_min
            FROM alarm_events
            WHERE {base_where}
            GROUP BY tag_name
            ORDER BY alarm_count DESC
        """, params_base).fetchall()

        by_level = con.execute(f"""
            SELECT alarm_level, COUNT(*) AS n
            FROM alarm_events WHERE {base_where}
            GROUP BY alarm_level ORDER BY n DESC
        """, params_base).fetchall()

        by_priority = con.execute(f"""
            SELECT priority, COUNT(*) AS n
            FROM alarm_events WHERE {base_where}
            GROUP BY priority ORDER BY n DESC
        """, params_base).fetchall()

        most_frequent = con.execute(f"""
            SELECT tag_name, alarm_level, COUNT(*) AS n
            FROM alarm_events WHERE {base_where}
            GROUP BY tag_name, alarm_level
            ORDER BY n DESC LIMIT 5
        """, params_base).fetchall()

    finally:
        con.close()

    return {
        "start_time":     start_time,
        "end_time":       end_time,
        "total_alarms":   total,
        "ack_rate":       round(ack_count / total, 3) if total else None,
        "by_tag": [
            {
                "tag_name":          r[0],
                "alarm_count":       r[1],
                "avg_duration_min":  round(r[2], 1) if r[2] is not None else None,
                "max_duration_min":  round(r[3], 1) if r[3] is not None else None,
            }
            for r in by_tag
        ],
        "by_level":    [{"alarm_level": r[0], "count": r[1]} for r in by_level],
        "by_priority": [{"priority": r[0], "count": r[1]} for r in by_priority],
        "most_frequent": [
            {"tag_name": r[0], "alarm_level": r[1], "count": r[2]}
            for r in most_frequent
        ],
    }


def tool_alarm_get_active_at(
    timestamp: str,
    tag_names: list[str] | None = None,
) -> dict:
    ts = _parse_time(timestamp)

    params: list = [ts, ts]
    tag_filter = ""
    if tag_names:
        tag_filter = f"AND tag_name IN ({', '.join(['?'] * len(tag_names))})"
        params.extend(tag_names)

    sql = f"""
        SELECT {', '.join(_ALARM_ROW_KEYS)}
        FROM alarm_events
        WHERE activated_at <= ?
          AND (cleared_at IS NULL OR cleared_at > ?)
          {tag_filter}
        ORDER BY priority DESC, activated_at DESC
    """
    con = get_alarm_connection()
    try:
        rows = con.execute(sql, params).fetchall()
    finally:
        con.close()

    return {
        "timestamp":           timestamp,
        "active_alarm_count":  len(rows),
        "active_alarms":       _rows_to_dicts(rows),
    }


def tool_alarm_search_context(
    timestamp: str,
    window_minutes: int = 30,
    tag_names: list[str] | None = None,
) -> dict:
    focal        = _parse_time(timestamp)
    window_start = focal - timedelta(minutes=window_minutes)
    window_end   = focal + timedelta(minutes=window_minutes)

    params: list = [window_start, window_end]
    tag_filter = ""
    if tag_names:
        tag_filter = f"AND tag_name IN ({', '.join(['?'] * len(tag_names))})"
        params.extend(tag_names)

    sql = f"""
        SELECT {', '.join(_ALARM_ROW_KEYS)}
        FROM alarm_events
        WHERE activated_at >= ? AND activated_at <= ?
          {tag_filter}
        ORDER BY activated_at
    """
    con = get_alarm_connection()
    try:
        rows = con.execute(sql, params).fetchall()
    finally:
        con.close()

    result_alarms = []
    for r in rows:
        d         = dict(zip(_ALARM_ROW_KEYS, r))
        activated = _to_dt(d["activated_at"])
        d["minutes_offset"] = round((activated - focal).total_seconds() / 60, 1)
        result_alarms.append(d)

    result_alarms.sort(key=lambda x: abs(x["minutes_offset"]))

    return {
        "focal_timestamp": timestamp,
        "window_minutes":  window_minutes,
        "window_start":    str(window_start),
        "window_end":      str(window_end),
        "alarm_count":     len(result_alarms),
        "alarms":          result_alarms,
    }


def tool_alarm_detect_flood(
    start_time: str,
    end_time: str,
    threshold_per_10min: int = 10,
) -> dict:
    start_dt = _parse_time(start_time)
    end_dt   = _parse_time(end_time)

    con = get_alarm_connection()
    try:
        rows = con.execute("""
            SELECT activated_at, tag_name
            FROM alarm_events
            WHERE activated_at >= ? AND activated_at <= ?
            ORDER BY activated_at
        """, [start_dt, end_dt]).fetchall()
    finally:
        con.close()

    if not rows:
        return {
            "start_time":           start_time,
            "end_time":             end_time,
            "threshold_per_10min":  threshold_per_10min,
            "flood_periods":        [],
            "total_flood_windows":  0,
        }

    window_sec = 600
    floods     = []
    i          = 0
    while i < len(rows):
        window_ts     = _to_dt(rows[i][0])
        window_end_ts = window_ts + timedelta(seconds=window_sec)

        bucket = [r for r in rows if _to_dt(r[0]) >= window_ts and _to_dt(r[0]) < window_end_ts]
        if len(bucket) >= threshold_per_10min:
            floods.append({
                "window_start":      str(window_ts),
                "window_end":        str(window_end_ts),
                "alarm_count":       len(bucket),
                "contributing_tags": sorted({r[1] for r in bucket}),
            })
            i += len(bucket)
        else:
            i += 1

    return {
        "start_time":           start_time,
        "end_time":             end_time,
        "threshold_per_10min":  threshold_per_10min,
        "total_flood_windows":  len(floods),
        "flood_periods":        floods,
    }
