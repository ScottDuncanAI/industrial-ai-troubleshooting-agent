---
doc_id: ds_steam_outlet
doc_type: datasheet
equipment: [steam_outlet]
tags: [TE_8332A, PTCA_8324, ZZQBCHLL]
title: Equipment Datasheet — Steam Outlet Header
revision: 1.1
date: 2020-08-01
---

# Equipment Datasheet — Steam Outlet Header and Measurement Station

**Document No.:** ZJP-DS-013  
**Equipment Tag:** SO-1  
**P&ID Reference:** P&ID-8300-014  
**Revision:** 1.1 | **Date:** 2020-08-01

---

## 1. Equipment Description

The steam outlet is the final measurement and isolation point before superheated steam leaves the boiler and enters the plant steam distribution header. Three instruments are located here: TE_8332A (temperature — the primary KPI), PTCA_8324 (pressure), and ZZQBCHLL (compensated steam flow). This is the handoff point between the boiler and the process plant.

**System:** Steam Generation & Superheating System  
**Criticality:** Critical — instrumentation here defines boiler performance

---

## 2. Outlet Steam Design Conditions

| Parameter | Value |
|-----------|-------|
| Design Steam Flow | 130 t/h (MCR) |
| Design Steam Pressure | 9.81 MPa |
| Design Steam Temperature | 540°C |
| Minimum Continuous Rating | 52 t/h |
| Main Steam Header Size | DN300, Schedule 80, SA-106 Gr.C |
| Main Steam Isolation Valve | Motor-operated gate valve, 12" class 1500 |

---

## 3. Steam Temperature — TE_8332A

See full specification in ZJP-DS-011 (High Temperature Superheater). Summary:

| Parameter | Value |
|-----------|-------|
| Tag | TE_8332A |
| Normal range | 530–545°C |
| High Alarm | 548°C |
| Low Alarm | 528°C |
| High-High Trip | 565°C |

---

## 4. Steam Pressure — PTCA_8324

| Parameter | Value |
|-----------|-------|
| Instrument Tag | PTCA_8324 |
| Description | Container outlet vapour pressure (main steam pressure) |
| Type | Pressure transmitter, gauge |
| Range | 0–12 MPa |
| Normal Operating Range | 9.4–10.0 MPa |
| High Alarm | 10.2 MPa |
| Low Alarm | 8.8 MPa |
| Units | kPa |

PTCA_8324 should track closely with PTCA_8322A (steam drum pressure) — the pressure drop across the superheater system is typically 0.2–0.4 MPa. A larger pressure drop indicates a flow restriction (blocked superheater drain, partial isolation valve closure, or tube blockage).

---

## 5. Main Steam Flow — ZZQBCHLL

| Parameter | Value |
|-----------|-------|
| Instrument Tag | ZZQBCHLL |
| Description | Main steam flow rate after compensation |
| Measurement Type | Orifice plate with DP transmitter; temperature and pressure compensated |
| Range | 0–160 t/h |
| Normal Operating Range | 120–135 t/h (full load) |
| Low Alarm | 100 t/h |
| High Alarm | 145 t/h |
| Units | t/h |

"After compensation" means the raw differential pressure measurement is corrected for actual steam density using the measured TE_8332A and PTCA_8324 values. This gives a mass flow rate that is accurate across the operating range.

---

## 6. Expected Relationships

At full load (130 t/h):
- TE_8332A: 530–545°C
- PTCA_8324: 9.5–9.9 MPa
- ZZQBCHLL: 125–135 t/h

A divergence in these three values (e.g., normal flow but low temperature) points toward control or heat transfer problems rather than measurement errors.

---

## 7. Maintenance Schedule

| Task | Frequency | Reference |
|------|-----------|-----------|
| ZZQBCHLL orifice inspection | Annual | Instrument maintenance |
| PTCA_8324 calibration | 6 months | Instrument maintenance |
| TE_8332A calibration and thermowell pull | Annual | Instrument maintenance |
| Main steam isolation valve exercise | 6 months | Mechanical maintenance |
