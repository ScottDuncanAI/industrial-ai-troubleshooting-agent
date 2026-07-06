---
doc_id: normal_shutdown_procedure
doc_type: sop
equipment: [primary_fan, secondary_fan, induced_draft_fan, furnace_lower_hearth, furnace_chamber, steam_drum, low_temp_superheater, high_temp_superheater, steam_outlet]
tags: [FT_8301, FT_8302, TE_8313B, PT_8313A, PTCA_8322A, PTCA_8324, TE_8332A, ZZQBCHLL, AIR_8301A, AIR_8301B, SXLTCYZ, SXLTCYY, TV_8329ZC]
title: Normal Planned Shutdown Procedure
revision: 2.4
date: 2021-09-20
---

# Normal Planned Shutdown Procedure

**Document No.:** ZJP-SOP-003  
**Revision:** 2.4  
**Effective Date:** 2021-09-20  
**Approved By:** Plant Engineering Manager  
**Applicability:** Unit 1 — 130 t/h CFB Coal-Fired Boiler

---

## 1. Scope

This procedure covers planned, controlled shutdown of the CFB boiler from full load to a safe, depressurized, locked-out state suitable for maintenance or prolonged standby. Estimated shutdown time: **6–8 hours** to cool bed below 200°C.

For emergency shutdown, use ZJP-SOP-004.

---

## 2. Notification and Preparation

1. Notify process area that steam supply will be reduced and eventually interrupted — coordinate timing with production
2. Notify maintenance of any planned inspection or work scope for the outage
3. Prepare shift log entry with planned shutdown start time, reason, and expected duration
4. Confirm coal bunker level — note remaining inventory (coal will continue feeding until bed temperature drops)

---

## 3. Load Reduction (Hour 0–2)

### 3.1 Step Down Load
1. Transfer all control loops to manual operation:
   - Steam temperature control loop: hold TV_8329ZC at current position
   - Furnace draft control loop: hold IDF at current speed
   - O2 trim loop: hold fan speeds at current position
2. Reduce coal feed rate by **10 t/h per 15 minutes**
3. Proportionally reduce primary air (FT_8301) and secondary air (FT_8302) as coal decreases
4. Maintain AIR_8301A and AIR_8301B at 4.0–6.0% during load reduction (slight excess air acceptable)
5. Monitor TE_8332A — allow to drop below 530°C as load reduces; do not fight the natural decrease with reduced desuperheating

### 3.2 Steam System Handover
- At ZZQBCHLL < 50 t/h: notify process area to isolate or switch to alternate steam source
- At ZZQBCHLL < 20 t/h: begin closing main steam isolation valve
- Close main steam valve fully before bed temperature drops below 600°C

---

## 4. Coal Cutoff and Bed Cooldown (Hour 2–5)

1. When ready to complete shutdown, stop coal feeder completely
2. Maintain air flows at 30–40% to continue fluidizing the bed and cooling via convection
3. Continue IDF operation — maintain negative furnace pressure
4. TE_8313B will decline — target cool-down rate < 80°C/hour to protect refractory
5. Monitor SXLTCYZ and SXLTCYY — ΔP will decrease as bed cools and defluidizes
6. When bed temperature < 400°C (TE_8313B < 400°C), reduce primary air to 15% (minimum fluidization)
7. When bed temperature < 200°C, fans may be stopped

### 4.1 Steam Drum During Cooldown
- Drum vent valves: open when PTCA_8322A < 0.1 MPa to prevent vacuum formation
- Do not force-cool with cold feedwater injection — allow natural cooling
- Bottom blowdown: perform when PTCA_8322A < 0.5 MPa and drum water is warm (< 100°C)

---

## 5. Fan Shutdown Sequence

When bed temperature (TE_8313B) < 200°C and furnace has been ventilated for ≥ 30 minutes:
1. Stop secondary fan — close outlet damper
2. Stop primary fan — close outlet damper and inlet isolation
3. Reduce IDF to minimum speed, verify O2 at AIR_8301A/B stable
4. Stop IDF — close inlet damper and outlet isolation
5. Lock out all three fans per LOTO procedures (ZJP-SAFE-002, ZJP-SAFE-003, ZJP-SAFE-004)

---

## 6. Final Depressurization

1. Confirm all steam consumers are isolated
2. Allow PTCA_8322A to decay naturally to atmospheric
3. Open drum air vent valves once pressure is zero
4. Drain condensate from superheater headers via drain valves
5. Leave boiler in wet lay-up condition (drum full of treated water) for outages < 2 weeks
6. For outages > 2 weeks: perform dry lay-up per water treatment procedure ZJP-CHEM-001

---

## 7. Isolation for Maintenance (if applicable)
1. Complete all LOTO isolations per relevant equipment procedures
2. Sign off isolation register with shift supervisor
3. Issue equipment to maintenance (sign entry permit if confined space access required)

---

## 8. Post-Shutdown Log Entry
Record in shift log:
- Time coal feed stopped
- Time fans stopped
- Final drum pressure (PTCA_8322A) and temperature (TE_8332A) at shutdown
- Any abnormal observations during shutdown
- LOTO status and responsible person

---

## 9. References
- ZJP-SOP-001: Cold Start Procedure
- ZJP-SOP-004: Emergency Shutdown Procedure
- ZJP-CHEM-001: Feedwater Chemistry and Boiler Lay-Up
- ZJP-CHEM-002: Boiler Blowdown Procedure
- ZJP-SAFE-001 through ZJP-SAFE-003: LOTO Procedures
