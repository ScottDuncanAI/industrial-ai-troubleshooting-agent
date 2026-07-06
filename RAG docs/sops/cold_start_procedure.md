---
doc_id: cold_start_procedure
doc_type: sop
equipment: [primary_fan, secondary_fan, primary_air_preheater, secondary_air_preheater, furnace_lower_hearth, furnace_chamber, induced_draft_fan, steam_drum, low_temp_superheater, primary_desuperheater, high_temp_superheater, steam_outlet]
tags: [FT_8301, FT_8302, TE_8303, TE_8304, TE_8313B, PT_8313A, PT_8313B, PT_8313C, PT_8313D, PT_8313E, PT_8313F, PTCA_8322A, TE_8332A, PTCA_8324, ZZQBCHLL, AIR_8301A, AIR_8301B]
title: CFB Boiler Cold Start Procedure
revision: 3.2
date: 2021-11-15
---

# CFB Boiler Cold Start Procedure

**Document No.:** ZJP-SOP-001  
**Revision:** 3.2  
**Effective Date:** 2021-11-15  
**Approved By:** Plant Engineering Manager  
**Applicability:** Unit 1 — 130 t/h CFB Coal-Fired Boiler

---

## 1. Scope and Purpose

This procedure covers the full cold start sequence for the CFB boiler from ambient temperature (bed temperature < 100°C, unit idle for > 48 hours). A cold start requires full refractory warm-up, controlled bed material loading, and gradual light-off to avoid thermal shock to pressure parts.

Estimated time from initiation to full load: **10–14 hours**.

---

## 2. Prerequisites and Pre-Startup Checks

Before initiating the cold start, verify the following:

### 2.1 Permits and Safety
- [ ] Boiler is cleared of all maintenance work orders (MWOs)
- [ ] All LOTO devices removed and verified per isolation register
- [ ] Pre-startup safety inspection checklist (ZJP-SOP-007) completed and signed
- [ ] Operations supervisor notified and shift log entry made
- [ ] DCS/HMI system healthy — no critical alarms active

### 2.2 Utilities Available
- [ ] Instrument air pressure ≥ 0.5 MPa at header
- [ ] Plant electrical supply stable — MCC energized, UPS on-line
- [ ] Feedwater supply available — deaerator level ≥ 60%, feedwater pump on standby
- [ ] Coal bunker level ≥ 50% — coal feeder system ready
- [ ] Ignition fuel (light oil or gas) available and valve train leak-tested

### 2.3 Equipment Status
- [ ] Induced draft fan (IDF) — bearing lubrication confirmed, inlet damper closed
- [ ] Primary fan — bearing lubrication confirmed, outlet damper closed
- [ ] Secondary fan — bearing lubrication confirmed, outlet damper closed
- [ ] All furnace inspection ports and access doors sealed and bolted
- [ ] Ash removal system available (bottom ash cooler, fly ash conveying)
- [ ] Blowdown system lined up and drains positioned for warm-up drainage

### 2.4 Instrumentation
- [ ] All critical transmitters reading correctly (see Section 2.4 expected cold readings below)
- [ ] TE_8332A — steam outlet temperature (should read ambient, ~15–30°C)
- [ ] PTCA_8322A — steam drum pressure (should read 0 kPa gauge if fully depressurized)
- [ ] PT_8313A through PT_8313F — furnace pressure (all should read ~0 Pa)
- [ ] AIR_8301A, AIR_8301B — O2 analyzers warmed up and calibrated

---

## 3. Steam Drum Water Filling

### 3.1 Fill to Normal Cold Level
1. Open feedwater supply isolation valve to economizer inlet
2. Open economizer bypass valve (if installed) to bypass during filling
3. Start feedwater pump on minimum flow recirculation
4. Slowly open feedwater control valve — fill rate not to exceed 10 t/h during cold fill
5. Fill steam drum to **low-level mark** (approximately −50 mm below centerline gauge glass)
   - Cold water level will appear higher than hot level due to density difference
   - PTCA_8322A will show atmospheric pressure throughout
6. Vent drum through air vent valves until water flows — then partially close vents
7. Confirm no visible leaks at drum manway, nozzles, or gauge connections

---

## 4. Refractory Warm-Up (Hours 0–4)

The CFB furnace refractory requires slow, controlled warm-up to prevent thermal cracking. This phase uses ignition burners only — no coal.

### 4.1 Start Draft System
1. Start IDF in manual control at minimum speed (≈15% VFD command)
2. Verify furnace pressure PT_8313A–F reads −20 to −50 Pa negative
3. Open primary fan inlet damper — start primary fan at minimum speed (10%)
4. Open secondary fan inlet damper — start secondary fan at minimum speed (10%)
5. Purge furnace for **5 minutes minimum** — confirm O2 > 18% at AIR_8301A and AIR_8301B before lighting ignition burners
6. Establish total air flow ≥ 30% rated to maintain dilution

### 4.2 Ignition Burner Light-Off
1. Confirm ignition interlock satisfied (purge complete, draft established)
2. Light lower ignition burners first — confirm flame on CCTV/scanner
3. Light upper ignition burners — confirm flame
4. Target furnace exit gas temperature (TE_8313B): **raise at ≤ 50°C/hour**
5. Monitor furnace pressure — maintain −50 to −100 Pa via IDF speed adjustment

