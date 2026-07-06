---
doc_id: mnt_primary_fan_inspection
doc_type: maintenance
equipment: [primary_fan]
tags: [FT_8301]
title: Primary Fan Annual Inspection and Flow Calibration
revision: 1.3
date: 2021-05-15
---

# Maintenance Procedure: Primary Fan Annual Inspection and Flow Calibration

**Document No.:** ZJP-MNT-005  
**Revision:** 1.3 | **Date:** 2021-05-15  
**Applicability:** Unit 1 Primary Fan (YFJ1)  
**Maintenance Type:** Annual Outage  
**Estimated Duration:** 6 hours

---

## 1. Scope

Annual inspection of the primary fan including bearing check, impeller inspection, outlet damper verification, and flow instrument calibration for FT_8301.

---

## 2. Isolation

- [ ] LOTO per ZJP-SAFE-002
- [ ] Outlet damper mechanically blocked in closed position (prevents back-flow from pressurized furnace)
- [ ] Motor isolated at MCC and locked

---

## 3. Bearing Inspection

Primary fan bearings are less heavily loaded than IDF bearings (lower fly ash content in clean inlet air). Inspection is visual and tactile during first year of service; bearing replacement on condition (or every 3 years whichever is sooner).

- [ ] Remove bearing housing covers
- [ ] Inspect bearings visually (see ZJP-MNT-003 criteria)
- [ ] Check radial clearance with feeler gauge — replace if > 0.35 mm
- [ ] Inspect grease condition (grease-lubricated bearings): no discoloration, no hardening
- [ ] Regrease with specified grease (Shell Gadus S2 V100 2 or equivalent, 150 g per housing)

---

## 4. Impeller Inspection

Primary fan handles clean ambient air — erosion is minimal compared to IDF. However:
- [ ] Inspect for any build-up of sticky material (coal dust, oil mist) on blades — clean if present
- [ ] Inspect blade root welds for cracking (especially if fan has operated in surge condition)
- [ ] Check impeller hub set-screws and keyway — no fretting or movement

---

## 5. Outlet Damper Inspection

The outlet damper is the primary flow control element for FT_8301.

- [ ] Damper blades: no warping, cracking, or ash buildup that would prevent full travel
- [ ] Damper actuator: full travel test (0–100%) with position feedback verified in DCS
- [ ] Damper seal strips: replaced if worn (wear causes air leakage at low damper positions)
- [ ] Confirm closed position = 0% and fully open position = 100% on DCS signal

---

## 6. Flow Instrument Verification — FT_8301

FT_8301 uses a pitot tube. Accuracy can drift if the pitot tube is partially blocked by condensed moisture or ash accumulation.

1. Remove pitot tube from service port (retractable design)
2. Inspect pitot tube tip — clean with compressed air and wire brush if needed
3. Verify differential pressure transmitter zero — with zero flow, should read ≤ 2 Pa
4. Reinstall pitot tube — confirm reading matches pre-outage trend at equivalent conditions within ±5%
5. If zero or span is out of calibration: recalibrate against portable pitot traverse

Normal FT_8301 at various loads:
| Load | Expected FT_8301 |
|------|-----------------|
| 100% | 125,000–135,000 m³/h |
| 75% | 100,000–112,000 m³/h |
| 50% | 78,000–88,000 m³/h |

---

## 7. Post-Maintenance Test

1. Start primary fan in local control — confirm direction of rotation
2. Confirm FT_8301 increases linearly with damper opening
3. Full load run at 100% damper for 15 minutes — confirm no abnormal vibration or heat
4. Verify DCS FT_8301 reading matches expected flow at current furnace conditions

**Acceptance criterion:** No vibration or heat issues; FT_8301 within ±5% of expected at each test point.

---

## 8. Sign-Off

**Performed by:** ________________________  
**Date:** ____________  
**Bearings replaced:** ☐ Yes / ☐ No  
**FT_8301 calibrated:** ☐ Yes / ☐ No (no drift found)  
**Approval:** ________________________
