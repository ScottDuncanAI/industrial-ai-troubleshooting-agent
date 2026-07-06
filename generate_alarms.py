"""
Generate synthetic DCS alarm events from historian data.

Reads every 5-second row from boiler_historian.duckdb, runs each tag through
a simplified ISA-18.2 alarm state machine, and writes one row per alarm
lifecycle into boiler_alarms.duckdb.

Run once to create the alarm database:
    python generate_alarms.py

The output database (boiler_alarms.duckdb) is static â€” re-run only if the
historian data or alarm setpoints change.

State machine (per tag, per alarm level):
  NORMAL  â†’  ACTIVE  : process value crosses setpoint in alarm direction
  ACTIVE  â†’  NORMAL  : process value returns past setpoint + deadband
                        (deadband = max(1% of |setpoint|, 0.5 absolute units)
                        prevents chattering at the threshold boundary)

Each alarm lifecycle becomes one row with activation, acknowledgement
(simulated: 80% ack rate, 5â€“30 min random delay), and clearance timestamps.
"""

import os
import random
import duckdb
from datetime import datetime, timedelta

from alarm_metadata import ALARM_SETPOINTS, PRIORITY_MAP, ALARM_DIRECTION

random.seed(42)  # reproducible synthetic acks

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
HIST_DB  = os.path.join(PROJECT_DIR, "boiler_historian.duckdb")
ALARM_DB = os.path.join(PROJECT_DIR, "boiler_alarms.duckdb")

ACK_RATE        = 0.80   # fraction of alarms that get acknowledged
ACK_DELAY_MIN   = 5      # minutes
ACK_DELAY_MAX   = 30     # minutes
DEADBAND_PCT    = 0.01   # 1 % of |setpoint|
DEADBAND_ABS    = 0.5    # minimum absolute deadband units


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _deadband(setpoint: float) -> float:
    return max(abs(setpoint) * DEADBAND_PCT, DEADBAND_ABS)


