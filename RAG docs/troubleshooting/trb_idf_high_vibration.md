---
doc_id: trb_idf_high_vibration
doc_type: troubleshooting
equipment: [induced_draft_fan]
tags: [YFJ3_ZD1, YFJ3_ZD2, YFJ3_AI, PT_8313A]
title: Troubleshooting Guide — IDF High Bearing Vibration
revision: 2.2
date: 2022-01-20
---

# Troubleshooting Guide: IDF High Bearing Vibration

**Document No.:** ZJP-TRB-005  
**Symptom:** YFJ3_ZD1 or YFJ3_ZD2 elevated above 3.5 mm/s (alert) or 4.5 mm/s (alarm)  
**Revision:** 2.2 | **Date:** 2022-01-20

> **Safety:** IDF trip setpoint is 11 mm/s on either sensor. If vibration reaches 7 mm/s and is rising, do not wait for automatic trip — initiate manual ESD and shut the boiler down immediately. A catastrophic fan failure can destroy the ductwork and injure personnel.

---

## 1. Immediate Assessment

When YFJ3_ZD1 or YFJ3_ZD2 exceeds 3.5 mm/s (alert):

1. **Record both readings immediately** — note which bearing (drive end = ZD1, non-drive end = ZD2) and the absolute values
2. **Determine trend** — is vibration stable at elevated level, or rising?
   - Stable: monitor closely every 15 minutes; investigate root cause during next window
   - Rising: prepare for shutdown; notify supervisor
3. **Check YFJ3_AI** — is motor current elevated? (Elevated current + vibration = mechanical binding or severe imbalance)
4. **Listen at IDF** — distinctive vibration signatures:
   - Periodic, once-per-revolution knock: likely blade rub or imbalance
   - Continuous roughness: bearing damage
   - Intermittent/random: likely surge or flow instability

---

## 2. Probable Causes — Ranked by Frequency

### 2.1 Blade Fouling / Ash Buildup on Impeller (Most Common — ~50%)

**Description:** Fly ash accumulates on the impeller blades asymmetrically, causing mass imbalance. Vibration increases gradually over days to weeks, typically at twice-per-revolution frequency.

**Diagnosis:**
- Gradual onset: started increasing over past 3–7 days, not suddenly
- YFJ3_ZD1 and YFJ3_ZD2 both elevated (whole shaft affected)
- YFJ3_AI slightly elevated (heavier impeller)
- Happens more often after running at reduced load (less centrifugal shedding)

**Action:**
1. If vibration is stable < 4.5 mm/s: plan an outage for blade cleaning within 7 days
2. Online ash cleaning: briefly increase IDF speed to full for 10–15 minutes — centrifugal force may shed loose deposits (not always successful)
3. If vibration is rising: schedule shutdown at earliest opportunity for blade inspection (ZJP-MNT-004)
4. During shutdown, clean blades with compressed air and inspect for erosion

### 2.2 Blade Erosion — Impeller Imbalance (Gradual, Long-Term)

**Description:** Uniform blade erosion still causes imbalance if erosion is uneven across blades. This is a long-term mechanism — vibration has been trending upward over months.

**Diagnosis:**
- Slow trend over months; annual vibration readings trending up
- Last outage inspection may have noted erosion but blades not replaced

**Action:**
1. Outage required: blade replacement or re-balancing (ZJP-MNT-004)
2. If vibration > 5 mm/s and rising: do not defer — plan immediate short shutdown for blade inspection

### 2.3 Bearing Damage (Acute Onset)

**Description:** Bearing defects (spalling, fatigue) cause high-frequency vibration, often with bearing temperature rise. Onset can be sudden.

**Diagnosis:**
- Sudden increase in vibration — was normal yesterday
- Bearing housing temperature elevated (check during rounds: hand to housing — should be warm not hot)
- High-frequency vibration signature (portable analyzer shows 5–20 kHz energy)
- YFJ3_AI possibly elevated if bearing has seized partially

**Action:**
1. If vibration > 5 mm/s with any of the above: shut down IDF immediately (manual ESD)
2. During outage: replace both bearings regardless of which one appears damaged (ZJP-MNT-003)
3. Investigate lubrication: was oil supply maintained? Oil sample analysis for metallic particles?

### 2.4 Misalignment (After Maintenance)

**Description:** If vibration increased immediately after maintenance work (bearing replacement, coupling work), misalignment is the most likely cause.

**Diagnosis:**
- Timeline: vibration increased within hours of restart post-maintenance
- Both ZD1 and ZD2 affected but ZD2 (non-drive end) more pronounced suggests angular misalignment

**Action:**
1. Shut down — re-check coupling alignment per ZJP-MNT-003 Section 7
2. Acceptable alignment: parallel < 0.05 mm, angular < 0.05 mm per 100 mm
3. Confirm coupling guard properly installed (not touching shaft)

### 2.5 Fan Operating in Surge (Flow-Induced)

**Description:** At very low flow (startup or minimum load), the IDF may surge — flow separates from impeller blades, creating periodic pressure pulses and vibration. Distinctive pulsing sound accompanies this.

**Diagnosis:**
- Vibration irregular, pulsing, not smooth
- Happens at low load (startup, reduced firing)
- PT_8313A–F showing unstable pressure (oscillating ±50 Pa)

**Action:**
1. Increase IDF speed or open inlet damper wider — move away from surge point
2. If surge occurs during startup: increase air flow before stepping up IDF speed
3. If surge occurs at minimum load: do not operate below minimum stable flow as defined in ZJP-DS-012

---

## 3. Vibration Monitoring Protocol (Elevated but Below Trip)

If vibration is between 3.5–5 mm/s and stable:
- Increase monitoring frequency: check DCS readings every 30 minutes
- Assign an operator to do local vibration check with portable instrument every 2 hours
- Prepare shutdown plan (notify process area of possible steam interruption)
- Document trend in shift log

If vibration exceeds 5 mm/s: initiate controlled shutdown within 2 hours maximum.

---

## 4. Post-Vibration-Trip Return to Service

After IDF trips on high vibration:
1. Mandatory bearing inspection before restart (ZJP-MNT-003)
2. Mandatory blade inspection (ZJP-MNT-004)
3. Post-repair acceptance test: vibration must be < 2.5 mm/s at full speed before return to continuous service
4. Complete vibration trip report (Form ZJP-F-004) and submit to engineering
