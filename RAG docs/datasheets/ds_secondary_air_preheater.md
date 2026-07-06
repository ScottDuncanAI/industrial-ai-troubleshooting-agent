---
doc_id: ds_secondary_air_preheater
doc_type: datasheet
equipment: [secondary_air_preheater]
tags: [TE_8304]
title: Equipment Datasheet — Secondary Air Preheater
revision: 1.1
date: 2020-08-01
---

# Equipment Datasheet — Secondary Air Preheater

**Document No.:** ZJP-DS-004  
**Equipment Tag:** KQYQ-2 (Unit 1 Secondary Air Preheater)  
**P&ID Reference:** P&ID-8300-003  
**Revision:** 1.1 | **Date:** 2020-08-01

---

## 1. Equipment Description

The Secondary Air Preheater recovers flue gas waste heat to preheat secondary combustion air before it enters the upper furnace. It is structurally identical to the primary air preheater but sized for the lower secondary air flow. Outlet air temperature is measured by TE_8304.

**System:** Secondary Air System / Flue Gas & Heat Recovery System  
**Criticality:** Medium

---

## 2. Design Specifications

| Parameter | Value |
|-----------|-------|
| Type | Tubular (shell-and-tube), counter-flow |
| Manufacturer | Jiangnan Boiler Co., Ltd. |
| Heat Transfer Area | 1,900 m² |
| Air Outlet Temperature (Design) | 200°C |
| Flue Gas Inlet Temperature (Design) | 280°C |
| Flue Gas Outlet Temperature (Design) | 145°C |
| Air Flow (Design) | 95,000 m³/h |
| Pressure Drop — Air Side | 650 Pa |
| Pressure Drop — Flue Gas Side | 300 Pa |
| Material (tubes) | Carbon steel, enamel-coated on cold end |

---

## 3. Temperature Monitoring — TE_8304

| Parameter | Value |
|-----------|-------|
| Instrument Tag | TE_8304 |
| Description | Secondary air preheater outlet air temperature |
| Measurement Type | Type K thermocouple |
| Normal Range | 175–215°C |
| Low Alarm | 145°C |
| High Alarm | 230°C |
| Units | °C |

---

## 4. Operating Guidance

TE_8303 (primary) and TE_8304 (secondary) should track each other closely (within 15°C) under normal conditions. A significant divergence between the two indicates:
- Fouling on the diverging unit's tube bundle
- Uneven flue gas distribution in the backpass
- Possible air leakage on one side

If TE_8304 − TE_8303 > 20°C or TE_8303 − TE_8304 > 20°C: inspect both preheaters for fouling and check for ductwork cross-leaks.

---

## 5. Maintenance Schedule

| Task | Frequency | Procedure Reference |
|------|-----------|---------------------|
| Tube inspection | Annual (outage) | ZJP-MNT-007 |
| External cleaning | 6 months (as needed) | ZJP-MNT-007 |
| TE_8304 calibration | 6 months | Instrument maintenance |

---

## 6. Revision History

| Rev | Date | Description |
|-----|------|-------------|
| 1.0 | 2019-03-01 | Initial issue |
| 1.1 | 2020-08-01 | Cross-reference to TE_8303 divergence criterion added |
