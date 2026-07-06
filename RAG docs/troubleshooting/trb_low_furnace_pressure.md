---
doc_id: trb_low_furnace_pressure
doc_type: troubleshooting
equipment: [furnace_chamber, induced_draft_fan]
tags: [PT_8313A, PT_8313B, PT_8313C, PT_8313D, PT_8313E, PT_8313F, YFJ3_AI, FT_8301, FT_8302, AIR_8301A, AIR_8301B]
title: Troubleshooting Guide — Excessive Furnace Negative Pressure / Draft Loss
revision: 1.4
date: 2022-01-20
---

# Troubleshooting Guide: Excessive Furnace Negative Pressure

**Document No.:** ZJP-TRB-004  
**Symptom:** PT_8313A–F reading more negative than −200 Pa (excessive draft) OR furnace draft suddenly lost  
**Revision:** 1.4 | **Date:** 2022-01-20

---

## 1. Two Distinct Scenarios

This guide covers two opposite but related conditions:

**A — Excessive draft (too negative):** PT_8313A–F < −200 Pa. Furnace is pulling too hard — cold air infiltrates through expansion joints and access points, reducing combustion efficiency.

**B — Sudden draft loss:** PT_8313A–F rapidly approaching zero or going positive, despite IDF running. This is more urgent and may indicate IDF mechanical failure or duct blockage.

---

## 2. Scenario A: Excessive Draft (PT_8313A–F < −200 Pa)

### 2.1 Causes

| Cause | Indicators | Action |
|-------|-----------|--------|
| IDF setpoint too aggressive | PT_8313 far more negative than setpoint | Adjust furnace_draft_control_loop setpoint from −120 Pa to −100 Pa |
| Low boiler load with IDF at minimum speed | Normal at very low load — less gas generation | Monitor; acceptable if setpoint is met |
| Cold air infiltration causing false draft reading | One or two PT_8313 sensors more negative than others | Verify impulse lines not drafting air; inspect sensor taps |
| IDF overspeed (VFD at maximum with low load) | YFJ3_AI lower than expected at this speed | Reduce IDF speed in manual; re-engage auto with revised setpoint |

### 2.2 Impact of Excessive Draft

- Cold air infiltration: AIR_8301A/B will read artificially high (more O2 from infiltration, not from proper combustion air)
- Reduced furnace temperature: cooling effect from air infiltration lowers TE_8313B
- Heat loss: more gas flow carries more heat out of the furnace → TE_8319A/B rising

### 2.3 Actions

1. If PT_8313A–F average < −200 Pa steadily: reduce IDF speed in manual (−5% per step) until pressure stabilizes at −120 Pa
2. Review furnace_draft_control_loop setpoint: ensure it is not set more negative than −180 Pa
3. If reduced IDF speed causes pressure to recover but AIR_8301A/B remains high: investigate air infiltration sources (expansion joints, access doors)
4. Seal any air infiltration points found during next outage (ZJP-MNT-013)

---

## 3. Scenario B: Sudden Draft Loss (PT_8313A–F Rising Toward Zero)

### 3.1 Immediate Assessment

When PT_8313A–F rising from normal toward −30 Pa or less negative, despite IDF reportedly running:

1. Check YFJ3_AI — is IDF actually consuming current? If YFJ3_AI = 0: IDF has tripped → BPS should trip boiler automatically
2. Check IDF running feedback on DCS — confirm status
3. If IDF running but draft still declining: possible ductwork blockage between furnace and IDF inlet

### 3.2 Causes

| Cause | Indicators | Action |
|-------|-----------|--------|
| IDF tripped | YFJ3_AI = 0, IDF running status = TRIP | BPS trips boiler; investigate IDF trip cause per ZJP-TRB-005/013 |
| Major ductwork blockage (ash fall, refractory collapse) | IDF running at high current but low flow; YFJ3_AI elevated | Reduce load immediately; plan emergency outage for duct inspection |
| IDF damper failure — inlet damper closing | IDF running but reduced flow | Check inlet damper position; override open if stuck |
| Air leakage into ductwork between cyclone and IDF | O2 at AIR_8301A/B suddenly high; no other change | Locate leakage source; temporary sealing if possible |

### 3.3 Actions for Rising Pressure

1. **If IDF confirmed running:** Manually increase IDF speed to 100% — if pressure stabilizes, blockage is downstream of IDF (rare) or there is a sudden major air flow increase upstream
2. **If pressure still rising toward +50 Pa:** Reduce primary and secondary air flow to minimum — less air in = less pressure buildup
3. **If pressure reaches +100 Pa:** Alarm; prepare for ESD
4. **If pressure reaches +200 Pa (2-of-6 sensors):** BPS trips boiler — do NOT fight the trip

---

## 4. Normal Furnace Pressure Operating Range

For reference, the expected normal range at different measurement elevations:

| Elevation | Sensor(s) | Normal Range at Full Load |
|-----------|-----------|--------------------------|
| +22 m (top) | PT_8313A, PT_8313B | −80 to −160 Pa |
| +18 m (mid) | PT_8313C, PT_8313D | −90 to −170 Pa |
| +14 m (lower) | PT_8313E, PT_8313F | −100 to −180 Pa |

The pressure becomes slightly more negative lower in the furnace because the draft column creates a pressure gradient. Deviation from this gradient pattern can indicate uneven combustion, air infiltration, or sensor faults.

---

## 5. Relationship to Other Guides

- For rising furnace pressure (too positive): ZJP-TRB-003 (High Furnace Pressure)
- For IDF mechanical fault: ZJP-TRB-005 (IDF High Vibration), ZJP-TRB-013 (IDF High Current)
- For furnace draft control: ZJP-CTRL-002 (Furnace Draft Control Loop)
