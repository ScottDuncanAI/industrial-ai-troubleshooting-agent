---
doc_id: ds_secondary_fan
doc_type: datasheet
equipment: [secondary_fan]
tags: [FT_8302]
title: Equipment Datasheet — Secondary Fan
revision: 1.2
date: 2020-08-01
---

# Equipment Datasheet — Secondary Fan

**Document No.:** ZJP-DS-003  
**Equipment Tag:** YFJ2 (Unit 1 Secondary Fan)  
**P&ID Reference:** P&ID-8300-002  
**Revision:** 1.2 | **Date:** 2020-08-01

---

## 1. Equipment Description

The Secondary Fan supplies secondary combustion air to the upper furnace zone for staged combustion. Secondary air promotes burnout of volatile matter and CO above the dense bed zone, reducing emissions. Flow is measured by FT_8302. The primary-to-secondary ratio is coordinated by the combustion_air_control_loop.

**System:** Secondary Air System  
**Criticality:** High — loss of secondary fan requires firing rate reduction

---

## 2. Design Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Chengda Fan Co., Ltd. |
| Model | G4-73-11 No. 18D |
| Fan Type | Centrifugal, single-inlet |
| Design Volume Flow | 95,000 m³/h |
| Design Static Pressure | +4,800 Pa |
| Fan Speed | Fixed — 980 RPM |
| Impeller Diameter | 1,800 mm |
| Inlet Temperature | Ambient (15–40°C typical) |
| Shaft Power at Design | 380 kW |
| Motor Rating | 450 kW, 6,000 V |

---

## 3. Flow Measurement — FT_8302

| Parameter | Value |
|-----------|-------|
| Instrument Tag | FT_8302 |
| Description | Secondary fan outlet flow rate |
| Measurement Type | Pitot tube / differential pressure |
| Full Scale | 100,000 m³/h |
| Normal Operating Range | 55,000–80,000 m³/h (full boiler load) |
| Low Alarm | 40,000 m³/h |
| Low-Low Alarm | 25,000 m³/h |
| Units | m³/h |

---

## 4. Operating Guidance

Secondary air is injected at multiple elevation levels in the upper furnace to create staged combustion. The total combustion air split (FT_8301 + FT_8302) is adjusted by the O2 trim control loop (combustion_air_control_loop) to maintain the AIR_8301A/B oxygen target.

| Boiler Load | FT_8302 Target | PA:SA Ratio |
|-------------|---------------|-------------|
| 100% (130 t/h) | 72,000–80,000 m³/h | 55:45 |
| 75% | 58,000–68,000 m³/h | 60:40 |
| 50% | 44,000–54,000 m³/h | 60:40 |
| 40% (min) | 36,000–42,000 m³/h | 62:38 |

---

## 5. Protection and Interlocks

| Interlock | Condition | Action |
|-----------|-----------|--------|
| Low-low flow | FT_8302 < 25,000 m³/h with coal firing | Alarm |
| Motor overtemperature | Winding temp > 140°C | Trip |

---

## 6. Maintenance Schedule

| Task | Frequency | Procedure Reference |
|------|-----------|---------------------|
| Bearing and motor check | Daily rounds | ZJP-SOP-006 |
| Damper calibration | 6 months | ZJP-MNT-006 |
| Impeller inspection | Annual (outage) | ZJP-MNT-006 |

---

## 7. Revision History

| Rev | Date | Description |
|-----|------|-------------|
| 1.0 | 2019-03-01 | Initial issue |
| 1.2 | 2020-08-01 | Flow ranges updated from commissioning data |
