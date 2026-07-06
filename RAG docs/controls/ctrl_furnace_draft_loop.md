---
doc_id: ctrl_furnace_draft_loop
doc_type: controls
equipment: [induced_draft_fan, furnace_chamber]
tags: [PT_8313A, PT_8313B, PT_8313C, PT_8313D, PT_8313E, PT_8313F, YFJ3_AI]
title: Furnace Draft Control Loop — Description and Tuning
revision: 1.8
date: 2021-10-01
---

# Furnace Draft Control Loop

**Document No.:** ZJP-CTRL-002  
**Loop Name:** furnace_draft_control_loop  
**Revision:** 1.8 | **Date:** 2021-10-01

---

## 1. Loop Purpose

The furnace draft control loop maintains negative pressure in the upper furnace by controlling the speed of the Induced Draft Fan (IDF) via its Variable Frequency Drive (VFD). Negative furnace pressure (draft) is essential for safe operation — positive pressure causes hot gas and ash to escape from the furnace enclosure.

**Controlled Variable (PV):** Average of PT_8313A through PT_8313F (upper furnace pressure)  
**Setpoint (SP):** −120 Pa (adjustable range: −80 to −200 Pa)  
**Manipulated Variable (MV):** IDF VFD speed command (0–100%)  
**Feedback sensors:** PT_8313A, PT_8313B, PT_8313C, PT_8313D, PT_8313E, PT_8313F (six-point average)

---

## 2. Control Scheme

**Control type:** Single-loop PID  
**Action:** Direct acting — as furnace pressure rises (less negative), IDF speed increases.

**Averaging logic:** The six PT_8313 signals are averaged after rejection of outliers (any sensor more than 100 Pa from the median is excluded from the average). This provides robustness against single-sensor failures while maintaining accurate control.

**PID Parameters (Current Tuning):**

| Parameter | Value |
|-----------|-------|
| Proportional band | 50 Pa |
| Integral time (Ti) | 90 seconds |
| Derivative time (Td) | 15 seconds (small derivative to anticipate pressure spikes) |
| Output limits | 15–100% (IDF speed) |
| Minimum speed clamp | 15% (anti-surge protection) |
| Anti-windup | Enabled |

**Process response:** Furnace pressure responds very quickly to IDF speed changes (< 30 seconds). The tight control loop is appropriate here — rapid response prevents pressure excursions.

---

## 3. Pressure Measurement Voting Logic

The six sensors PT_8313A–F are also connected to the boiler protection system (BPS) with the following voting logic:

| Condition | Logic | Action |
|-----------|-------|--------|
| Any 2-of-6 sensors > +100 Pa | 2/6 vote | High pressure alarm |
| Any 2-of-6 sensors > +200 Pa | 2/6 vote | Boiler trip (puff protection) |
| Any 1-of-6 sensors failed | 1/6 | Alarm — exclude from control average; trip vote becomes 2/5 |

This 2-of-6 voting protects against false trips from a single faulty transmitter while ensuring that a genuine positive pressure event (which would affect multiple sensors) is detected.

---

## 4. Normal Operating Values

At full load (130 t/h):
- PT_8313A–F average: −110 to −130 Pa
- Spread between sensors: typically ±20 Pa (larger spread indicates combustion asymmetry or one faulty sensor)
- IDF VFD speed: typically 70–85%
- YFJ3_AI: 220–250 A

At minimum load (52 t/h):
- PT_8313A–F average: −80 to −100 Pa (less gas flow requires less draft)
- IDF VFD speed: 45–55%

**Setpoint adjustment guidance:**
- Increase draft setpoint (more negative, e.g., to −150 Pa) if fuel/air flows are unusually high — more conservative setting for high-output periods
- Decrease draft setpoint (less negative, e.g., to −80 Pa) if excessive draft is causing cold air infiltration through expansion joints

---

## 5. Disturbance Response

| Disturbance | Furnace Pressure Change | Loop Response |
|------------|------------------------|---------------|
| Load increase | Rises (less negative) | IDF speeds up |
| Coal feed spike | Rises transiently (more combustion gas) | IDF speeds up, then settles |
| Fan air flow surge | Rises sharply | IDF speeds up; may trigger alarm |
| Ash hopper drop (sudden solids fall) | Brief positive pulse | IDF responds, usually contained |

---

## 6. Manual Operation

If loop is transferred to manual:
- Hold IDF at current speed while investigating cause
- Manually adjust IDF speed in 5% increments to maintain pressure between −80 and −180 Pa
- Monitor all 6 PT_8313 sensors individually — do not rely on average when in manual
- Maximum safe furnace pressure in manual operation: −20 Pa (any closer to zero, reduce firing rate immediately)

---

## 7. Sensor Maintenance

PT_8313A–F impulse lines are 6 mm stainless steel tubing running from furnace wall taps to transmitters in the instrument room. These lines can:
- Plug with condensed ash if not heat-traced properly
- Freeze in winter (Zhejiang winters are mild — not typically an issue)
- Fill with water if not properly pitched

If a single transmitter reads anomalously: blow-through the impulse line with nitrogen before condemning the transmitter.

---

## 8. Related Documents
- ZJP-DS-012: Induced Draft Fan Datasheet
- ZJP-DS-005: CFB Furnace Datasheet (sensor elevation table)
- ZJP-TRB-003: High Furnace Pressure Troubleshooting
- ZJP-TRB-005: IDF High Vibration Troubleshooting
- ZJP-CTRL-004: Alarm Setpoint Register
