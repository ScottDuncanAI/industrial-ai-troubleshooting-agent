---
doc_id: safe_blowdown_procedure
doc_type: safety
equipment: [steam_drum]
tags: [PTCA_8322A]
title: Continuous and Intermittent Blowdown Procedure
revision: 1.4
date: 2021-09-01
---

# Boiler Blowdown Procedure

**Document No.:** ZJP-CHEM-002  
**Revision:** 1.4 | **Date:** 2021-09-01  
**Frequency:** Intermittent blowdown every 8 hours; continuous blowdown ongoing

> **CAUTION:** Blowdown valves release high-pressure, high-temperature water. PPE — heat-resistant gloves, face shield, and steam-resistant clothing — is MANDATORY during any manual blowdown operation.

---

## 1. Purpose

Blowdown controls the concentration of dissolved solids (TDS), alkalinity, and phosphate in the boiler drum water. Without blowdown, dissolved solids concentrate over time as pure steam leaves the drum, eventually causing carryover and tube fouling.

---

## 2. Continuous Blowdown

**Location:** Steam drum continuous blowdown nozzle (top connection, near water line)  
**Control:** Motorized control valve (continuous blowdown CV) — set by DCS to maintain drum water conductivity target  
**Target:** Drum water conductivity < 30 µS/cm  
**Typical flow rate:** 1.3–3.9 t/h (adjusted automatically)

**Continuous blowdown heat recovery:**
Blowdown water (at ~311°C, 9.8 MPa) is flashed in the blowdown vessel:
- Flash steam (generated at lower pressure) returned to deaerator
- Remaining hot water discharged to blowdown pit via heat exchanger (cooled to < 40°C before discharge)

Do not bypass or close the continuous blowdown control valve without engineering authorization — TDS will climb rapidly.

---

## 3. Intermittent (Manual) Blowdown Procedure

**Frequency:** Every 8 hours (3× per 24 hours)  
**Timing constraints:** Do not perform intermittent blowdown during:
- Load changes (ramp up or down — drum level is already transient)
- Within 30 minutes of a cold start (drum level not stabilized)
- When drum level is already at −30 mm or below

**Step-by-step procedure:**
1. Confirm boiler is at steady load — no load ramps in progress
2. Confirm drum level is at normal level (+/−10 mm of centerline) — note: blowdown will temporarily drop level
3. Inform control room operator: "Beginning blowdown sequence"
4. Put on PPE: heat-resistant gloves, face shield
5. Confirm drain line is open and valve downstream is positioned to blowdown vessel — not to atmosphere
6. Open blowdown valve (turn 1–2 full turns): hold for 30 seconds — listen for flow
7. Close blowdown valve fully — confirm seat is tight (no weeping sound)
8. Observe drum level recovery on DCS within 2 minutes
9. Record blowdown in shift log: time and operator initials

**Multiple blowdown points:** If the drum has bottom nozzles at multiple locations (front and rear), repeat the procedure for each valve in sequence — do not open both simultaneously.

---

## 4. Post-Blowdown Chemistry Check

After each intermittent blowdown:
- Take drum water sample (if sampling infrastructure permits during operation) or note on chemistry schedule that blowdown was completed
- Chemistry team verifies TDS and phosphate within 4 hours of each blowdown sequence

---

## 5. Abnormal Conditions

| Condition | Action |
|-----------|--------|
| Blowdown valve leaking after closure | Do not leave — get second operator; may need work order to tighten packing |
| Drum level drops > 50 mm and doesn't recover after 3 minutes | Open feedwater control valve fully; stop any further blowdown |
| Steam/water escaping at blowdown valve body | Evacuate area, close upstream isolation, report valve failure immediately |
| Blowdown pit water temperature > 50°C at outlet | Reduce blowdown rate; check heat exchanger |

---

## 6. Revision History

| Rev | Date | Change |
|-----|------|--------|
| 1.0 | 2019-03-01 | Initial issue |
| 1.2 | 2020-06-01 | Added timing constraints (no blowdown during load ramp) |
| 1.4 | 2021-09-01 | Added PPE requirement detail; aligned with ZJP-CHEM-001 Rev 2.2 |
