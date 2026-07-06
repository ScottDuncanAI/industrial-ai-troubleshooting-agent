---
doc_id: trb_bed_inventory_loss
doc_type: troubleshooting
equipment: [furnace_lower_hearth, cyclone_separator_left, cyclone_separator_right]
tags: [SXLTCYZ, SXLTCYY, ZCLCCY, YCLCCY, FT_8306A, FT_8306B, TE_8313B, AIR_8301A, AIR_8301B]
title: Troubleshooting Guide — Bed Inventory Loss
revision: 1.8
date: 2022-01-20
---

# Troubleshooting Guide: Bed Inventory Loss

**Document No.:** ZJP-TRB-009  
**Symptom:** SXLTCYZ and/or SXLTCYY declining — hearth differential pressure falling below 1,000 Pa  
**Revision:** 1.8 | **Date:** 2022-01-20

---

## 1. Why Bed Inventory Matters

The circulating fluidized bed requires a minimum mass of solid material (bed material) in the system to:
- Provide thermal mass (heat storage) for stable combustion
- Enable efficient heat transfer between the combustion gases and water walls
- Maintain the "circulating" characteristic — solids cycling through furnace → cyclone → return leg → furnace

If bed inventory falls below the minimum, combustion becomes unstable, steam temperature drops sharply, and the boiler will eventually need to be shut down to recharge bed material.

**Normal bed inventory (ΔP):** SXLTCYZ and SXLTCYY = 1,500–3,000 Pa at full load  
**Alert level:** < 1,000 Pa  
**Emergency level:** < 600 Pa (risk of flame loss, immediate action required)

---

## 2. Immediate Actions

When SXLTCYZ or SXLTCYY < 1,000 Pa:
1. **Do not increase air flow** — excess air fluidization velocity accelerates solid carry-out
2. **Reduce primary air (FT_8301) by 10–15%** — lower fluidization velocity reduces elutriation rate
3. Check ZCLCCY and YCLCCY — are cyclone ΔPs normal? (If cyclone ΔP is also dropping, cyclones may not be returning solids)
4. Check FT_8306A and FT_8306B — return air flows to L-seals (should be 8,000–15,000 m³/h each)
5. Notify supervisor — bed inventory restoration may require shutdown

---

## 3. Probable Causes

### 3.1 Blocked Solid Return Leg (L-Seal) — Most Common

**Description:** The L-seal return leg from one or both cyclones has become blocked (bridging of solids, loss of fluidizing air). Solids are captured by the cyclone but cannot return to the furnace.

**Diagnosis:**
- SXLTCYZ/Y declining
- ZCLCCY or YCLCCY declining (cyclone sees reduced solid loading because bed is depleted upstream)
- FT_8306A or FT_8306B showing low flow (blocked return leg starves return air measurement)
- One cyclone affected before the other (asymmetric — left or right)

**Action:**
1. Increase return air to the affected L-seal (increase FT_8306A or FT_8306B) — attempt to re-fluidize blockage
2. If no response in 5 minutes: the blockage may be mechanical (sintered ash, foreign object)
3. At reduced load, a blocked L-seal may allow sufficient bed inventory on the working side for continued operation, but this is a short-term measure only
4. Plan outage for L-seal inspection and clearing (ZJP-MNT-008)

### 3.2 Excessive Fluidization Velocity — Elutriation

**Description:** Too high a primary air flow causes fine particles to be elutriated (carried out of the bed) faster than cyclones can return them.

**Diagnosis:**
- Occurred after an increase in FT_8301 or FT_8302
- Both SXLTCYZ and SXLTCYY declining symmetrically
- ZCLCCY and YCLCCY high (cyclones receiving more solids)
- AIR_8301A/B may be rising (more excess air)

**Action:**
1. Reduce FT_8301 by 10% — reduce fluidization velocity
2. Allow 20–30 minutes for bed to re-establish with reduced elutriation
3. Once SXLTCYZ/Y stabilizes, carefully rebalance air flows for combustion efficiency

### 3.3 Refractory Failure in Cyclone or Return Leg

**Description:** If cyclone refractory has failed significantly, gas bypasses the cyclone (taking a lower-resistance path), reducing separation efficiency. Solids pass through to the economizer and beyond without returning to the bed.

**Diagnosis:**
- ZCLCCY or YCLCCY suddenly drops (reduced differential pressure — bypass path reduces the flow through the cyclone)
- SXLTCYZ/Y declining as solids are lost
- TE_8319A/B may rise (ash particles in economizer zone)

**Action:**
1. Reduce load — less gas flow reduces the bypass effect
2. Plan outage inspection — cyclone refractory failure requires repair before normal operation (ZJP-MNT-008)

### 3.4 Bed Material Quality Change

**Description:** If coal or ash particle size has changed (finer coal → more fines generated → faster elutriation), bed inventory depletes faster.

**Diagnosis:**
- Gradual trend over days after coal delivery change
- Both cyclone and hearth ΔPs declining slowly

**Action:**
1. Check coal particle size from current delivery vs. design specification
2. If finer coal: reduce primary air velocity target; plan to recharge bed material

---

## 4. Bed Material Recharging

If SXLTCYZ/Y falls below 600 Pa: controlled shutdown is typically necessary. After shutdown:
1. Add fresh bed sand through charging ports: 5–10 tonnes depending on inventory loss
2. Bed sand specification: silica sand, 0.2–0.4 mm particle size, < 1% fines content
3. After recharging: restart per ZJP-SOP-001 (cold start) with gradual warm-up

---

## 5. Prevention

- Monitor SXLTCYZ and SXLTCYY on DCS trend (1-hour trending scale is ideal for catching slow decline)
- Review ZCLCCY and YCLCCY together — asymmetry early identifies a single blocked return leg
- After any change in coal source or particle size, increase monitoring frequency for first 48 hours
