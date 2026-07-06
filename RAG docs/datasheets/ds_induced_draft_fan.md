---
doc_id: ds_induced_draft_fan
doc_type: datasheet
equipment: [induced_draft_fan]
tags: [YFJ3_AI, YFJ3_ZD1, YFJ3_ZD2]
title: Equipment Datasheet — Induced Draft Fan
revision: 1.5
date: 2020-08-01
---

# Equipment Datasheet — Induced Draft Fan (IDF)

**Document No.:** ZJP-DS-012  
**Equipment Tag:** YFJ3 (Unit 1 Induced Draft Fan)  
**P&ID Reference:** P&ID-8300-005  
**Revision:** 1.5 | **Date:** 2020-08-01

---

## 1. Equipment Description

The Induced Draft (ID) Fan pulls combustion flue gas from the furnace exit, through the cyclone separators, economizer, and air preheaters, and discharges it through the stack to atmosphere. It is the primary device responsible for maintaining the furnace at negative pressure (induced draft). It is classified as **Critical** equipment — a trip of the IDF results in an immediate boiler trip.

---

## 2. Design Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Chengda Fan Co., Ltd. |
| Model | Y4-73-11 No. 24D |
| Fan Type | Centrifugal, double-inlet, single-stage |
| Design Volume Flow | 420,000 m³/h at operating conditions |
| Design Static Pressure | −2,800 Pa |
| Fan Speed | Variable — 600–985 RPM (via VFD) |
| Impeller Diameter | 2,400 mm |
| Inlet Temperature (Design) | 145°C |
| Shaft Power at Design Point | 1,680 kW |
| Fan Efficiency at Design Point | 82% |
| Weight (rotor assembly) | 8,200 kg |

---

## 3. Drive and Motor

| Parameter | Value |
|-----------|-------|
| Motor Manufacturer | SIEMENS / Local equivalent |
| Motor Rating | 1,800 kW |
| Motor Voltage | 6,000 V (6 kV) |
| Motor Speed | 985 RPM (4-pole) |
| Insulation Class | F |
| Protection Class | IP54 |
| Variable Frequency Drive | Yes — ABB ACS880 series |
| Normal Running Current (YFJ3_AI) | 180–250 A at full boiler load |
| High Current Alarm | 280 A |
| High-High Current Trip | 310 A |

---

## 4. Bearing Specifications

| Parameter | Value |
|-----------|-------|
| Bearing Type | Self-aligning spherical roller bearings |
| Drive-End Bearing | FAG 22340-E1-K (or equivalent) |
| Non-Drive-End Bearing | FAG 22336-E1-K (or equivalent) |
| Lubrication | Forced oil lubrication — circulating oil system |
| Oil Type | ISO VG 100 turbine oil |
| Oil Flow Rate | 12 L/min per bearing housing |
| Oil Temperature Normal | 45–65°C |
| Oil Temperature High Alarm | 75°C |
| Bearing Normal Temperature | < 70°C (housing) |
| Bearing High Alarm Temperature | 80°C |
| Bearing High-High Trip Temperature | 90°C |

---

## 5. Vibration Limits and Monitoring

Vibration is monitored continuously at two points on the bearing housings:

| Sensor | Location | Normal | Alert | Alarm | Trip |
|--------|----------|--------|-------|-------|------|
| YFJ3_ZD1 | Drive-end bearing shell, point A | < 2.5 mm/s | 3.5 mm/s | 4.5 mm/s | 11 mm/s |
| YFJ3_ZD2 | Non-drive-end bearing shell, point B | < 2.5 mm/s | 3.5 mm/s | 4.5 mm/s | 11 mm/s |

Vibration standard: **ISO 10816-3** (large industrial fans, Class III foundation)

**Common causes of elevated vibration:**
- Blade fouling / ash buildup on impeller blades
- Blade erosion (coal fly ash is abrasive)
- Bearing wear or lubrication failure
- Operating near surge line (low flow, high pressure)
- Foundation bolt looseness

---

## 6. Control and Protection

| Parameter | Value |
|-----------|-------|
| Control Mode | VFD speed control via DCS furnace_draft_control_loop |
| Feedback Signal | PT_8313A–F (furnace pressure average) |
| Draft Setpoint | −120 Pa (adjustable −80 to −200 Pa) |
| Inlet Damper | Motorized — 0–100% modulating |
| Anti-surge Control | Minimum speed limit 15% VFD command |
| Interlock — Trip IDF | High-high vibration (YFJ3_ZD1 or ZD2 > 11 mm/s) |
| Interlock — Trip IDF | Motor overcurrent (> 310 A) |
| Interlock — Trip IDF | Bearing high-high temperature (> 90°C) |
| Interlock — Trip Boiler | IDF running feedback lost |

---

## 7. Maintenance Schedule

| Task | Frequency | Procedure Reference |
|------|-----------|---------------------|
| Vibration check (local, walk-around) | Daily | ZJP-SOP-006 |
| Oil level check | Daily | ZJP-SOP-006 |
| Oil quality sample | Monthly | ZJP-MNT-003 |
| Blade erosion inspection (endoscope) | 6 months | ZJP-MNT-004 |
| Full bearing inspection and oil change | Annual (outage) | ZJP-MNT-003 |
| Impeller dynamic balancing | As needed (vibration > 3.5 mm/s sustained) | Vendor specialist |

---

## 8. Spare Parts (Recommended Stock)

| Part | Qty | Part Number |
|------|-----|-------------|
| Drive-end bearing | 1 | FAG 22340-E1-K |
| Non-drive-end bearing | 1 | FAG 22336-E1-K |
| Shaft seal assembly | 1 set | Vendor PN: CD-7304 |
| VFD cooling fan | 2 | ABB PN: 64178052 |
| Impeller blade set | 1 set | Vendor PN: CD-7298 |

---

## 9. Nozzle / Connection Schedule

| Connection | Size | Service |
|------------|------|---------|
| Flue gas inlet (×2, double inlet) | DN2400 | Flue gas from economizer |
| Flue gas outlet | DN1800 | Discharge to chimney |
| Oil supply/return | DN50 | Lubrication oil circuit |
| Cooling water supply/return | DN40 | Motor cooler (if water-cooled motor) |
| Drain | DN25 | Oil pan drain |

---

## 10. Revision History

| Rev | Date | Description |
|-----|------|-------------|
| 1.0 | 2019-03-01 | Initial issue |
| 1.3 | 2020-01-15 | Updated vibration trip setpoint from 7.1 to 11 mm/s per OEM recommendation post-commissioning |
| 1.5 | 2020-08-01 | Added YFJ3_AI alarm setpoints per actual motor performance data |
