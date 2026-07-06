---
doc_id: mnt_secondary_fan_inspection
doc_type: maintenance
equipment: [secondary_fan]
tags: [FT_8302]
title: Secondary Fan Annual Inspection and Flow Calibration
revision: 1.2
date: 2021-05-15
---

# Maintenance Procedure: Secondary Fan Annual Inspection and Flow Calibration

**Document No.:** ZJP-MNT-006  
**Revision:** 1.2 | **Date:** 2021-05-15  
**Applicability:** Unit 1 Secondary Fan (YFJ2)  
**Maintenance Type:** Annual Outage  
**Estimated Duration:** 5 hours

---

## 1. Scope

Annual inspection of the secondary fan and calibration of FT_8302. This procedure mirrors ZJP-MNT-005 (Primary Fan) — the two fans are similar in design. Both should be completed in the same outage window.

---

## 2. Isolation

- [ ] LOTO per ZJP-SAFE-003
- [ ] Outlet damper blocked in closed position
- [ ] Motor isolated and locked at MCC

---

## 3. Bearing Inspection

Secondary fan bearings: same criteria as primary fan (ZJP-MNT-005, Section 3).

- Grease type: Shell Gadus S2 V100 2 or equivalent
- Quantity: 120 g per housing (slightly smaller housing than primary)
- Replace if radial clearance > 0.30 mm or any visible damage found

---

## 4. Impeller and Casing Inspection

Secondary air handles preheated air from the secondary air preheater — slightly warmer than primary fan inlet but still clean air. Main wear mechanism is erosion at secondary air injection ports if fans surge during abnormal operations.

- [ ] Blade inspection: same criteria as primary fan
- [ ] Casing wear plates: check for erosion at blade tips (tip clearance should be 2–4 mm; > 8 mm indicates casing wear)
- [ ] Outlet ducting: no cracks or distortion from thermal cycling

---

## 5. Damper Inspection

- [ ] Full travel test: 0–100%, confirmed in DCS
- [ ] Actuator: no air leak (pneumatic actuator) or oil leak (hydraulic)
- [ ] Damper seals: replace if leakage > 5% at closed position during purge test

---

## 6. Flow Instrument Verification — FT_8302

Same procedure as FT_8301 (ZJP-MNT-005, Section 6).

Normal FT_8302 at various loads:
| Load | Expected FT_8302 |
|------|-----------------|
| 100% | 72,000–80,000 m³/h |
| 75% | 58,000–67,000 m³/h |
| 50% | 44,000–53,000 m³/h |

---

## 7. Coordination Note

Primary and secondary fans should always be returned to service together. Operating with one fan significantly derated requires an immediate rebalancing of primary-to-secondary air split — notify control room before restarting only one fan.

---

## 8. Sign-Off

**Performed by:** ________________________  
**Date:** ____________  
**Bearings replaced:** ☐ Yes / ☐ No  
**FT_8302 calibrated:** ☐ Yes / ☐ No  
**Approval:** ________________________
