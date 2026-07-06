---
doc_id: ds_primary_fan
doc_type: datasheet
equipment: [primary_fan]
tags: [FT_8301]
title: Equipment Datasheet — Primary Fan
revision: 1.2
date: 2020-08-01
---

# Equipment Datasheet — Primary Fan

**Document No.:** ZJP-DS-001  
**Equipment Tag:** YFJ1 (Unit 1 Primary Fan)  
**P&ID Reference:** P&ID-8300-001  
**Revision:** 1.2 | **Date:** 2020-08-01

---

## 1. Equipment Description

The Primary Fan supplies primary combustion air to the CFB furnace lower hearth. Its flow is measured by FT_8301. Primary air provides the fluidizing medium for the bed material and lower-zone combustion air. The split of primary vs. secondary air affects combustion staging, bed temperature distribution, and NOₓ emissions.

**System:** Primary Air System  
**Criticality:** High — loss of primary fan requires load reduction or shutdown

---

## 2. Design Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Chengda Fan Co., Ltd. |
| Model | G4-73-11 No. 20D |
| Fan Type | Centrifugal, single-inlet |
| Design Volume Flow | 155,000 m³/h |
| Design Static Pressure | +5,500 Pa (positive pressure, forced draft) |
| Fan Speed | Fixed — 980 RPM (coupled to motor direct) |
| Impeller Diameter | 2,000 mm |
| Inlet Temperature | Ambient (15–40°C typical) |
| Shaft Power at Design | 680 kW |
| Fan Efficiency at Design | 79% |

---

## 3. Drive and Motor

| Parameter | Value |
|-----------|-------|
| Motor Rating | 750 kW |
| Motor Voltage | 6,000 V |
| Motor Speed | 980 RPM |
| Flow Control | Outlet damper (modulating) — IGV optional upgrade |
| Normal Operating Range | 60–100% damper position |

---

## 4. Flow Measurement — FT_8301

| Parameter | Value |
|-----------|-------|
| Instrument Tag | FT_8301 |
| Description | Primary fan outlet flow rate |
| Measurement Type | Pitot tube / differential pressure |
| Full Scale | 160,000 m³/h |
| Normal Operating Range | 90,000–135,000 m³/h (full boiler load) |
| Low Alarm | 70,000 m³/h |
| Low-Low Alarm / Trip | 50,000 m³/h (minimum fluidization boundary) |
| Units | m³/h |

---

## 5. Operating Guidance

| Boiler Load | FT_8301 Target | Notes |
|-------------|---------------|-------|
| 100% (130 t/h steam) | 125,000–135,000 m³/h | Full fluidization |
| 75% | 100,000–115,000 m³/h | |
| 50% | 78,000–90,000 m³/h | |
| 40% (minimum) | 65,000–72,000 m³/h | Approaching minimum fluidization |

The primary-to-secondary air ratio is typically maintained at **60:40** at mid-load and shifts toward **55:45** at full load to improve combustion staging and reduce NOₓ.

---

## 6. Protection and Interlocks

| Interlock | Condition | Action |
|-----------|-----------|--------|
| Low-low flow | FT_8301 < 50,000 m³/h | Alarm — manual trip if persists |
| Motor overtemperature | Motor winding sensor > 140°C | Trip motor |
| Reverse rotation detected | Post-start check | Alarm and investigate |

---

## 7. Maintenance Schedule

| Task | Frequency | Procedure Reference |
|------|-----------|---------------------|
| Bearing check (vibration, heat) | Daily rounds | ZJP-SOP-006 |
| Damper actuator calibration | 6 months | ZJP-MNT-005 |
| Impeller inspection | Annual (outage) | ZJP-MNT-005 |
| Motor insulation resistance test | Annual | Electrical maintenance |

---

## 8. Revision History

| Rev | Date | Description |
|-----|------|-------------|
| 1.0 | 2019-03-01 | Initial issue |
| 1.2 | 2020-08-01 | Updated FT_8301 normal range based on actual operating data |
