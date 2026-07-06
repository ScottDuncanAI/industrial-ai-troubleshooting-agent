---
doc_id: ds_upper_economizer
doc_type: datasheet
equipment: [economizer]
tags: [TE_8319A, TE_8319B, AIR_8301A, AIR_8301B]
title: Equipment Datasheet — Upper Economizer
revision: 1.2
date: 2020-08-01
---

# Equipment Datasheet — Upper Economizer

**Document No.:** ZJP-DS-007  
**Equipment Tag:** ECO-1  
**P&ID Reference:** P&ID-8300-009  
**Revision:** 1.2 | **Date:** 2020-08-01

---

## 1. Equipment Description

The Upper Economizer is a counterflow heat exchanger in the boiler backpass that recovers heat from flue gas to preheat boiler feedwater before it enters the steam drum. Preheating the feedwater reduces thermal shock to the drum and improves overall boiler efficiency. The O2 analyzers (AIR_8301A/B) are located at the economizer inlet to measure flue gas oxygen content — a key combustion control feedback signal. The economizer outlet flue gas temperature is measured by TE_8319A (left) and TE_8319B (right).

**System:** Flue Gas & Heat Recovery System  
**Criticality:** High — economizer fouling or tube failure impacts both efficiency and water chemistry

---

## 2. Design Specifications

| Parameter | Value |
|-----------|-------|
| Type | Counterflow, bare tube, multi-pass |
| Manufacturer | Jiangnan Boiler Co., Ltd. |
| Heat Transfer Area | 2,800 m² |
| Tube Material | SA-210C carbon steel |
| Tube OD / Wall Thickness | 38 mm / 4.5 mm |
| Feedwater Inlet Temperature | 105°C |
| Feedwater Outlet Temperature | 215°C |
| Feedwater Flow (Design) | 145 t/h |
| Feedwater Design Pressure | 12.5 MPa |
| Flue Gas Inlet Temperature | 380–430°C |
| Flue Gas Outlet Temperature (Design) | 145°C |
| Flue Gas Flow | 420,000 m³/h |
| Heat Duty | 22.5 MW |
| Effectiveness | 82% |

---

## 3. Instrumentation

### 3.1 Flue Gas O2 Analyzers (at Economizer Inlet)

| Sensor | Location | Normal Range | Low Alarm | High Alarm |
|--------|----------|-------------|-----------|------------|
| AIR_8301A | Left economizer inlet duct | 3.5–5.5% | 2.0% | 7.0% |
| AIR_8301B | Right economizer inlet duct | 3.5–5.5% | 2.0% | 7.0% |

These sensors provide the feedback signal for the combustion_air_control_loop. A low O2 reading indicates insufficient combustion air (risk of CO formation and incomplete combustion). A high O2 reading indicates excess air (reduced efficiency, increased fan power).

The left-right average (AIR_8301A + AIR_8301B)/2 is used as the control variable. A divergence > 1.5% between left and right may indicate uneven air distribution or a failed analyzer.

### 3.2 Economizer Outlet Flue Gas Temperature

| Sensor | Location | Normal Range | Low Alarm | High Alarm |
|--------|----------|-------------|-----------|------------|
| TE_8319A | Economizer outlet, left | 135–160°C | 110°C | 185°C |
| TE_8319B | Economizer outlet, right | 135–160°C | 110°C | 185°C |

TE_8319A/B are the primary indicators of economizer performance:
- **Rising trend:** Flue gas bypassing economizer (tube erosion/failure creating bypass, or flue gas short-circuiting)
- **High reading sustained:** Fouled economizer tubes, reduced heat transfer
- **Low reading:** Reduced boiler load, or feedwater flow higher than expected
- **Below 120°C:** Risk of acid dewpoint corrosion on economizer outlet tubes

---

## 4. Operating Guidance

| Condition | TE_8319 Reading | Action |
|-----------|----------------|--------|
| Normal | 135–160°C | No action |
| Slightly elevated | 160–175°C | Monitor; schedule sootblowing at next opportunity |
| High | > 175°C | Initiate sootblowing; if no improvement, plan outage inspection |
| Very high | > 185°C | Investigate tube bypass or severe fouling — consider derate |
| Near acid dew point | < 120°C | Increase boiler load if possible; reduce feedwater preheat |

---

## 5. Sootblowing

Retractable sootblowers are installed in the economizer section (3 elevations). Sootblower operation:
- **Normal frequency:** Every 12 hours at full load (coal ash can be adhesive)
- **Trigger criteria:** TE_8319A or TE_8319B rising > 15°C above baseline trend
- **Procedure:** Confirm steam pressure available; run sootblowers in sequence (bottom to top); monitor ΔP across economizer for improvement

---

## 6. Maintenance Schedule

| Task | Frequency | Reference |
|------|-----------|-----------|
| External tube inspection (visual, erosion probes) | Annual | ZJP-MNT-009 |
| Tube thickness UT check (selected tubes) | Annual | ZJP-MNT-009 |
| O2 analyzer calibration (AIR_8301A/B) | Monthly | Instrument maintenance |
| TE_8319A/B calibration | 6 months | Instrument maintenance |
| Economizer hydrotest (after tube repairs) | As needed | ZJP-MNT-009 |

---

## 7. Revision History

| Rev | Date | Description |
|-----|------|-------------|
| 1.0 | 2019-03-01 | Initial issue |
| 1.2 | 2020-08-01 | Added O2 analyzer divergence criterion; acid dew point guidance added |
