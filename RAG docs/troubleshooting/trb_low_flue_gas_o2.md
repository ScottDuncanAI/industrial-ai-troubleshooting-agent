---
doc_id: trb_low_flue_gas_o2
doc_type: troubleshooting
equipment: [furnace_chamber, furnace_lower_hearth, primary_fan, secondary_fan, economizer]
tags: [AIR_8301A, AIR_8301B, FT_8301, FT_8302, TE_8313B, TE_8332A]
title: Troubleshooting Guide — Low Flue Gas O2 (Under-Aeration / CO Risk)
revision: 2.0
date: 2022-01-20
---

# Troubleshooting Guide: Low Flue Gas O2

**Document No.:** ZJP-TRB-008  
**Symptom:** AIR_8301A or AIR_8301B < 3.0% (alarm at 2.0%)  
**Revision:** 2.0 | **Date:** 2022-01-20

> **SAFETY WARNING:** Low O2 in flue gas indicates incomplete combustion — carbon monoxide (CO) is being produced. CO is toxic (TLV 25 ppm TWA) and can accumulate in the backpass and ductwork, creating an explosion hazard if a relight occurs. If O2 drops below 1.5%, BPS will trip the boiler.

---

## 1. Immediate Actions

When AIR_8301A or AIR_8301B < 2.5%:
1. **Immediately increase air flows** — increase FT_8301 (primary) by 10,000 m³/h and FT_8302 (secondary) by 5,000 m³/h manually
2. If in automatic mode: override combustion_air_control_loop to manual, increase air
3. Reduce coal feed by 10% simultaneously — bring fuel-to-air ratio back into balance
4. If O2 continues declining below 2.0%: reduce coal feed a further 15%; notify supervisor
5. If O2 drops below 1.5%: BPS auto-trips the boiler — do not attempt to override

---

## 2. Probable Causes

### 2.1 Combustion Air Control Loop Setpoint Too Low / Loop Malfunction

**Diagnosis:** O2 setpoint has been set too low (below 3.0%), or loop has wound up in wrong direction.

**Action:**
1. Check O2 setpoint — restore to 4.0% if changed
2. Check loop for integrator windup: if output is at minimum air flow despite low O2 reading, loop is malfunctioning
3. Switch to manual and adjust air flows directly

### 2.2 Primary or Secondary Fan Degradation

**Description:** Reduced air flow from a mechanically degraded fan or a stuck damper.

**Diagnosis:**
- FT_8301 or FT_8302 below expected for current damper position
- Fan motor current (check locally) lower than expected
- AIR_8301A and AIR_8301B tracking together (both dropping — process issue, not instrument)

**Action:**
1. Manually open dampers — confirm FT_8301 and FT_8302 increase
2. If FT does not increase with damper open: fan may be in surge, or mechanical fault (stall, blocked inlet)
3. Reduce coal feed to match available air flow; schedule fan inspection

### 2.3 Coal Feed Rate Unexpectedly High

**Description:** Coal feeder malfunction causing feed rate above DCS setpoint — excess unburned coal depletes O2.

**Diagnosis:**
- O2 drops while fan flows appear normal or even slightly reduced
- TE_8313B very high (> 960°C) — excess fuel is burning at high temperature
- TE_8332A may also be rising (excess heat)

**Action:**
1. Stop coal feeder for 30 seconds, then restart at a reduced rate
2. Increase air flows to compensate until coal feed is verified under control
3. Check feeder calibration — weigh actual output vs. DCS setpoint

### 2.4 O2 Analyzer Fault (Reading Low)

**Diagnosis:**
- AIR_8301A and AIR_8301B diverge significantly (one low, one normal) → the low-reading analyzer is faulty
- Or: both analyzers low but TE_8313B is normal (not elevated as would be expected with low O2 real condition)

**Action:**
1. Check probe for blockage (plugged reference air inlet, plugged sample probe)
2. Perform span calibration with reference gas
3. If one analyzer confirmed faulty: disable it from control loop, run on single analyzer with additional manual monitoring

---

## 3. After Low O2 Event — CO Risk Mitigation

If O2 fell below 1.5% before being corrected:
1. Before any restart attempt, purge the entire flue gas path (furnace, backpass, ductwork) with > 25% O2 air flow for minimum **5 minutes**
2. CO analyzer reading (if available at stack) should be < 50 ppm before restart
3. Do not open any ductwork access points until purge is confirmed complete — CO pockets can be lethal
4. Complete incident report and notify safety officer

---

## 4. Prevention

- Monitor AIR_8301A and AIR_8301B together as a pair — alert on divergence > 1.5%
- Never allow the combustion_air_control_loop O2 setpoint below 3.0%
- Review coal quality when O2 trend requires persistent adjustments — high-volatile coal can cause rapid O2 swings
