---
doc_id: hot_restart_procedure
doc_type: sop
equipment: [primary_fan, secondary_fan, induced_draft_fan, furnace_lower_hearth, furnace_chamber, steam_drum, steam_outlet]
tags: [FT_8301, FT_8302, TE_8313B, PT_8313A, PT_8313B, PTCA_8322A, PTCA_8324, TE_8332A, ZZQBCHLL, AIR_8301A, AIR_8301B, SXLTCYZ, SXLTCYY]
title: Hot Restart Procedure — After Short Planned Outage
revision: 2.1
date: 2022-01-08
---

# Hot Restart Procedure — After Short Planned Outage (< 8 Hours)

**Document No.:** ZJP-SOP-002  
**Revision:** 2.1  
**Effective Date:** 2022-01-08  
**Approved By:** Plant Engineering Manager  
**Applicability:** Unit 1 — 130 t/h CFB Coal-Fired Boiler

---

## 1. Scope

This procedure applies when the boiler has been shut down in a planned, controlled manner for less than 8 hours and bed temperature remains above 400°C. Because the bed retains significant heat, no ignition burner warm-up phase is required and restart to full load can be achieved in **2–4 hours**.

If bed temperature has fallen below 400°C or the unit has been idle > 8 hours, use the **Cold Start Procedure (ZJP-SOP-001)**.

---

## 2. Pre-Restart Verification

### 2.1 Confirm Hot-Hold Conditions
- [ ] SXLTCYZ and SXLTCYY (hearth ΔP) > 0.8 kPa — bed material retained
- [ ] Bed temperature (inferred) > 400°C — confirmed by thermal soaking time since shutdown
- [ ] PTCA_8322A (drum pressure) > 1.0 MPa — unit still pressurized, no air ingress into pressure parts
- [ ] All maintenance personnel have cleared the unit
- [ ] Any planned maintenance performed during outage is complete and work orders closed

### 2.2 Instrumentation Check
- [ ] AIR_8301A and AIR_8301B O2 analyzers on-line and reading
- [ ] All furnace pressure transmitters (PT_8313A–F) functional
- [ ] TE_8332A reading (will show below normal during hot-hold, typically 300–450°C)

### 2.3 Steam Side
- [ ] Steam drum level PTCA_8322A within −50 to +50 mm of setpoint
- [ ] Main steam isolation valve in closed position
- [ ] Superheater drains cracked open

---

## 3. Draft System Start

1. Start IDF at minimum speed — confirm furnace pressure negative (−20 to −50 Pa) within 30 seconds
2. Open primary fan outlet damper — start primary fan at 20% speed
3. Open secondary fan outlet damper — start secondary fan at 20% speed
4. **Furnace purge is NOT required** if unit was shut down under controlled conditions with draft maintained; however, confirm O2 at AIR_8301A and AIR_8301B > 15% before coal introduction
5. If O2 < 15%: purge at minimum 30% air flow for 3 minutes before proceeding

---

## 4. Bed Re-Ignition and Coal Light-Off

1. Confirm bed temperature > 400°C (review TE_8313B trend or thermal soak calculation)
2. Begin coal feed at **minimum rate (5–8 t/h)**
3. Increase primary air (FT_8301) to 35% to re-fluidize the bed — watch SXLTCYZ/Y for ΔP response
4. Monitor TE_8313B — temperature rise should be observed within 5 minutes
5. If no temperature rise in 5 minutes: stop coal feed, verify bed temperature, check coal flow path
6. Once bed temperature is rising steadily, increase coal feed at 3–5 t/h per 10 minutes
7. Reduce firing rate once TE_8313B exceeds 850°C to avoid temperature overshoot

---

## 5. Pressure Restoration

1. Monitor PTCA_8322A — if drum pressure was maintained > 3 MPa, skip to step 4
2. If pressure has dropped to < 1 MPa during hot-hold: raise pressure at ≤ 1 MPa per 20 minutes
3. Keep superheater drains open until ZZQBCHLL > 15 t/h
4. Once PTCA_8322A ≥ 9.0 MPa and TE_8332A between 520–545°C: connect to steam system
5. Gradually open main steam isolation valve — monitor ZZQBCHLL

---

## 6. Control Loop Transfer to Automatic

Once ZZQBCHLL > 60 t/h and TE_8332A is stable:
1. Transfer steam temperature control loop to automatic — setpoint 540°C
2. Transfer furnace draft control loop to automatic — setpoint −120 Pa
3. Transfer O2 trim to automatic — setpoint 4.0% O2

---

## 7. Load Ramp to Full Load

- Ramp coal feed at up to **8 t/h per 10 minutes** (faster than cold start — bed is already hot)
- Coordinate air flows: maintain AIR_8301A and AIR_8301B 3.5–5.5% throughout ramp
- Target full load: ZZQBCHLL = 130 t/h within 60–90 minutes of coal light-off

---

## 8. Full Load Confirmation Checklist
- [ ] TE_8332A: 530–545°C
- [ ] PTCA_8324: 9.5–10.0 MPa
- [ ] ZZQBCHLL: 125–135 t/h
- [ ] AIR_8301A and AIR_8301B: 3.5–5.5%
- [ ] PT_8313A–F: −100 to −150 Pa
- [ ] YFJ3_ZD1 and YFJ3_ZD2: < 4.5 mm/s
- [ ] All alarms clear, shift log entry completed

---

## 9. References
- ZJP-SOP-001: Cold Start Procedure
- ZJP-SOP-003: Normal Shutdown Procedure
- ZJP-SOP-006: Daily Operator Rounds Checklist
