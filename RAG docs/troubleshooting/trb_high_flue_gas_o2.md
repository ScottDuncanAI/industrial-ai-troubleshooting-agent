---
doc_id: trb_high_flue_gas_o2
doc_type: troubleshooting
equipment: [furnace_chamber, furnace_lower_hearth, economizer, primary_fan, secondary_fan]
tags: [AIR_8301A, AIR_8301B, FT_8301, FT_8302, TE_8313B, TE_8332A, ZZQBCHLL]
title: Troubleshooting Guide — High Flue Gas O2 (Over-Aeration)
revision: 1.3
date: 2022-01-20
---

# Troubleshooting Guide: High Flue Gas O2

**Document No.:** ZJP-TRB-007  
**Symptom:** AIR_8301A or AIR_8301B consistently > 6.0% (normal target: 3.5–5.5%)  
**Revision:** 1.3 | **Date:** 2022-01-20

---

## 1. Impact of High Flue Gas O2

Excess air (high O2) reduces boiler efficiency:
- Every 1% increase in excess O2 above the optimum increases heat loss in the flue gas by approximately 0.5–0.8%
- High O2 at full load indicates the combustion_air_control_loop is supplying more air than necessary
- At > 8% O2: fan power is being wasted, steam temperature may be lower than setpoint (too much cooling air), and NOₓ emissions may be elevated

---

## 2. Probable Causes

### 2.1 Combustion Air Control Loop Malfunction — Setpoint Too High

**Diagnosis:** O2 setpoint in combustion_air_control_loop set higher than normal (operator may have temporarily raised it and not restored it).

**Action:** Check O2 setpoint in DCS — should be 4.0% for normal coal. If changed, restore to 4.0%. Review shift log for operator notes.

### 2.2 Air Infiltration (Furnace Air In-Leakage)

**Description:** Air leaks into the furnace or backpass through expansion joint gaps, inspection door seals, or damaged casing. This dilutes the flue gas with additional oxygen that does not participate in combustion.

**Diagnosis:**
- O2 is high but fuel feed and fan flows appear normal
- TE_8313B is lower than expected (dilution cooling effect)
- Left-right O2 divergence (AIR_8301A ≠ AIR_8301B) if infiltration is on one side

**Action:**
1. Visual inspection of furnace exterior for visible cold-air jets (a candle or smoke pencil held near suspect areas will deflect toward the boiler)
2. Identify leakage points — common locations: expansion joints, manway doors, burner tile seals
3. Seal temporarily with high-temperature caulk or refractory cement (online repair possible for minor leaks)
4. Document location for proper repair during next outage

### 2.3 O2 Analyzer Calibration Drift

**Diagnosis:**
- AIR_8301A and AIR_8301B agree with each other (both high) → process issue
- One analyzer high, one normal → suspect the high-reading analyzer

**Action:**
1. Check O2 analyzer calibration date — if > 1 month since calibration, recalibrate immediately
2. Perform span check with certified reference gas
3. If calibration confirmed correct and analyzer is still reading high: check for air infiltration into sample probe

### 2.4 Reduced Coal Feed (High O2 for Load)

**Diagnosis:** At lower loads, the excess air ratio naturally increases because minimum fan speeds provide more air than needed.

**Action:**
- At loads < 70%: O2 up to 6.5% may be acceptable — monitor but not necessarily a fault
- Reduce fan speeds if O2 significantly above setpoint at low load

---

## 3. Correction Actions

1. If combustion_air_control_loop is in automatic: review setpoint and adjust coal-to-air ratio
2. If in manual: reduce FT_8301 and/or FT_8302 gradually (reduce by 5,000 m³/h steps, wait 3 minutes for O2 response)
3. Target AIR_8301A and AIR_8301B at 3.5–4.5% under normal load
4. Do not reduce O2 below 3.0% — risk of CO formation increases sharply below this level (see ZJP-TRB-008)

---

## 4. Efficiency Impact Calculation

At current O2 reading ______%, estimated efficiency reduction vs. design (4.0% O2):
- Each 1% above 4.0% O2: approximately 0.6% efficiency reduction
- Coal consumption increase: approximately 140 kg/h per 1% excess O2 at full load
- Annual cost at CNY 600/tonne coal: approximately CNY 740,000 per 1% sustained O2 excess

This justifies prompt correction rather than leaving high O2 as a "safe margin."
