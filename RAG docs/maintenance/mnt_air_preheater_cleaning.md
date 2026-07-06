---
doc_id: mnt_air_preheater_cleaning
doc_type: maintenance
equipment: [primary_air_preheater, secondary_air_preheater]
tags: [TE_8303, TE_8304]
title: Air Preheater Cleaning Procedure (Primary and Secondary)
revision: 1.5
date: 2021-06-01
---

# Maintenance Procedure: Air Preheater Cleaning — Primary and Secondary

**Document No.:** ZJP-MNT-007  
**Revision:** 1.5 | **Date:** 2021-06-01  
**Applicability:** Primary Air Preheater (KQYQ-1) and Secondary Air Preheater (KQYQ-2)  
**Maintenance Type:** Annual (condition-based trigger: TE_8303 or TE_8304 rising trend)  
**Estimated Duration:** 12 hours each (2-person crew)

---

## 1. Scope

Both tubular air preheaters are subject to fouling on the flue gas side by ash deposits and, particularly at the cold end, by sulfuric acid condensation products. This procedure covers external tube cleaning (flue gas side) and inspection of tube integrity.

**Performance trigger:** If TE_8303 or TE_8304 increases > 15°C above the seasonal baseline at equivalent load, schedule cleaning at the next available opportunity.

---

## 2. Isolation Requirements

- [ ] Boiler shutdown and LOTO complete (both fans locked out)
- [ ] Flue gas side: ducting isolation dampers closed and blanked if accessible
- [ ] Air side: fan outlet damper closed and locked
- [ ] Preheater allowed to cool to < 60°C before entering (minimum 8 hours after shutdown)
- [ ] Confined space entry permit required if entering tube bundle cavities (ZJP-SAFE-004)

---

## 3. Inspection Before Cleaning

### 3.1 Flue Gas Side Inspection
Access via inspection doors on the flue gas casing (2 per preheater).

- [ ] Fouling type: dry powdery ash (easy to remove) vs. sticky/caked deposits (harder to remove — indicates SO₃ condensation)
- [ ] Cold-end tubes: check for visible acid corrosion (orange-brown staining, pitting, perforations)
- [ ] Enamel coating (cold end): intact or chipped — record coverage % for each tube bundle
- [ ] Tube bundle clearances: no collapsed or bent tubes obstructing flow passages

### 3.2 Air Side Inspection
- [ ] No cross-contamination (flue gas entering air side) — confirmed by checking for ash on air side tube surfaces
- [ ] Air side tubes: no external scale, clean metal surface

---

## 4. Cleaning Procedure

### 4.1 Dry Ash Deposits (Flue Gas Side)
1. Set up portable air lance (compressed air at 5–7 bar)
2. Insert lance into tube rows from the hot end access door
3. Blow each tube pass systematically — work from top to bottom
4. Collect dislodged ash in hoppers below — dispose per ZJP-ENV-002 (ash disposal)
5. Confirm hopper drain valves open before starting to avoid ash accumulation

### 4.2 Sticky / Caked Deposits
1. Apply light water wash via gentle spray nozzle — do not use high-pressure jet (risk of tube damage)
2. Allow deposits to soften for 30 minutes
3. Follow with compressed air lance per Section 4.1
4. Final rinse: clean water spray
5. Drain all wash water — contains soluble sulfates, dispose as process wastewater

### 4.3 Cold-End Acid Deposits (Sulfate Scale)
If enamel coating is heavily coated with ammonium sulfate or calcium sulfate scale:
1. Apply 10% sodium hydroxide (caustic) solution by brush to affected tubes
2. Allow 15-minute contact time
3. Rinse thoroughly with clean water
4. Inspect enamel coating after cleaning — reseal any chipped areas with acid-resistant epoxy coating

---

## 5. Post-Cleaning Inspection

- [ ] Tubes free of obstruction — confirm by light test (flashlight at one end, visible at other)
- [ ] No perforations (visible holes or cracks in tube walls)
- [ ] Cold-end enamel: coverage > 80% — if below, plan re-coating at next outage
- [ ] Tube thickness UT check on 5% of cold-end tubes — minimum thickness 3.5 mm (design 4.5 mm wall)

---

## 6. Performance Verification After Restart

Within 48 hours of restart at full load, compare TE_8303 and TE_8304 to pre-outage baseline:
- Expected improvement: 10–25°C reduction in outlet flue gas temperature
- If TE_8303/8304 remains at pre-cleaning level: further investigation — possible tube bypass or internal blockage remaining

---

## 7. Sign-Off

**Performed by:** ________________________  
**Date:** ____________  
**Preheater(s) cleaned:** ☐ Primary / ☐ Secondary / ☐ Both  
**Enamel coating condition:** _______%  
**Approval for return to service:** ________________________