### 4.3 Refractory Warm-Up Hold Points
| Hold Point | Bed Temp | Duration |
|------------|----------|----------|
| Hold 1 | 100°C | 60 min |
| Hold 2 | 200°C | 60 min |
| Hold 3 | 350°C | 90 min |

At each hold point, inspect furnace exterior for cracking sounds or visible distress. Continue warm-up only when hold timer expires.

---

## 5. Bed Material Loading and Heatup (Hours 4–7)

### 5.1 Load Bed Material
1. Once bed temperature (inferred from lower furnace ΔP and ignition burner behavior) > 400°C, begin loading bed sand/recycle ash
2. Feed bed material via pneumatic conveying or manual charging port
3. Target bed inventory: SXLTCYZ and SXLTCYY differential pressure = **1.5–2.5 kPa** at low air flow
4. Increase primary air flow to **30–40%** of rated — confirm fluidization (bubbling evident by ΔP fluctuation ±100 Pa)

### 5.2 Coal Introduction
1. Confirm bed temperature > 650°C before introducing coal
2. Start coal feeder at **minimum rate (10–15%)** — typically 3–5 t/h
3. Monitor TE_8313B — should show temperature rise within 2–3 minutes of coal introduction
4. If no temperature rise within 5 minutes: stop coal feed, investigate before retrying
5. Gradually increase coal feed rate as bed temperature rises — target 1–2 t/h increase per 10 minutes
6. Reduce ignition burner output proportionally as coal combustion is established

---

## 6. Pressure Raising (Hours 7–10)

### 6.1 Steam Drum Pressure Raise
1. Once stable combustion is confirmed (TE_8313B > 750°C, coal feed self-sustaining), begin closing steam drum air vents
2. Allow PTCA_8322A to rise naturally — do not force with excessive firing
3. Target pressure raise rate: **≤ 0.5 MPa per 30 minutes**

| Drum Pressure (PTCA_8322A) | Action |
|---------------------------|--------|
| 0.2 MPa | Close drum air vent |
| 1.0 MPa | Check all flanged connections for leaks |
| 3.0 MPa | Hold 30 minutes — check drain valves, warm through superheater drains |
| 5.0 MPa | Begin warming through main steam line |
| 9.0 MPa | Approach normal operating pressure |
| 9.8 MPa | Full operating pressure — proceed to load increase |

### 6.2 Superheater Management
- During pressure raise, maintain superheater drain valves open until steam flow established
- Monitor TE_8332A — must not exceed **500°C** until ZZQBCHLL > 20 t/h
- Desuperheater (TV_8329ZC) should remain in manual/closed until steam flow established

---

## 7. Load Increase to Full Load (Hours 10–14)

### 7.1 Connect to Steam System
1. Crack main steam isolation valve — warm through to process header
2. Check TE_8332A: 530–545°C, PTCA_8324: 9.5–10.0 MPa
3. Slowly open main steam valve — monitor ZZQBCHLL for flow increase
4. Transfer steam temperature control to automatic (close steam_temp_control_loop)
5. Transfer furnace draft control to automatic (close furnace_draft_control_loop)
6. Transfer O2 trim to automatic (close combustion_air_control_loop)

### 7.2 Load Ramp
- Increase coal feed at maximum **5 t/h per 15 minutes**
- Coordinate primary air (FT_8301) and secondary air (FT_8302) increase with coal — maintain AIR_8301A and AIR_8301B between **3.5–5.5%** O2
- Target full load: ZZQBCHLL = 130 t/h

### 7.3 Full Load Confirmation
At full load, confirm:
- [ ] TE_8332A: 530–545°C
- [ ] PTCA_8324: 9.5–10.0 MPa
- [ ] ZZQBCHLL: 125–135 t/h
- [ ] AIR_8301A and AIR_8301B: 3.5–5.5%
- [ ] PT_8313A–F: −100 to −150 Pa
- [ ] YFJ3_ZD1 and YFJ3_ZD2: < 4.5 mm/s
- [ ] All alarms clear

---

## 8. Post-Startup Checks
1. Review all DCS trends for smooth, stable operation
2. Perform operator rounds within 30 minutes of reaching full load (see ZJP-SOP-006)
3. Enter startup completion in shift log with time and operator signature
4. Notify plant supervisor and process area that steam is available

---

## 9. Abnormal Conditions During Startup

| Condition | Action |
|-----------|--------|
| Flame loss on ignition burners | Stop coal, re-purge (5 min), re-light |
| Furnace pressure positive (> +50 Pa) | Trip all fans immediately, investigate |
| TE_8332A > 560°C during ramp | Open TV_8329ZC manually, reduce firing |
| Drum level low (< −100 mm) | Increase feedwater, reduce firing rate |
| IDF YFJ3_ZD1 or YFJ3_ZD2 > 7 mm/s | Trip IDF, execute emergency shutdown |

---

## 10. References
- ZJP-SOP-006: Daily Operator Rounds Checklist
- ZJP-SOP-007: Pre-Startup Safety Inspection Checklist
- ZJP-SOP-003: Normal Shutdown Procedure
- ZJP-SOP-004: Emergency Shutdown Procedure
- ZJP-DS-012: Induced Draft Fan Datasheet
- ZJP-SAFE-001: LOTO Procedure — Induced Draft Fan
