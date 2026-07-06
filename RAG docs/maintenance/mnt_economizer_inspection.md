---
doc_id: mnt_economizer_inspection
doc_type: maintenance
equipment: [economizer]
tags: [TE_8319A, TE_8319B, AIR_8301A, AIR_8301B]
title: Economizer Tube Inspection and Hydrotest
revision: 1.3
date: 2021-06-01
---

# Maintenance Procedure: Economizer Tube Inspection and Hydrotest

**Document No.:** ZJP-MNT-009  
**Revision:** 1.3 | **Date:** 2021-06-01  
**Applicability:** Upper Economizer (ECO-1)  
**Maintenance Type:** Annual Outage  
**Estimated Duration:** 10 hours (inspection) + 6 hours if hydrotest required

---

## 1. Scope

The economizer is subject to fly ash erosion on the outside of tubes and oxygen-induced corrosion on the inside (water side) during lay-up. Annual inspection includes external tube condition assessment and internal hydrostatic pressure test if any tube damage is suspected.

---

## 2. Isolation

- [ ] Boiler shutdown and depressurized
- [ ] Feedwater isolation valve closed at economizer inlet and outlet — both sides blinded if hydrotest planned
- [ ] Flue gas side: cooled to < 50°C before entry (minimum 16 hours after shutdown)
- [ ] Drain economizer water side via drain valves at bottom headers
- [ ] Drain valve open — leave open until fully drained and confirmed dry

---

## 3. External Tube Inspection (Flue Gas Side)

Access through economizer casing access doors (4 levels).

### 3.1 Erosion Assessment
Fly ash erosion is most severe at:
- Tube bends (return bends at each pass end)
- Leading tube rows on each pass
- Areas downstream of any flow disturbances (missing baffles, supports)

For each inspection level, record:
- [ ] Worst-case tube thinning location: ________________________
- [ ] Estimated remaining thickness at worst location (UT): _______ mm
- [ ] Number of tubes with visible thinning (pit depth > 1 mm): _______

**Acceptance criteria:**
| Remaining Wall Thickness | Action |
|--------------------------|--------|
| > 3.5 mm (≥ 78% of design) | Acceptable |
| 2.8–3.5 mm | Monitor — plan replacement within 2 years |
| < 2.8 mm | Replace tubes before restart |

### 3.2 Ash Deposit Condition
- [ ] Loose ash: blow clear with compressed air
- [ ] Bonded deposits (sticky or fused): record location and thickness — may require water washing
- [ ] Deposit thickness > 10 mm: sootblowing frequency increase required

### 3.3 Support System
- [ ] Tube-to-tube spacers: intact, no missing
- [ ] Casing support lugs: no cracking or distortion
- [ ] Expansion bends: no cracking at tube bends

---

## 4. Internal (Water Side) Inspection

Remove one tube during every 3-year inspection cycle for internal section examination:
- [ ] Internal surface: uniform oxide layer acceptable; pitting > 0.5 mm deep requires water chemistry investigation
- [ ] Scale thickness: > 0.5 mm of iron scale indicates oxygen corrosion — review lay-up procedure (ZJP-CHEM-001)
- [ ] Record tube OD, ID, and wall thickness at 3 locations — compare to original drawings

---

## 5. O2 Analyzer Access Ports (AIR_8301A and AIR_8301B)

Located at the economizer inlet duct (flue gas side):
1. Remove each O2 analyzer probe for cleaning
2. Check probe tip for ash plugging — clean with compressed air and probe cleaning kit
3. Replace O2 analyzer reference filter if due (per manufacturer schedule — typically annual)
4. Reinstall and perform zero/span calibration before restart

---

## 6. Hydrostatic Pressure Test (If Required)

Hydrotest is required if any of the following occurred since the last test:
- Tube leak or suspected tube failure
- Any tube weld repair performed
- Tube wall thickness below 80% of design found during UT

**Test procedure:**
1. Isolate economizer water side — close inlet/outlet valves and install blinds
2. Fill with clean treated water — purge all air via vent connections
3. Pressurize to 1.25 × design pressure = **15.6 MPa** using high-pressure pump
4. Hold for 30 minutes — no visible leaks, no pressure drop > 0.05 MPa
5. Depressurize slowly — minimum 30 minutes to atmospheric
6. Drain fully before reinstalling insulation

**Acceptance criterion:** Zero leakage at test pressure for the 30-minute hold period.

---

## 7. Sign-Off

**Performed by:** ________________________  
**Date:** ____________  
**Minimum tube thickness found:** _______ mm at ________________________  
**Tubes replaced:** ☐ Yes (number: ___, locations on attached sketch) / ☐ No  
**Hydrotest performed:** ☐ Yes (result: ☐ Pass / ☐ Fail) / ☐ Not required  
**AIR_8301A/B probes cleaned and calibrated:** ☐ Yes  
**Approval:** ________________________
