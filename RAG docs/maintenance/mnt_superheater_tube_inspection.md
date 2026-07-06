---
doc_id: mnt_superheater_tube_inspection
doc_type: maintenance
equipment: [low_temp_superheater, high_temp_superheater]
tags: [TE_8332A]
title: Superheater Tube Inspection — Low Temp and High Temp
revision: 1.4
date: 2021-06-15
---

# Maintenance Procedure: Superheater Tube Inspection

**Document No.:** ZJP-MNT-011  
**Revision:** 1.4 | **Date:** 2021-06-15  
**Applicability:** Low Temperature Superheater (LTSH-1) and High Temperature Superheater (HTSH-1)  
**Maintenance Type:** Annual Outage  
**Estimated Duration:** 16 hours (2-person crew, both superheaters)

---

## 1. Scope

Superheater tubes are among the highest-risk pressure parts in the boiler. LTSH tubes operate at ~430°C; HTSH tubes at 560–580°C metal temperature. Both are subject to fly ash erosion externally and potential overheating or corrosion internally. TE_8332A (the primary KPI) is directly determined by the heat transfer performance of these two heat exchangers.

---

## 2. Isolation

- [ ] Boiler depressurized — PTCA_8322A at 0 kPa, PTCA_8324 at 0 kPa
- [ ] Superheater steam side drained via header drain valves — confirm drains flowing to drain pot
- [ ] Flue gas side cooled to < 60°C before entering backpass
- [ ] No LOTO required for inspection (passive equipment) but fan LOTO must be in place (fans off)

---

## 3. Access

LTSH and HTSH are pendant tube banks in the boiler backpass. Access is from the backpass casing inspection doors (4 doors per superheater, two sides). Do not open more than 2 doors simultaneously to maintain structural integrity of the casing.

---

## 4. HTSH Inspection (Inspect First — Highest Risk)

### 4.1 Tube Surface Condition — Leading Rows
The first 3 tube rows (facing incoming flue gas) have the highest erosion rate from fly ash.

Measure UT tube wall thickness at:
- Leading edge of each tube in rows 1, 2, and 3
- Mid-span
- Return bends at top and bottom headers

Record minimum measured thickness for each row:
| Row | Design Thickness | Minimum Acceptable | Minimum Measured |
|-----|-----------------|-------------------|-----------------|
| Row 1 | 6.0 mm | 4.0 mm | _______ mm |
| Row 2 | 6.0 mm | 4.2 mm | _______ mm |
| Row 3 | 6.0 mm | 4.5 mm | _______ mm |

Any tube below the minimum acceptable thickness must be plugged or replaced before restart.

### 4.2 Tube Swelling
Walk the length of each tube visually — any visible bulging or swelling (diameter increase > 2%) indicates creep from overtemperature. Swollen tubes require immediate condemnation and replacement. Record exact location and send section for metallurgical analysis.

### 4.3 Fireside Deposits
Heavy dark deposits on tube surfaces indicate:
- High iron sulfide: reducing atmosphere at tube — risk of fireside corrosion
- White/gray ash: normal coal ash — clean with air lance

### 4.4 Header Welds
Inspect header nozzle welds (tube-to-header connections) using MT or PT on the accessible external surface. These are the highest-stress weld locations.

---

## 5. LTSH Inspection

Same methodology as HTSH but less critical — LTSH operates at lower temperature (T12 material):

| Row | Design Thickness | Minimum Acceptable | Minimum Measured |
|-----|-----------------|-------------------|-----------------|
| Row 1 | 5.5 mm | 3.5 mm | _______ mm |
| Row 2 | 5.5 mm | 3.8 mm | _______ mm |
| Row 3+ | 5.5 mm | 4.0 mm | _______ mm |

Check for cracking at tube bends (thermal fatigue from desuperheater water injection — see ZJP-DS-010 note).

---

## 6. Relationship to TE_8332A

If TE_8332A has been trending low at constant load without a corresponding increase in desuperheater water flow (YJJWSLL), this may indicate:
- Increased fouling on HTSH tube external surfaces (lower heat transfer)
- Reduced flue gas temperature entering HTSH (upstream heat sink increase)

Conversely, if TE_8332A runs consistently high with TV_8329ZC nearly closed, inspect LTSH for flow restriction (internal deposit or blockage reducing steam flow through LTSH).

---

## 7. Post-Inspection Actions

| Finding | Action |
|---------|--------|
| Tube below minimum thickness | Plug header nozzle (approved plug PN: ZJP-HTSH-PL-01) or replace tube |
| Swelling detected | Condemn tube section, metallurgical sample, identify root cause |
| Weld crack confirmed | UT sizing, weld repair per WPS-ZJP-003 (T91 welding procedure) |
| Heavy deposits | Air lance clean; if bonded, water wash |

Tube plugging or weld repair requires boiler engineer sign-off and hydrotest before restart.

---

## 8. Sign-Off

**Inspection performed by:** ________________________  
**Date:** ____________  
**HTSH minimum tube thickness found:** _______ mm (location: ________________________)  
**LTSH minimum tube thickness found:** _______ mm (location: ________________________)  
**Tubes plugged or replaced:** ☐ Yes (number/locations on attached sketch) / ☐ No  
**Hydrotest performed after repair:** ☐ Yes / ☐ Not required  
**Engineer approval:** ________________________
