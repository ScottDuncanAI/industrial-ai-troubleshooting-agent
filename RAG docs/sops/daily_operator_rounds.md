---
doc_id: daily_operator_rounds
doc_type: sop
equipment: [primary_fan, secondary_fan, induced_draft_fan, primary_air_preheater, secondary_air_preheater, cyclone_separator_left, cyclone_separator_right, economizer, steam_drum, low_temp_superheater, high_temp_superheater, primary_desuperheater, steam_outlet, chimney]
tags: [FT_8301, FT_8302, FT_8306A, FT_8306B, TE_8303, TE_8304, TE_8313B, TE_8319A, TE_8319B, TE_8332A, PT_8313A, PTCA_8322A, PTCA_8324, ZZQBCHLL, AIR_8301A, AIR_8301B, YFJ3_AI, YFJ3_ZD1, YFJ3_ZD2, ZCLCCY, YCLCCY, SXLTCYZ, SXLTCYY, TV_8329ZC, YJJWSLL]
title: Daily Operator Rounds Checklist
revision: 5.1
date: 2022-02-14
---

# Daily Operator Rounds Checklist

**Document No.:** ZJP-SOP-006  
**Revision:** 5.1  
**Effective Date:** 2022-02-14  
**Applicability:** Unit 1 — 130 t/h CFB Coal-Fired Boiler  
**Frequency:** Every 4 hours during normal operation (minimum 6 rounds per day)

> **Note:** This checklist supplements DCS monitoring. Physical inspection is required — many conditions (leaks, unusual sounds, vibration) cannot be detected remotely.

---

## Round Completion Instructions
- Complete all items in sequence
- Record all values in the rounds log book — do not leave blanks
- Circle any out-of-normal values and notify shift supervisor immediately
- Sign and time-stamp the completed sheet

---

## Section 1: Control Room Pre-Round DCS Check (5 minutes)

Before leaving the control room, confirm no active alarms and record the following:

| Tag | Description | Current Reading | Normal Range | OK? |
|-----|-------------|----------------|--------------|-----|
| TE_8332A | Steam outlet temperature | _____°C | 530–545°C | ☐ |
| PTCA_8324 | Outlet steam pressure | _____ kPa | 9400–10000 kPa | ☐ |
| PTCA_8322A | Steam drum pressure | _____ kPa | 9400–10000 kPa | ☐ |
| ZZQBCHLL | Main steam flow | _____ t/h | 120–135 t/h | ☐ |
| AIR_8301A | Flue gas O2 (left) | ____% | 3.5–5.5% | ☐ |
| AIR_8301B | Flue gas O2 (right) | ____% | 3.5–5.5% | ☐ |
| PT_8313A | Furnace pressure (A) | _____ Pa | −80 to −160 Pa | ☐ |
| YFJ3_ZD1 | IDF bearing vibration A | _____ mm/s | < 4.5 mm/s | ☐ |
| YFJ3_ZD2 | IDF bearing vibration B | _____ mm/s | < 4.5 mm/s | ☐ |

---

## Section 2: Boiler House — Lower Level

### 2.1 Primary Fan Area
- [ ] Primary fan bearing housing: no abnormal heat (hand-check housing — should be warm, not hot)
- [ ] Primary fan: no unusual noise (grinding, squealing, rubbing)
- [ ] FT_8301 reading: _____ m³/h (normal: 95,000–130,000 m³/h at full load)
- [ ] Primary fan inlet filter: no visible blockage or debris accumulation
- [ ] Fan motor: no visible smoke, burning smell, or vibration
- [ ] Area: no coal dust accumulation on hot surfaces

### 2.2 Secondary Fan Area
- [ ] Secondary fan bearing housing: no abnormal heat
- [ ] Secondary fan: no unusual noise
- [ ] FT_8302 reading: _____ m³/h (normal: 55,000–80,000 m³/h at full load)
- [ ] Fan motor: no visible smoke, burning smell, or vibration

### 2.3 Return Air Chambers
- [ ] FT_8306A (left return air): _____ m³/h
- [ ] FT_8306B (right return air): _____ m³/h
- [ ] Return air ducting: no visible leaks (hot air escaping joints)
- [ ] L-seal area: no unusual solids accumulation or blockage

### 2.4 Coal Feed System
- [ ] Coal bunker level indicator: ____% (notify if < 30%)
- [ ] Coal feeders: running smoothly, no surging or jamming
- [ ] Coal feed piping: no blockages or unusual vibration

---

## Section 3: Furnace Area

### 3.1 Furnace Lower Hearth
- [ ] SXLTCYZ (hearth ΔP left): _____ Pa (normal at full load: 1500–3000 Pa)
- [ ] SXLTCYY (hearth ΔP right): _____ Pa (normal at full load: 1500–3000 Pa)
- [ ] Bottom ash discharge system: operating normally, ash discharging regularly
- [ ] Bed ash cooler: operating, no overflow or blockage
- [ ] Lower furnace exterior: no red-hot spots or unusual heat on casing

