---
doc_id: trb_idf_high_current
doc_type: troubleshooting
equipment: [induced_draft_fan]
tags: [YFJ3_AI, YFJ3_ZD1, YFJ3_ZD2, PT_8313A]
title: Troubleshooting Guide — IDF Motor High Current
revision: 1.3
date: 2022-01-20
---

# Troubleshooting Guide: IDF Motor High Current

**Document No.:** ZJP-TRB-013  
**Symptom:** YFJ3_AI elevated above 280 A (high alarm) or trending toward 310 A (trip)  
**Revision:** 1.3 | **Date:** 2022-01-20

---

## 1. Normal Current Reference

| Boiler Load | Expected YFJ3_AI |
|------------|-----------------|
| 100% | 220–250 A |
| 75% | 175–200 A |
| 50% | 140–165 A |

YFJ3_AI > 280 A at full load = 12% above maximum normal → investigate.

---

## 2. Immediate Actions

When YFJ3_AI > 280 A:
1. Check YFJ3_ZD1 and YFJ3_ZD2 — if vibration is also elevated, likely mechanical cause (go to Section 3.1)
2. Check IDF speed vs. current — is fan running faster than normal for current boiler conditions? (go to Section 3.3)
3. If current is rising rapidly (> 290 A and increasing): reduce IDF speed in manual to prevent motor trip

---

## 3. Probable Causes

### 3.1 Mechanical Binding — Impeller Rubbing

**Symptoms:** High current + high vibration (YFJ3_ZD1 or ZD2 > 4.5 mm/s). Possible metallic noise heard locally.

**Action:** Immediate controlled shutdown — impeller contact with casing will cause catastrophic damage. Inspect bearing alignment and blade clearances before restart.

### 3.2 Impeller Ash Buildup (Mass Increase)

**Symptoms:** Gradual increase in YFJ3_AI over days; vibration also slightly elevated; ash accumulation suspected.

**Action:** Monitor for 24 hours; if trend continues, plan short shutdown for blade cleaning (ZJP-MNT-004). Online cleaning attempt (brief high-speed run) may help.

### 3.3 High Flue Gas Flow (IDF Overloaded at High Load)

**Symptoms:** YFJ3_AI elevated only when boiler is at maximum load; decreases when load is reduced.

**Action:** Check if boiler is being pushed above MCR (130 t/h). If so, reduce coal feed to rated load. IDF is rated for design flow — operating above design continuously causes motor overloading.

### 3.4 High Flue Gas Density (Elevated Temperature or Composition)

**Symptoms:** Flue gas entering the IDF at higher temperature than normal raises gas density and increases fan power requirement.

Check: Is TE_8319A/B (economizer outlet flue gas temperature) elevated? High gas temperature = higher gas density = higher fan power.

**Action:** Investigate why TE_8319A/B is elevated (economizer fouling, air preheater bypass, high load) — address root cause.

### 3.5 VFD Issue — Overmodulation or Power Factor Problem

**Symptoms:** YFJ3_AI elevated but speed feedback is normal; no mechanical explanation; VFD local display showing warning codes.

**Action:**
1. Check VFD display for error/warning codes
2. Check VFD input current (on VFD input terminals) vs. output — large difference indicates VFD efficiency problem
3. Notify electrical team — VFD may need servicing

---

## 4. Motor Protection

The motor protection relay will trip YFJ3 at 310 A sustained. If the motor trips on overcurrent:
1. Do not restart immediately — allow motor to cool (minimum 30 minutes)
2. Identify root cause before restart
3. If overcurrent trip repeats: mandatory electrical inspection before further operation

---

## 5. Relationship to IDF Vibration Guide

High current and high vibration together almost always indicate a mechanical problem. Treat as a mechanical fault (ZJP-TRB-005) first — the current increase is a consequence of the mechanical problem, not the primary fault.
