"""
Alarm setpoint definitions for all 30 historian tags.

Values are sourced directly from the Alarm and Trip Setpoint Register
(ctrl_alarm_setpoint_register, Rev 4.2, 2022-03-01).

IMPORTANT — unit alignment:
  PTCA_8322A and PTCA_8324 are stored in the historian as MPa
  (the DCS engineering range is 0–12 MPa); the alarm register quotes kPa.
  All setpoints here are expressed in the same units as the DB column,
  so PTCA values are divided by 1,000.
  All other tags use the units shown in the register directly.

Alarm direction:
  Hi / HiHi / HiHiHi / Alert / Alarm / Trip  →  triggered when value EXCEEDS setpoint
  Lo / LoLo                                   →  triggered when value FALLS BELOW setpoint
"""

# Priority tier for each alarm level name
PRIORITY_MAP: dict[str, str] = {
    "Trip":    "Critical",
    "HiHiHi":  "Critical",
    "LoLo":    "Critical",
    "HiHi":    "High",
    "Alarm":   "High",
    "Hi":      "Medium",
    "Lo":      "Medium",
    "Alert":   "Low",
}

# Direction each level fires in
ALARM_DIRECTION: dict[str, str] = {
    "Hi":      "high",
    "HiHi":    "high",
    "HiHiHi":  "high",
    "Alert":   "high",
    "Alarm":   "high",
    "Trip":    "high",
    "Lo":      "low",
    "LoLo":    "low",
}

