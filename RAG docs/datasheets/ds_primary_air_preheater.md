---
doc_id: ds_primary_air_preheater
doc_type: datasheet
equipment: [primary_air_preheater]
tags: [TE_8303]
title: Equipment Datasheet — Primary Air Preheater
revision: 1.1
date: 2020-08-01
---

# Equipment Datasheet — Primary Air Preheater

**Document No.:** ZJP-DS-002  
**Equipment Tag:** KQYQ-1 (Unit 1 Primary Air Preheater)  
**P&ID Reference:** P&ID-8300-003  
**Revision:** 1.1 | **Date:** 2020-08-01

---

## 1. Equipment Description

The Primary Air Preheater is a tubular heat exchanger that recovers waste heat from flue gas to preheat primary combustion air before it enters the furnace lower hearth. Preheating the combustion air improves furnace efficiency and reduces coal consumption. The outlet air temperature is measured by TE_8303.

**System:** Primary Air System / Flue Gas & Heat Recovery System  
**Criticality:** Medium — degradation reduces efficiency; failure requires derating

---

## 2. Design Specifications

| Parameter | Value |
|-----------|-------|
| Type | Tubular (shell-and-tube), counter-flow |
| Manufacturer | Jiangnan Boiler Co., Ltd. |
| Heat Transfer Area | 3,200 m² |
| Air-Side Design Pressure | +6,000 Pa |
| Flue Gas-Side Design Pressure | −3,000 Pa |
| Air Inlet Temperature | 20°C (ambient) |
| Air Outlet Temperature (Design) | 210°C |
| Flue Gas Inlet Temperature (Design) | 320°C |
| Flue Gas Outlet Temperature (Design) | 145°C |
| Air Flow (Design) | 155,000 m³/h |
| Pressure Drop — Air Side | 800 Pa |
| Pressure Drop — Flue Gas Side | 400 Pa |
| Material (tubes) | Carbon steel, enamel-coated on cold end |
| Material (casing) | Carbon steel with refractory lining at hot end |

---

## 3. Temperature Monitoring — TE_8303

| Parameter | Value |
|-----------|-------|
| Instrument Tag | TE_8303 |
| Description | Primary air preheater outlet air temperature |
| Measurement Type | Type K thermocouple |
| Normal Range | 180–220°C |
| Low Alarm | 150°C (indicates fouling or flue gas temp drop) |
| High Alarm | 240°C (investigate flue gas temperature) |
| Units | °C |

---

## 4. Operating Guidance

| Condition | Indication | Action |
|-----------|-----------|--------|
| TE_8303 low (< 160°C) | Fouled tubes, reduced flue gas flow, flue gas temp drop | Schedule cleaning (ZJP-MNT-007) |
| TE_8303 high (> 235°C) | Flue gas temperature abnormally high, possible sootblowing needed | Investigate upstream heat transfer |
| Air-side ΔP increasing over time | Tube fouling from fly ash | Clean during next outage |
| Corrosion on cold end | Cold end below acid dew point | Increase air inlet temperature if possible |

**Acid Dew Point Note:** When burning coal with > 1.5% sulfur content, the flue gas sulfuric acid dew point may be 120–140°C. The cold-end tubes are enamel-coated to resist acid corrosion. If outlet flue gas temperature drops below 130°C, acid corrosion rate increases significantly.

---

## 5. Maintenance Schedule

| Task | Frequency | Procedure Reference |
|------|-----------|---------------------|
| Tube blockage inspection | Annual (outage) | ZJP-MNT-007 |
| Air preheater external cleaning | 6 months (as needed) | ZJP-MNT-007 |
| Cold-end enamel coating inspection | Annual | ZJP-MNT-007 |
| TE_8303 calibration verification | 6 months | Instrument maintenance |

---

## 6. Revision History

| Rev | Date | Description |
|-----|------|-------------|
| 1.0 | 2019-03-01 | Initial issue |
| 1.1 | 2020-08-01 | Added acid dew point note based on coal quality data |
