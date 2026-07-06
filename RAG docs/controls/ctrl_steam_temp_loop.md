---
doc_id: ctrl_steam_temp_loop
doc_type: controls
equipment: [primary_desuperheater, high_temp_superheater, steam_outlet]
tags: [TE_8332A, TV_8329ZC, YJJWSLL]
title: Steam Temperature Control Loop — Description and Tuning
revision: 2.1
date: 2021-10-01
---

# Steam Temperature Control Loop

**Document No.:** ZJP-CTRL-001  
**Loop Name:** steam_temp_control_loop  
**Revision:** 2.1 | **Date:** 2021-10-01

---

## 1. Loop Purpose

The steam temperature control loop maintains the boiler outlet steam temperature (TE_8332A) at the setpoint of 540°C by modulating the desuperheating water spray valve (TV_8329ZC), thereby controlling the water flow (YJJWSLL) injected into the steam path between the Low Temperature Superheater and the High Temperature Superheater.

**Controlled Variable (PV):** TE_8332A — Boiler outlet steam temperature  
**Setpoint (SP):** 540°C  
**Manipulated Variable (MV):** TV_8329ZC position (0–100%)  
**Secondary confirmation:** YJJWSLL (desuperheating water flow, t/h)  
**Operating range:** TE_8332A = 530–545°C (normal band); control acts to hold 540°C

---

## 2. Control Scheme

**Control type:** Single-loop PID  
**Action:** Reverse acting — as TE_8332A increases above setpoint, TV_8329ZC opens (more spray water cools steam).

**PID Parameters (Current Tuning):**

| Parameter | Value | Notes |
|-----------|-------|-------|
| Proportional band | 10°C | 1% valve movement per °C deviation |
| Integral time (Ti) | 180 seconds | Corrects steady-state offset |
| Derivative time (Td) | 0 seconds | Derivative not used (noisy signal) |
| Output limits | 0–100% (TV_8329ZC) | |
| Anti-windup | Enabled (output clamp) | |
| Fail-safe mode | Manual hold at last position | On DCS failure |

**Process dead time:** Approximately 3–5 minutes from TV_8329ZC change to TE_8332A response (steam transit time from desuperheater to outlet).

---

## 3. Normal Operating Behavior

At steady full load (130 t/h):
- TE_8332A: ~540°C ± 3°C
- TV_8329ZC: 30–50% open
- YJJWSLL: 3–6 t/h
- Control loop deviation (TE_8332A − SP): ± 2°C, returning to zero within 8 minutes of any disturbance

**Expected disturbances and responses:**

| Disturbance | TV_8329ZC Response | Recovery Time |
|------------|-------------------|---------------|
| Load increase (+10 t/h ZZQBCHLL) | Brief close (temperature dips, then recovers) | 10–15 min |
| Load decrease (−10 t/h ZZQBCHLL) | Opens more (temperature rises, spray increases) | 8–12 min |
| Combustion intensity increase | Opens more | 5–8 min |
| Coal quality change (higher CV) | Opens more | 5–10 min |

---

## 4. Alarm Setpoints Related to This Loop

| Tag | Condition | Setpoint | Action |
|-----|-----------|---------|--------|
| TE_8332A | High | 548°C | Alarm |
| TE_8332A | High-High | 558°C | Alarm + manual action required |
| TE_8332A | High-High-High (BPS) | 565°C | Automatic boiler trip |
| TE_8332A | Low | 528°C | Alarm |
| TV_8329ZC | High position | > 85% sustained | Alarm (large cooling demand — investigate) |
| YJJWSLL | High flow | > 10 t/h | Alarm |

---

## 5. Control Loop Modes

| Mode | When Used | Who Sets |
|------|-----------|---------|
| Automatic | Normal steady operation | Standard — default |
| Manual | Startup, shutdown, maintenance, loop malfunction | Operator |
| Cascade | Not installed in current configuration | — |

**To switch to manual:** Hold TV_8329ZC at current output before transferring — prevents bump.  
**To transfer back to automatic:** Confirm TE_8332A is within 5°C of setpoint before engaging auto — prevents integrator windup on transfer.

---

## 6. Tuning History

| Date | Previous Ti | New Ti | Reason |
|------|-------------|--------|--------|
| 2019-08 (commissioning) | 120 s | 120 s | Initial commissioning |
| 2020-04 | 120 s | 180 s | Oscillation observed — increased Ti to reduce frequency |
| 2021-03 | 180 s | 180 s | No change — review after desuperheater nozzle inspection |

If TE_8332A oscillation (cycling) is observed with amplitude > 5°C:
1. First check: is the process disturbed (load changing, coal quality varying)? If yes, not a tuning issue
2. If sustained oscillation with stable process: increase Ti to 240 s
3. If sluggish response (large TE_8332A error persisting > 30 min): reduce Ti to 150 s

---

## 7. Interlock with BPS

The steam_temp_control_loop receives a signal from the boiler protection system (BPS). On boiler trip:
- TV_8329ZC commanded to CLOSED immediately (fail-close, spring-to-close)
- Loop transferred to MANUAL automatically
- Must be manually returned to automatic after restart

---

## 8. Related Documents
- ZJP-DS-010: Desuperheater Datasheet
- ZJP-DS-011: High Temperature Superheater Datasheet
- ZJP-TRB-001: High Steam Temperature Troubleshooting
- ZJP-TRB-002: Low Steam Temperature Troubleshooting
- ZJP-TRB-011: Desuperheater Malfunction Troubleshooting
- ZJP-CTRL-004: Alarm Setpoint Register