# ---------------------------------------------------------------------------
# Main setpoint registry
# Key:   tag_name (str)
# Value: dict with any subset of Hi/HiHi/HiHiHi/Alert/Alarm/Trip/Lo/LoLo
#        plus 'description' and 'units' for human-readable messages.
# ---------------------------------------------------------------------------
ALARM_SETPOINTS: dict[str, dict] = {

    # ── Steam side ────────────────────────────────────────────────────────
    "TE_8332A": {
        "description": "Steam outlet temperature",
        "units": "°C",
        "Lo":      528.0,
        "Hi":      548.0,
        "HiHi":    558.0,
        "HiHiHi":  565.0,
    },
    "PTCA_8324": {
        "description": "Outlet steam pressure",
        "units": "MPa",
        # Register values in kPa ÷ 1000
        "LoLo":  8.4,
        "Lo":    8.8,
        "Hi":   10.2,
        "HiHi": 10.5,
    },
    "PTCA_8322A": {
        "description": "Steam drum pressure",
        "units": "MPa",
        "Lo":      8.8,
        "Hi":     10.2,
        "HiHi":   10.5,
        "HiHiHi": 10.8,
    },
    "ZZQBCHLL": {
        "description": "Main steam flow (compensated)",
        "units": "t/h",
        "Lo":   100.0,
        "Hi":   145.0,
    },
    "TV_8329ZC": {
        "description": "Desuperheater spray valve position",
        "units": "%",
        "Hi":    85.0,
    },
    "YJJWSLL": {
        "description": "Desuperheating water flow",
        "units": "t/h",
        "Hi":    10.0,
        "HiHi":  12.0,
    },

    # ── Combustion and furnace ────────────────────────────────────────────
    "PT_8313A": {
        "description": "Upper furnace pressure A",
        "units": "Pa",
        "Hi":   100.0,
        "HiHi": 200.0,
    },
    "PT_8313B": {
        "description": "Upper furnace pressure B",
        "units": "Pa",
        "Hi":   100.0,
        "HiHi": 200.0,
    },
    "PT_8313C": {
        "description": "Upper furnace pressure C",
        "units": "Pa",
        "Hi":   100.0,
        "HiHi": 200.0,
    },
    "PT_8313D": {
        "description": "Upper furnace pressure D",
        "units": "Pa",
        "Hi":   100.0,
        "HiHi": 200.0,
    },
    "PT_8313E": {
        "description": "Upper furnace pressure E",
        "units": "Pa",
        "Hi":   100.0,
        "HiHi": 200.0,
    },
    "PT_8313F": {
        "description": "Upper furnace pressure F",
        "units": "Pa",
        "Hi":   100.0,
        "HiHi": 200.0,
    },
    "TE_8313B": {
        "description": "Upper furnace temperature",
        "units": "°C",
        "Lo":    750.0,
        "Hi":    980.0,
        "HiHi": 1020.0,
    },
    "SXLTCYZ": {
        "description": "Hearth differential pressure (left)",
        "units": "Pa",
        "Lo":    800.0,
        "Hi":   4000.0,
    },
    "SXLTCYY": {
        "description": "Hearth differential pressure (right)",
        "units": "Pa",
        "Lo":    800.0,
        "Hi":   4000.0,
    },

    # ── Flue gas and O2 ───────────────────────────────────────────────────
    "AIR_8301A": {
        "description": "Flue gas O2 content (left)",
        "units": "%",
        "LoLo":  1.5,
        "Lo":    2.0,
        "Hi":    7.0,
    },
    "AIR_8301B": {
        "description": "Flue gas O2 content (right)",
        "units": "%",
        "LoLo":  1.5,
        "Lo":    2.0,
        "Hi":    7.0,
    },
    "TE_8319A": {
        "description": "Economizer flue gas outlet temperature (left)",
        "units": "°C",
        "Lo":    110.0,
        "Hi":    185.0,
        "HiHi":  210.0,
    },
    "TE_8319B": {
        "description": "Economizer flue gas outlet temperature (right)",
        "units": "°C",
        "Lo":    110.0,
        "Hi":    185.0,
        "HiHi":  210.0,
    },
    "ZCLCCY": {
        "description": "Cyclone separator differential pressure (left)",
        "units": "Pa",
        "Lo":    300.0,
        "Hi":   1800.0,
    },
    "YCLCCY": {
        "description": "Cyclone separator differential pressure (right)",
        "units": "Pa",
        "Lo":    300.0,
        "Hi":   1800.0,
    },

    # ── Air flows ─────────────────────────────────────────────────────────
    "FT_8301": {
        "description": "Primary fan outlet flow",
        "units": "m³/h",
        "LoLo": 50_000.0,
        "Lo":   70_000.0,
    },
    "FT_8302": {
        "description": "Secondary fan outlet flow",
        "units": "m³/h",
        "LoLo": 25_000.0,
        "Lo":   40_000.0,
    },
    "FT_8306A": {
        "description": "Return air chamber flow (left)",
        "units": "m³/h",
        "Lo":    5_000.0,
        "Hi":   20_000.0,
    },
    "FT_8306B": {
        "description": "Return air chamber flow (right)",
        "units": "m³/h",
        "Lo":    5_000.0,
        "Hi":   20_000.0,
    },

    # ── Air preheater temperatures ────────────────────────────────────────
    "TE_8303": {
        "description": "Primary air preheater outlet air temperature",
        "units": "°C",
        "Lo":   150.0,
        "Hi":   240.0,
    },
    "TE_8304": {
        "description": "Secondary air preheater outlet air temperature",
        "units": "°C",
        "Lo":   145.0,
        "Hi":   230.0,
    },

    # ── IDF (Induced Draft Fan) ───────────────────────────────────────────
    "YFJ3_ZD1": {
        "description": "IDF bearing vibration — drive end",
        "units": "mm/s",
        "Alert":  3.5,
        "Alarm":  4.5,
        "Trip":  11.0,
    },
    "YFJ3_ZD2": {
        "description": "IDF bearing vibration — non-drive end",
        "units": "mm/s",
        "Alert":  3.5,
        "Alarm":  4.5,
        "Trip":  11.0,
    },
    "YFJ3_AI": {
        "description": "IDF motor current",
        "units": "A",
        "Alarm": 280.0,
        "Trip":  310.0,
    },
}
