---
doc_id: ds_cyclone_separator
doc_type: datasheet
equipment: [cyclone_separator_left, cyclone_separator_right]
tags: [ZCLCCY, YCLCCY]
title: Equipment Datasheet — Cyclone Separators (Left and Right)
revision: 1.3
date: 2020-08-01
---

# Equipment Datasheet — Cyclone Separators (Left and Right)

**Document No.:** ZJP-DS-006  
**Equipment Tags:** CS-L (Left Cyclone), CS-R (Right Cyclone)  
**P&ID Reference:** P&ID-8300-008  
**Revision:** 1.3 | **Date:** 2020-08-01

---

## 1. Equipment Description

Two cyclone separators are installed in parallel — one on each side of the furnace. They receive hot flue gas and entrained solid particles from the upper furnace. Centrifugal action separates the solids from the gas: solids fall to the bottom and are returned to the furnace via the solid return legs (the "circulating" loop), while cleaned flue gas exits through the cyclone vortex finder to the economizer backpass. The cyclones are the defining component of CFB technology.

**System:** Flue Gas & Heat Recovery System  
**Criticality:** High — loss of cyclone efficiency causes increased fly ash carry-over and loss of bed inventory

---

## 2. Design Specifications (Each Cyclone)

| Parameter | Value |
|-----------|-------|
| Manufacturer | Jiangnan Boiler Co., Ltd. |
| Type | High-efficiency tangential-entry cyclone |
| Number of Units | 2 (left and right, symmetric) |
| Inlet Gas Flow | 210,000 m³/h each (at operating conditions) |
| Inlet Gas Temperature | 850–900°C |
| Inlet Solids Loading | 5–15 kg/kg gas |
| Separation Efficiency | > 99.5% (for particles > 100 μm) |
| Cyclone Body Diameter | 4,800 mm |
| Cyclone Height (total) | 18 m |
| Vortex Finder Diameter | 2,000 mm |
| Pressure Drop (Design) | 800–1,400 Pa |
| Refractory Lining | 150 mm dense castable (inner surface) |
| Gas Outlet Temperature | 840–890°C (to economizer inlet) |

---

## 3. Differential Pressure Monitoring

Differential pressure across each cyclone is the primary indicator of solid separation rate and flow conditions:

| Sensor | Equipment | Normal Range | Low Alarm | High Alarm |
|--------|-----------|-------------|-----------|------------|
| ZCLCCY | Left cyclone | 600–1,200 Pa | < 300 Pa | > 1,800 Pa |
| YCLCCY | Right cyclone | 600–1,200 Pa | < 300 Pa | > 1,800 Pa |

**Interpretation:**
| ZCLCCY / YCLCCY Reading | Likely Cause |
|-------------------------|-------------|
| Both low (< 300 Pa) | Low gas velocity (low load), or blockage in solid return leg, or bed inventory loss |
| Both high (> 1,800 Pa) | Excessive solids loading, possible partial blockage in vortex finder |
| Left-right divergence > 400 Pa | Uneven gas flow distribution, one cyclone partially blocked |

---

## 4. Solid Return Leg (L-Seal) Operation

Each cyclone has a solid return leg (sometimes called an L-seal or loop seal) that returns captured solids to the lower hearth. These seals are fluidized with return air measured by FT_8306A (left) and FT_8306B (right).

| Parameter | Normal Value |
|-----------|-------------|
| Return air flow (each) | 8,000–15,000 m³/h |
| Seal temperature | 800–870°C |
| Solid return rate (estimated) | 10–25 t/h per leg |

A blocked return leg will cause rapid bed inventory loss (SXLTCYZ/Y dropping) and rising cyclone ΔP. An air-locked or empty return leg will cause ZCLCCY or YCLCCY to drop abruptly.

---

## 5. Refractory

Cyclone refractory is subject to severe abrasion from high-velocity solids and thermal cycling.

| Zone | Type | Thickness | Expected Life |
|------|------|-----------|---------------|
| Inlet duct | High-alumina abrasion-resistant castable | 200 mm | 3–5 years |
| Cyclone body (inner) | Dense abrasion-resistant castable | 150 mm | 4–6 years |
| Vortex finder | High-chrome castable | 100 mm | 2–4 years |

The vortex finder is the highest wear component — inspect first at every annual outage.

---

## 6. Maintenance Schedule

| Task | Frequency | Reference |
|------|-----------|-----------|
| Refractory inspection (endoscope or visual via access port) | Annual | ZJP-MNT-008 |
| Return leg inspection | Annual | ZJP-MNT-008 |
| ZCLCCY / YCLCCY transmitter calibration | 6 months | Instrument maintenance |
| Vortex finder erosion measurement | Annual | ZJP-MNT-008 |

---

## 7. Revision History

| Rev | Date | Description |
|-----|------|-------------|
| 1.0 | 2019-03-01 | Initial issue |
| 1.2 | 2020-01-10 | Vortex finder inspection interval reduced from 18 months to 12 months after erosion found during first outage |
| 1.3 | 2020-08-01 | Added divergence criterion (> 400 Pa L-R difference) |
