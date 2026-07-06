# Tag metadata for the boiler historian simulator
# Source: Research paper "A long-tailed distribution time-series dataset in..."
# Dataset: Coal-fired boiler at a chemical plant in Zhejiang, China
# Collection period: 2022-03-27 14:28:54 to 2022-04-01 14:28:49 (5-second intervals)

TAG_METADATA = {
    # --- Furnace Pressure Transmitters ---
    "PT_8313A": {
        "description": "Upper furnace pressure (point A)",
        "units": "kPa",
        "sensor_type": "Pressure",
        "normal_min": None,
        "normal_max": None,
    },
    "PT_8313B": {
        "description": "Upper furnace pressure (point B)",
        "units": "kPa",
        "sensor_type": "Pressure",
        "normal_min": None,
        "normal_max": None,
    },
    "PT_8313C": {
        "description": "Upper furnace pressure (point C)",
        "units": "kPa",
        "sensor_type": "Pressure",
        "normal_min": None,
        "normal_max": None,
    },
    "PT_8313D": {
        "description": "Upper furnace pressure (point D)",
        "units": "kPa",
        "sensor_type": "Pressure",
        "normal_min": None,
        "normal_max": None,
    },
    "PT_8313E": {
        "description": "Upper furnace pressure (point E)",
        "units": "kPa",
        "sensor_type": "Pressure",
        "normal_min": None,
        "normal_max": None,
    },
    "PT_8313F": {
        "description": "Upper furnace pressure (point F)",
        "units": "kPa",
        "sensor_type": "Pressure",
        "normal_min": None,
        "normal_max": None,
    },
    # --- Steam / Container Pressure ---
    "PTCA_8322A": {
        "description": "Pot pressure (left side steam drum pressure)",
        "units": "kPa",
        "sensor_type": "Pressure",
        "normal_min": None,
        "normal_max": None,
    },
    "PTCA_8324": {
        "description": "Container outlet vapour pressure",
        "units": "kPa",
        "sensor_type": "Pressure",
        "normal_min": None,
        "normal_max": None,
    },
    # --- Temperature Sensors ---
    "TE_8319A": {
        "description": "Flue gas temperature at upper economizer outlet (left)",
        "units": "°C",
        "sensor_type": "Temperature",
        "normal_min": None,
        "normal_max": None,
    },
    "TE_8319B": {
        "description": "Flue gas temperature at upper economizer outlet (right)",
        "units": "°C",
        "sensor_type": "Temperature",
        "normal_min": None,
        "normal_max": None,
    },
    "TE_8313B": {
        "description": "Temperature in upper part of furnace chamber (right side)",
        "units": "°C",
        "sensor_type": "Temperature",
        "normal_min": None,
        "normal_max": None,
    },
    "TE_8303": {
        "description": "Primary air preheater outlet air temperature",
        "units": "°C",
        "sensor_type": "Temperature",
        "normal_min": None,
        "normal_max": None,
    },
    "TE_8304": {
        "description": "Secondary air preheater outlet air temperature",
        "units": "°C",
        "sensor_type": "Temperature",
        "normal_min": None,
        "normal_max": None,
    },
    "TE_8332A": {
        "description": "Boiler outlet steam temperature (primary KPI — normal 530–545°C)",
        "units": "°C",
        "sensor_type": "Temperature",
        "normal_min": 530.0,
        "normal_max": 545.0,
    },
    # --- Valve Position ---
    "TV_8329ZC": {
        "description": "Primary desuperheater outlet steam temperature regulating valve position",
        "units": "%",
        "sensor_type": "Valve",
        "normal_min": None,
        "normal_max": None,
    },
    # --- Fan Flow Transmitters ---
    "FT_8301": {
        "description": "Primary fan outlet flow rate",
        "units": "m³/h",
        "sensor_type": "Flow",
        "normal_min": None,
        "normal_max": None,
    },
    "FT_8302": {
        "description": "Secondary fan outlet flow rate",
        "units": "m³/h",
        "sensor_type": "Flow",
        "normal_min": None,
        "normal_max": None,
    },
    "FT_8306A": {
        "description": "Return air chamber air flow (left)",
        "units": "m³/h",
        "sensor_type": "Flow",
        "normal_min": None,
        "normal_max": None,
    },
    "FT_8306B": {
        "description": "Return air chamber air flow (right)",
        "units": "m³/h",
        "sensor_type": "Flow",
        "normal_min": None,
        "normal_max": None,
    },
    # --- Flue Gas Oxygen Sensors ---
    "AIR_8301A": {
        "description": "Upper economizer inlet flue gas oxygen content (left)",
        "units": "%",
        "sensor_type": "Oxygen",
        "normal_min": None,
        "normal_max": None,
    },
    "AIR_8301B": {
        "description": "Upper economizer inlet flue gas oxygen content (right)",
        "units": "%",
        "sensor_type": "Oxygen",
        "normal_min": None,
        "normal_max": None,
    },
    # --- Induced Draft Fan (Motor / Vibration) ---
    "YFJ3_AI": {
        "description": "Induced draft fan motor current",
        "units": "A",
        "sensor_type": "Motor",
        "normal_min": None,
        "normal_max": None,
    },
    "YFJ3_ZD1": {
        "description": "Vibration of induced draft fan bearing shell (point A)",
        "units": "mm/s",
        "sensor_type": "Vibration",
        "normal_min": None,
        "normal_max": None,
    },
    "YFJ3_ZD2": {
        "description": "Vibration of induced draft fan bearing shell (point B)",
        "units": "mm/s",
        "sensor_type": "Vibration",
        "normal_min": None,
        "normal_max": None,
    },
    # --- Differential Pressure Sensors (hearth) ---
    "SXLTCYZ": {
        "description": "Differential pressure between upper and lower hearth (left)",
        "units": "Pa",
        "sensor_type": "Differential Pressure",
        "normal_min": None,
        "normal_max": None,
    },
    "SXLTCYY": {
        "description": "Differential pressure between upper and lower hearth (right)",
        "units": "Pa",
        "sensor_type": "Differential Pressure",
        "normal_min": None,
        "normal_max": None,
    },
    "ZCLCCY": {
        "description": "Differential pressure in the left layer (cyclone separator)",
        "units": "Pa",
        "sensor_type": "Differential Pressure",
        "normal_min": None,
        "normal_max": None,
    },
    "YCLCCY": {
        "description": "Differential pressure in the right layer (cyclone separator)",
        "units": "Pa",
        "sensor_type": "Differential Pressure",
        "normal_min": None,
        "normal_max": None,
    },
    # --- Steam / Water Flow ---
    "YJJWSLL": {
        "description": "Primary desuperheating water flow output",
        "units": "t/h",
        "sensor_type": "Flow",
        "normal_min": None,
        "normal_max": None,
    },
    "ZZQBCHLL": {
        "description": "Main steam flow rate after compensation",
        "units": "t/h",
        "sensor_type": "Flow",
        "normal_min": None,
        "normal_max": None,
    },
}

# Convenience groupings for natural language matching
SENSOR_TYPE_GROUPS = {
    "temperature": [k for k, v in TAG_METADATA.items() if v["sensor_type"] == "Temperature"],
    "pressure": [k for k, v in TAG_METADATA.items() if v["sensor_type"] == "Pressure"],
    "flow": [k for k, v in TAG_METADATA.items() if v["sensor_type"] == "Flow"],
    "oxygen": [k for k, v in TAG_METADATA.items() if v["sensor_type"] == "Oxygen"],
    "vibration": [k for k, v in TAG_METADATA.items() if v["sensor_type"] == "Vibration"],
    "differential_pressure": [k for k, v in TAG_METADATA.items() if v["sensor_type"] == "Differential Pressure"],
    "motor": [k for k, v in TAG_METADATA.items() if v["sensor_type"] == "Motor"],
    "valve": [k for k, v in TAG_METADATA.items() if v["sensor_type"] == "Valve"],
}
