---
doc_id: ds_cfb_furnace
doc_type: datasheet
equipment: [furnace_lower_hearth, furnace_chamber]
tags: [PT_8313A, PT_8313B, PT_8313C, PT_8313D, PT_8313E, PT_8313F, TE_8313B, SXLTCYZ, SXLTCYY, FT_8306A, FT_8306B]
title: Equipment Datasheet — CFB Furnace (Lower Hearth and Upper Chamber)
revision: 2.0
date: 2020-10-15
---

# Equipment Datasheet — CFB Furnace

**Document No.:** ZJP-DS-005  
**Equipment Tags:** LH-1 (Lower Hearth), UC-1 (Upper Chamber)  
**P&ID Reference:** P&ID-8300-006, P&ID-8300-007  
**Revision:** 2.0 | **Date:** 2020-10-15

---

## 1. Equipment Description

The CFB furnace is the primary combustion vessel. Coal combustion occurs in a circulating fluidized bed — bed material (sand/ash) is fluidized by primary air, and combustion extends through the full furnace height. Hot gas and entrained solids exit the upper furnace to the cyclone separators; captured solids recirculate back to the lower hearth, giving the unit its characteristic "circulating" operation.

The furnace is divided operationally into two zones:
- **Lower Hearth / Bed Zone:** Dense phase bed, primary air injection, coal feed, solid returns
- **Upper Chamber:** Dilute phase zone, secondary air injection, final burnout, flue gas exit to cyclones

---

## 2. Furnace Design Specifications

| Parameter | Value |
|-----------|-------|
| Boiler Manufacturer | Jiangnan Boiler Co., Ltd. |
| Boiler Type | Circulating Fluidized Bed (CFB) |
| MCR Steam Output | 130 t/h |
| Steam Pressure (MCR) | 9.81 MPa |
| Steam Temperature (MCR) | 540°C |
| Furnace Height (total) | 28 m |
| Furnace Cross-Section | 9.5 m × 5.2 m |
| Refractory Type (lower 8 m) | Dense castable refractory, 200 mm thick |
| Membrane Wall Material | SA-210C carbon steel |
| Design Temperature (furnace exit gas) | 870°C |
| Design Pressure (internal) | −5,000 Pa to +3,000 Pa |
| Fuel | Bituminous coal, 25–30 MJ/kg HHV |
| Coal Feed Rate (MCR) | 22–26 t/h |
| Bed Material | Silica sand / recycled ash, 0.2–0.4 mm particle size |

---

## 3. Lower Hearth — Bed Zone

| Parameter | Value |
|-----------|-------|
| Height | 0–8 m from distributor plate |
| Primary Air Distribution | Nozzle grid plate (768 nozzles) |
| Minimum Fluidizing Velocity | 2.8 m/s (at 200°C air temperature) |
| Operating Superficial Velocity | 4.5–5.5 m/s |
| Bed Temperature (Normal) | 850–920°C |
| Bed Inventory (Normal ΔP) | 1,500–3,000 Pa |
| Coal Feed Points | 4 points (2 per side, front wall) |
| Solid Return Legs | 2 (left and right, from cyclone separators) |

### 3.1 Hearth Differential Pressure Sensors

| Sensor | Location | Normal Range | Low Alarm | High Alarm |
|--------|----------|-------------|-----------|------------|
| SXLTCYZ | Left side, upper-to-lower hearth ΔP | 1,500–3,000 Pa | < 800 Pa | > 4,000 Pa |
| SXLTCYY | Right side, upper-to-lower hearth ΔP | 1,500–3,000 Pa | < 800 Pa | > 4,000 Pa |

SXLTCYZ/Y indicate bed inventory. Values < 800 Pa indicate dangerously low bed inventory; values > 4,000 Pa indicate excessive solids accumulation (potential bed agglomeration).

### 3.2 Return Air Chambers

Return air chambers (left: FT_8306A, right: FT_8306B) seal the solid return legs and use recycled primary air to transport returned solids back to the furnace bed. Normal flow per chamber: 8,000–15,000 m³/h.

---

## 4. Upper Chamber — Furnace Chamber

| Parameter | Value |
|-----------|-------|
| Height | 8–28 m from distributor |
| Secondary Air Injection | 3 elevations — 8.5 m, 12 m, 16 m |
| Design Gas Exit Temperature | 870°C (to cyclone inlet) |
| Water Wall Cooling | Full height, evaporator circuit |

### 4.1 Furnace Pressure Monitoring

Six pressure transmitters are installed at the upper furnace to provide the furnace_draft_control_loop with redundant feedback:

| Sensor | Elevation | Normal Range | Alarm High | Trip (2-of-6) |
|--------|-----------|-------------|------------|---------------|
| PT_8313A | +22 m | −80 to −160 Pa | +100 Pa | +200 Pa |
| PT_8313B | +22 m | −80 to −160 Pa | +100 Pa | +200 Pa |
| PT_8313C | +18 m | −90 to −170 Pa | +100 Pa | +200 Pa |
| PT_8313D | +18 m | −90 to −170 Pa | +100 Pa | +200 Pa |
| PT_8313E | +14 m | −100 to −180 Pa | +100 Pa | +200 Pa |
| PT_8313F | +14 m | −100 to −180 Pa | +100 Pa | +200 Pa |

A furnace positive pressure trip requires **2-of-6** sensors to exceed the trip setpoint simultaneously.

### 4.2 Upper Furnace Temperature

| Sensor | Location | Normal Range | High Alarm |
|--------|----------|-------------|------------|
| TE_8313B | Upper furnace, right side wall, +24 m | 850–950°C | 980°C |

TE_8313B is used as an indicator of combustion intensity in the upper zone. Values above 980°C may indicate excessive firing rate or insufficient secondary air.

---

## 5. Refractory Specifications

| Zone | Refractory Type | Thickness | Expected Life |
|------|----------------|-----------|---------------|
| Lower hearth (0–3 m) | Dense castable, abrasion-resistant | 200 mm | 3–5 years |
| Lower hearth (3–8 m) | Dense castable, standard | 150 mm | 5–7 years |
| Upper chamber | Insulating castable | 75 mm | 8–12 years |

Refractory inspection is mandatory at every annual outage. Spalling or cracking that exposes membrane walls must be repaired before restart.

---

## 6. Maintenance Schedule

| Task | Frequency | Reference |
|------|-----------|-----------|
| Refractory visual inspection | Annual (outage) | ZJP-MNT-011 |
| Distributor nozzle inspection | Annual | ZJP-MNT-011 |
| Coal feed nozzle inspection | Annual | ZJP-MNT-011 |
| Pressure transmitter calibration (PT_8313A–F) | 6 months | Instrument maintenance |
| TE_8313B calibration | 6 months | Instrument maintenance |
| Furnace internal inspection (confined space) | Annual | ZJP-SAFE-004 |

---

## 7. Revision History

| Rev | Date | Description |
|-----|------|-------------|
| 1.0 | 2019-03-01 | Initial issue |
| 1.5 | 2020-03-10 | Updated bed inventory ΔP normal range based on operating experience |
| 2.0 | 2020-10-15 | Added furnace pressure trip logic (2-of-6) and PT_8313E/F added |
