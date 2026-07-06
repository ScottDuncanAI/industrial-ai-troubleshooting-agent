---
doc_id: ds_desuperheater
doc_type: datasheet
equipment: [primary_desuperheater]
tags: [TV_8329ZC, YJJWSLL]
title: Equipment Datasheet — Primary Desuperheater
revision: 1.3
date: 2021-03-15
---

# Equipment Datasheet — Primary Desuperheater

**Document No.:** ZJP-DS-010  
**Equipment Tag:** DESUP-1  
**P&ID Reference:** P&ID-8300-012  
**Revision:** 1.3 | **Date:** 2021-03-15

---

## 1. Equipment Description

The Primary Desuperheater (also called the spray attemperator) is located between the Low Temperature Superheater outlet and the High Temperature Superheater inlet. It injects a controlled quantity of high-purity water (desuperheating water) into the steam to reduce its temperature. This provides the primary means of controlling final steam temperature (TE_8332A). The injection water flow is modulated by the temperature regulating valve TV_8329ZC, and the actual flow is measured by YJJWSLL.

The desuperheater is the actuator of the steam_temp_control_loop.

**System:** Steam Generation & Superheating System  
**Criticality:** High — loss of desuperheater control can cause TE_8332A to exceed limits

---

## 2. Design Specifications

| Parameter | Value |
|-----------|-------|
| Type | Internal spray (atomizing nozzle) |
| Manufacturer | Spirax Sarco / Local equivalent |
| Location | Steam header between LTSH and HTSH |
| Steam Inlet Temperature | 430°C (from LTSH) |
| Spray Water Temperature | 105°C (from economizer feedwater line) |
| Design Spray Water Flow | 0–12 t/h |
| Normal Operating Spray Flow | 2–8 t/h |
| Steam Outlet Temperature (target) | 510–520°C (entering HTSH) |
| Design Steam Pressure | 9.6 MPa |
| Nozzle Type | Full-cone, impingement type |
| Nozzle Quantity | 2 (one active, one spare) |
| Nozzle Material | 316 stainless steel |
| Downstream Minimum Straight Run | 5 m (required for complete evaporation before HTSH) |

---

## 3. Temperature Regulating Valve — TV_8329ZC

| Parameter | Value |
|-----------|-------|
| Instrument Tag | TV_8329ZC |
| Description | Desuperheater spray water regulating valve position |
| Valve Type | Globe valve, pneumatic actuator |
| Fail Position | Fail-closed (spring-to-close) |
| Control Signal | 4–20 mA from DCS steam_temp_control_loop |
| Travel | 0–100% (0% = closed, 100% = full open) |
| Normal Operating Position | 20–60% (at full load) |
| Cv at Full Open | 45 |
| High Position Alarm | > 85% sustained (indicates large cooling demand) |
| Low Position with High TE_8332A | < 5% with TE_8332A > 545°C — investigate valve fault |

---

## 4. Desuperheating Water Flow — YJJWSLL

| Parameter | Value |
|-----------|-------|
| Instrument Tag | YJJWSLL |
| Description | Primary desuperheating water flow output |
| Measurement Type | Vortex flowmeter |
| Range | 0–15 t/h |
| Normal Range | 2–8 t/h |
| High Flow Alarm | > 10 t/h |
| Zero Flow with TV_8329ZC Open | Indicates nozzle blockage or flow meter fault |
| Units | t/h |

---

## 5. Control Loop Integration

The desuperheater is controlled by the **steam_temp_control_loop**:
- **Feedback sensor:** TE_8332A (boiler outlet steam temperature)
- **Setpoint:** 540°C
- **Control action:** If TE_8332A > 540°C, open TV_8329ZC → increase YJJWSLL → cool steam entering HTSH → TE_8332A decreases
- **Proportional band:** 10°C (1% valve position per °C deviation)
- **Integral time:** 180 seconds

The loop is a cascade: the primary variable is TE_8332A; secondary validation uses YJJWSLL to confirm actual flow is tracking TV_8329ZC position.

---

## 6. Operating Cautions

1. **Minimum downstream evaporation length:** Water injected by the nozzle must fully evaporate before reaching the HTSH inlet. Incomplete evaporation causes water droplet impingement on HTSH tubes, leading to thermal fatigue cracking. Confirm the 5 m downstream straight run is unobstructed.

2. **Water quality:** Desuperheating water must meet boiler feedwater chemistry specifications (ZJP-CHEM-001). Using non-treated water will deposit solids on HTSH tube inner surfaces.

3. **Valve freeze-up:** If the boiler is tripped and steam pressure drops rapidly, the spray water line can cool and deposit scale in the nozzle. Flush the nozzle on restart per cold start procedure.

---

## 7. Maintenance Schedule

| Task | Frequency | Reference |
|------|-----------|-----------|
| TV_8329ZC valve travel calibration | 6 months | Instrument maintenance |
| Nozzle inspection and cleaning | Annual | ZJP-MNT-012 |
| YJJWSLL flow meter calibration | 6 months | Instrument maintenance |
| Downstream piping inspection for water deposition | Annual | ZJP-MNT-012 |

---

## 8. Revision History

| Rev | Date | Description |
|-----|------|-------------|
| 1.0 | 2019-03-01 | Initial issue |
| 1.2 | 2020-06-10 | Normal YJJWSLL range updated based on operating data |
| 1.3 | 2021-03-15 | Added downstream evaporation length caution after HTSH tube crack inspection finding |