### 3.2 Furnace Upper Chamber
- [ ] TE_8313B (upper furnace temp): _____°C (normal: 850–950°C at full load)
- [ ] PT_8313A–F readings reviewed on DCS: all showing −80 to −160 Pa ☐
- [ ] Furnace casing exterior: no hot spots, deformation, or gas leaks (detectable by holding hand near seams)
- [ ] Expansion joints: intact, no cracks or separation

---

## Section 4: Cyclone Separators and Backpass

### 4.1 Cyclone Separators
- [ ] ZCLCCY (left cyclone ΔP): _____ Pa (normal: 600–1200 Pa)
- [ ] YCLCCY (right cyclone ΔP): _____ Pa (normal: 600–1200 Pa)
- [ ] Cyclone casing exterior: no hot spots or unusual heat
- [ ] Solid return legs: solids flow visible/audible (characteristic rumbling), no blockage

### 4.2 Upper Economizer and Backpass
- [ ] TE_8319A (economizer flue gas outlet left): _____°C (normal: 135–160°C)
- [ ] TE_8319B (economizer flue gas outlet right): _____°C (normal: 135–160°C)
- [ ] AIR_8301A reading confirmed: ____% (normal: 3.5–5.5%)
- [ ] AIR_8301B reading confirmed: ____% (normal: 3.5–5.5%)
- [ ] Backpass casing: no unusual heat or gas escape at seams

---

## Section 5: Induced Draft Fan (IDF) — Upper Level

> **Caution:** High noise and vibration area — wear hearing protection. Do not touch rotating shaft.

- [ ] YFJ3_ZD1 (bearing vibration A): _____ mm/s — confirm matches DCS reading
- [ ] YFJ3_ZD2 (bearing vibration B): _____ mm/s — confirm matches DCS reading
- [ ] YFJ3_AI (motor current): _____ A (normal: 180–250 A at full load)
- [ ] IDF bearing housings: warm to touch but not excessively hot (< 70°C by feel)
- [ ] IDF lubrication oil level: within sight glass range ☐
- [ ] IDF: no unusual noise (metallic scraping, high-pitched whine, intermittent surging)
- [ ] IDF motor: no visible smoke or burning smell
- [ ] Inlet and outlet ductwork: no visible gas leaks or unusual heat

---

## Section 6: Air Preheaters

### 6.1 Primary Air Preheater
- [ ] TE_8303 (primary air outlet temp): _____°C (normal: 180–220°C)
- [ ] Preheater casing: no gas leaks at seams, flanges intact
- [ ] Air duct connections: no visible hot gas leakage into air side

### 6.2 Secondary Air Preheater
- [ ] TE_8304 (secondary air outlet temp): _____°C (normal: 175–215°C)
- [ ] Preheater casing: same checks as primary

---

## Section 7: Steam Side

### 7.1 Steam Drum
- [ ] PTCA_8322A reading confirmed: _____ kPa
- [ ] Drum gauge glass level: _____ mm relative to centerline (normal: ±50 mm)
- [ ] Drum insulation: no hot spots or damage
- [ ] Safety valves: not lifting (listen for hissing), no weeping

### 7.2 Superheaters and Desuperheater
- [ ] TE_8332A: _____°C (confirm matches DCS)
- [ ] PTCA_8324: _____ kPa (confirm matches DCS)
- [ ] TV_8329ZC (desuperheater valve position): ____% (normal: 20–60% at full load)
- [ ] YJJWSLL (desuperheating water flow): _____ t/h (normal: 2–8 t/h)
- [ ] Superheater headers: no steam leaks at flanges or drain valves

---

## Section 8: Stack / Chimney
- [ ] Stack visible from boiler roof or designated observation point
- [ ] Exhaust color: colorless to light gray (white water vapor acceptable in cold weather)
- [ ] No visible black smoke (indicates incomplete combustion — report immediately if observed)
- [ ] No unusual odor around chimney base

---

## Section 9: General Boiler Area
- [ ] Fire extinguishers: all in place and tagged current
- [ ] Emergency exits: clear and unobstructed
- [ ] No coal dust accumulation on walkways, grating, or hot surfaces
- [ ] All safety signs in place and legible
- [ ] No unauthorized personnel in restricted boiler area

---

## Rounds Completion

**Round completed by:** ________________________  
**Time:** ____________  
**Shift:** ____________  
**Abnormal observations noted:** ☐ Yes (see remarks) / ☐ None  

**Remarks:**
_______________________________________________
_______________________________________________

**Shift supervisor notified of abnormal conditions:** ☐ Yes / ☐ N/A
