---
doc_id: ds_steam_drum
doc_type: datasheet
equipment: [steam_drum]
tags: [PTCA_8322A]
title: Equipment Datasheet — Steam Drum
revision: 1.4
date: 2020-08-01
---

# Equipment Datasheet — Steam Drum

**Document No.:** ZJP-DS-008  
**Equipment Tag:** SD-1  
**P&ID Reference:** P&ID-8300-010  
**Revision:** 1.4 | **Date:** 2020-08-01

---

## 1. Equipment Description

The steam drum is the highest-pressure vessel in the boiler water-steam circuit. It receives preheated feedwater from the economizer, separates saturated steam from the water-steam mixture rising from the furnace water walls (downcomers/risers), and distributes dry saturated steam to the low-temperature superheater. The drum pressure (PTCA_8322A) is the primary indicator of boiler steam pressure. The drum is classified as a critical pressure vessel and is subject to mandatory inspection under Chinese Pressure Vessel Regulations (GB 150).

**System:** Steam Generation & Superheating System  
**Criticality:** Critical — vessel failure is catastrophic

---

## 2. Design Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Jiangnan Boiler Co., Ltd. |
| Design Code | GB 150 (Chinese Pressure Vessel Standard) |
| Shell Material | SA-516 Gr.70 (low-alloy, low-hydrogen) |
| Internal Diameter | 1,600 mm |
| Shell Length | 8,200 mm |
| Shell Thickness | 88 mm |
| Design Pressure | 11.27 MPa |
| Design Temperature | 317°C |
| Operating Pressure (Normal) | 9.8 MPa |
| Operating Temperature (Normal) | 311°C (saturation) |
| Hydrostatic Test Pressure | 16.9 MPa |
| Volume (total internal) | 16.5 m³ |
| Normal Water Volume | 8.2 m³ |

---

## 3. Pressure Monitoring — PTCA_8322A

| Parameter | Value |
|-----------|-------|
| Instrument Tag | PTCA_8322A |
| Description | Steam drum pressure (left side) |
| Measurement Type | Differential pressure transmitter (gauge) |
| Range | 0–12 MPa |
| Normal Operating Pressure | 9.4–10.0 MPa |
| High Alarm | 10.2 MPa |
| High-High Alarm | 10.5 MPa |
| Safety Valve Lift Set Pressure | 10.78 MPa (SV-1) and 10.88 MPa (SV-2) |
| High-High Trip (BPS) | 10.8 MPa |
| Units | kPa |

---

## 4. Safety Valves

Two spring-loaded safety valves are installed on the drum nozzle:

| Tag | Set Pressure | Capacity | Type |
|-----|-------------|---------|------|
| SV-1 | 10.78 MPa | 48 t/h | Full-lift, spring-loaded |
| SV-2 | 10.88 MPa | 48 t/h | Full-lift, spring-loaded |

Safety valves must not be gagged or blocked under any circumstances. Annual lift testing is mandatory.

---

## 5. Steam-Water Separation Internals

| Component | Specification |
|-----------|-------------|
| Primary separators | 24 × centrifugal (cyclone) steam separators |
| Secondary separators (dryer) | Chevron-type demister mesh, stainless steel |
| Steam dryness after drum | > 99.5% (design) |
| Allowable steam moisture carryover | < 0.5% by weight |

Excessive steam moisture carryover will contaminate the superheater and steam line with dissolved solids, causing deposition and potential tube failure. Signs of carryover: sodium in steam sample > 0.01 ppm, or unusual steam chemistry results.

---

## 6. Water Level Control

| Level | Indicator | Action |
|-------|-----------|--------|
| +150 mm (HH) | Drum level very high | Trip boiler (carryover risk) |
| +80 mm (H) | Drum level high | Reduce feedwater, investigate |
| Normal | −50 to +50 mm | No action |
| −80 mm (L) | Drum level low | Increase feedwater |
| −150 mm (LL) | Drum level very low | Trip boiler immediately (overheating risk) |

Level references are relative to drum centerline.

---

## 7. Inspection Requirements (Regulatory)

Per Chinese pressure vessel regulations, the steam drum requires:
- **Annual visual inspection** (external) — qualified boiler inspector
- **3-yearly internal inspection** — internal surfaces, nozzle welds, internals
- **6-yearly pressure test** — hydrostatic test or equivalent NDE

All inspection reports are filed with the plant safety department and relevant regulatory authority.

---

## 8. Maintenance Schedule

| Task | Frequency | Reference |
|------|-----------|-----------|
| Safety valve test (lift test) | Annual | ZJP-MNT-010 |
| Internal inspection | 3 years (or at each major outage) | ZJP-MNT-010 |
| PTCA_8322A calibration | 6 months | Instrument maintenance |
| Water level transmitter calibration | 6 months | Instrument maintenance |
| Chemical dosing connection check | 3 months | ZJP-CHEM-001 |

---

## 9. Revision History

| Rev | Date | Description |
|-----|------|-------------|
| 1.0 | 2019-03-01 | Initial issue |
| 1.2 | 2020-01-15 | Safety valve set pressures updated after re-stamping |
| 1.4 | 2020-08-01 | Level alarm setpoints revised, drum LL trip added |