def _alarm_message(tag: str, level: str, setpoint: float, value: float, units: str) -> str:
    meta = ALARM_SETPOINTS[tag]
    desc = meta.get("description", tag)
    direction = "above" if ALARM_DIRECTION[level] == "high" else "below"
    return (
        f"{desc} ({tag}) {level}: value {value:.2f} {units} "
        f"is {direction} setpoint {setpoint:.2f} {units}"
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print(f"Reading historian: {HIST_DB}")
    hist = duckdb.connect(HIST_DB, read_only=True)

    # Fetch all columns so we can index them by name
    rows = hist.execute("SELECT * FROM historian_data ORDER BY timestamp").fetchall()
    col_names = [d[0] for d in hist.description]
    col_index = {name: i for i, name in enumerate(col_names)}
    hist.close()
    print(f"  Loaded {len(rows):,} rows  ({col_names[0]}: {rows[0][0]} â†’ {rows[-1][0]})")

    # Build alarm events
    events: list[dict] = []
    alarm_id = 1

    for tag, setpoints in ALARM_SETPOINTS.items():
        if tag not in col_index:
            print(f"  WARNING: {tag} not found in historian columns, skipping")
            continue

        tag_col = col_index[tag]
        units   = setpoints.get("units", "")

        # Process each alarm level independently
        alarm_levels = {k: v for k, v in setpoints.items()
                        if k in ALARM_DIRECTION}

        for level, setpoint in alarm_levels.items():
            direction = ALARM_DIRECTION[level]
            priority  = PRIORITY_MAP[level]
            db        = _deadband(setpoint)

            state          = "NORMAL"
            activated_at   = None
            activated_val  = None
            max_dev        = 0.0

            for row in rows:
                ts  = row[col_index["timestamp"]]
                val = row[tag_col]
                if val is None:
                    continue

                if state == "NORMAL":
                    triggered = (direction == "high" and val > setpoint) or \
                                (direction == "low"  and val < setpoint)
                    if triggered:
                        state        = "ACTIVE"
                        activated_at  = ts
                        activated_val = val
                        max_dev       = abs(val - setpoint)

                else:  # ACTIVE
                    dev = abs(val - setpoint)
                    if dev > max_dev:
                        max_dev = dev

                    cleared = (direction == "high" and val < setpoint - db) or \
                              (direction == "low"  and val > setpoint + db)
                    if cleared:
                        duration = int((ts - activated_at).total_seconds())
                        ack_ts   = None
                        if random.random() < ACK_RATE:
                            ack_delay = random.uniform(ACK_DELAY_MIN, ACK_DELAY_MAX)
                            ack_ts    = activated_at + timedelta(minutes=ack_delay)
                            # Don't ack after clearance
                            if ack_ts > ts:
                                ack_ts = None

                        events.append({
                            "alarm_id":        alarm_id,
                            "tag_name":        tag,
                            "alarm_level":     level,
                            "priority":        priority,
                            "message":         _alarm_message(tag, level, setpoint,
                                                              activated_val, units),
                            "setpoint":        setpoint,
                            "activated_at":    activated_at,
                            "activated_value": round(activated_val, 4),
                            "acknowledged_at": ack_ts,
                            "cleared_at":      ts,
                            "duration_sec":    duration,
                            "max_deviation":   round(max_dev, 4),
                        })
                        alarm_id += 1
                        state    = "NORMAL"
                        max_dev  = 0.0

            # Alarm still active at end of dataset â€” record as open
            if state == "ACTIVE":
                ack_ts = None
                if random.random() < ACK_RATE:
                    ack_delay = random.uniform(ACK_DELAY_MIN, ACK_DELAY_MAX)
                    ack_ts    = activated_at + timedelta(minutes=ack_delay)

                events.append({
                    "alarm_id":        alarm_id,
                    "tag_name":        tag,
                    "alarm_level":     level,
                    "priority":        priority,
                    "message":         _alarm_message(tag, level, setpoint,
                                                      activated_val, units),
                    "setpoint":        setpoint,
                    "activated_at":    activated_at,
                    "activated_value": round(activated_val, 4),
                    "acknowledged_at": ack_ts,
                    "cleared_at":      None,   # still active
                    "duration_sec":    None,
                    "max_deviation":   round(max_dev, 4),
                })
                alarm_id += 1

        print(f"  {tag}: processed {len(alarm_levels)} level(s)")

    print(f"\nTotal alarm events generated: {len(events):,}")

    # -----------------------------------------------------------------------
    # Write to boiler_alarms.duckdb
    # -----------------------------------------------------------------------
    if os.path.exists(ALARM_DB):
        os.remove(ALARM_DB)
        print(f"Removed existing {ALARM_DB}")

    alm = duckdb.connect(ALARM_DB)
    alm.execute("""
        CREATE TABLE alarm_events (
            alarm_id        INTEGER PRIMARY KEY,
            tag_name        VARCHAR  NOT NULL,
            alarm_level     VARCHAR  NOT NULL,
            priority        VARCHAR  NOT NULL,
            message         VARCHAR  NOT NULL,
            setpoint        DOUBLE   NOT NULL,
            activated_at    TIMESTAMP NOT NULL,
            activated_value DOUBLE   NOT NULL,
            acknowledged_at TIMESTAMP,
            cleared_at      TIMESTAMP,
            duration_sec    INTEGER,
            max_deviation   DOUBLE   NOT NULL
        )
    """)

    # Batch insert
    alm.executemany("""
        INSERT INTO alarm_events VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
    """, [
        (
            e["alarm_id"],
            e["tag_name"],
            e["alarm_level"],
            e["priority"],
            e["message"],
            e["setpoint"],
            e["activated_at"],
            e["activated_value"],
            e["acknowledged_at"],
            e["cleared_at"],
            e["duration_sec"],
            e["max_deviation"],
        )
        for e in events
    ])

    # Summary stats
    total   = alm.execute("SELECT COUNT(*) FROM alarm_events").fetchone()[0]
    by_tag  = alm.execute("""
        SELECT tag_name, alarm_level, COUNT(*) as n
        FROM alarm_events GROUP BY 1, 2 ORDER BY 3 DESC LIMIT 15
    """).fetchall()
    by_pri  = alm.execute("""
        SELECT priority, COUNT(*) FROM alarm_events GROUP BY 1 ORDER BY 2 DESC
    """).fetchall()
    open_ct = alm.execute(
        "SELECT COUNT(*) FROM alarm_events WHERE cleared_at IS NULL"
    ).fetchone()[0]

    alm.close()

    print(f"\nDatabase written: {ALARM_DB}")
    print(f"  Total rows    : {total:,}")
    print(f"  Still active  : {open_ct:,}  (no cleared_at â€” active at dataset end)")
    print(f"\n  By priority:")
    for row in by_pri:
        print(f"    {row[0]:10s}: {row[1]:,}")
    print(f"\n  Top tag+level combinations:")
    for row in by_tag:
        print(f"    {row[0]:15s}  {row[1]:8s}  {row[2]:,}")


if __name__ == "__main__":
    main()

