---
doc_id: trb_cyclone_dp_abnormal
doc_type: troubleshooting
equipment: [cyclone_separator_left, cyclone_separator_right, furnace_lower_hearth]
tags: [ZCLCCY, YCLCCY, SXLTCYZ, SXLTCYY, FT_8306A, FT_8306B]
title: Troubleshooting Guide — Cyclone Separator Abnormal Differential Pressure
revision: 1.5
date: 2022-01-20
---

# Troubleshooting Guide: Cyclone Separator Abnormal Differential Pressure

**Document No.:** ZJP-TRB-010  
**Symptom:** ZCLCCY or YCLCCY outside normal range (600–1,200 Pa) or left-right divergence > 400 Pa  
**Revision:** 1.5 | **Date:** 2022-01-20

---

## 1. Normal Cyclone Operation

At full load:
- ZCLCCY (left cyclone): 700–1,100 Pa
- YCLCCY (right cyclone): 700–1,100 Pa
- Left-right difference: < 200 Pa (symmetric design)

---

## 2. Abnormally Low Cyclone ΔP

### Causes:
- **Low boiler load:** Normal — less gas flow = lower ΔP
- **Refractory failure creating bypass:** Gas finds lower-resistance path around the cyclone vortex — ΔP drops suddenly
- **Solid return leg fully blocked:** No solids circulation, so solids loading in gas decreases over time → cyclone ΔP falls
- **Cyclone vortex finder heavily eroded:** Loss of centrifugal efficiency; gas bypasses at finder tip

**Diagnosis:**
- Low ΔP at normal load with SXLTCYZ/Y also declining: likely blocked return leg or refractory failure
- Low ΔP with SXLTCYZ/Y stable: may be low solids loading (less coal, less ash generation)

**Actions:** See ZJP-TRB-009 (Bed Inventory Loss) for blocked return leg. For refractory failure: reduce load and plan outage.

---

## 3. Abnormally High Cyclone ΔP

### Causes:
- **Excessive solids loading:** High coal feed rate or high bed inventory → cyclones overloaded
- **Partially blocked vortex finder outlet:** Ash bridging at top of cyclone inner tube
- **High flue gas density / temperature issue**

**Symptoms:** ZCLCCY and/or YCLCCY > 1,800 Pa at normal load.

**Actions:**
1. If both cyclones high simultaneously: reduce coal feed rate slightly; monitor if ΔP stabilizes
2. If one cyclone high and one normal: vortex finder blockage on the high-reading cyclone — reduce load; plan outage for inspection

---

## 4. Left-Right Divergence (> 400 Pa)

This is the most operationally important pattern to recognize.

### Causes:
- **One return leg blocked:** The cyclone on the blocked side appears more loaded (ΔP may be higher) while the bed depletes only on that side
- **Uneven gas distribution:** One side of furnace running hotter/with more air → more gas to one cyclone
- **One ΔP transmitter fault:** Verify by checking ZCLCCY and YCLCCY independently

**Actions:**
1. Compare SXLTCYZ (left hearth ΔP) and SXLTCYY (right hearth ΔP) — if one side depleting faster, confirms that side's return leg is blocked
2. Increase return air on the affected side (FT_8306A or FT_8306B)
3. If imbalance persists, reduce load and plan inspection

---

## 5. Instrument Validity Check

With cyclones at known steady load, ZCLCCY and YCLCCY should track smoothly. Erratic, high-frequency oscillation on one transmitter (while the other is stable) indicates a partially blocked impulse line — blow through the impulse line at next opportunity.

---

## 6. Escalation

If ZCLCCY or YCLCCY drops to < 200 Pa at > 80% boiler load: this indicates severe cyclone bypass — significant fly ash is escaping to the economizer and beyond. This will rapidly cause bed inventory loss and potential ash overloading of the economizer. Reduce load to < 60% and plan outage within 24 hours.
