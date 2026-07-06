---
doc_id: safe_water_chemistry_specs
doc_type: safety
equipment: [steam_drum, economizer]
tags: [PTCA_8322A, TE_8332A]
title: Boiler Feedwater Chemistry Specifications and Treatment
revision: 2.2
date: 2021-09-01
---

# Boiler Feedwater Chemistry Specifications and Treatment

**Document No.:** ZJP-CHEM-001  
**Revision:** 2.2 | **Date:** 2021-09-01  
**Applicability:** Unit 1 — 9.81 MPa / 540°C CFB Boiler

---

## 1. Why Water Chemistry Matters

Poor feedwater chemistry causes:
- **Corrosion** of economizer, drum, and tube internals → tube failures and leaks
- **Scale deposits** on tube inner surfaces → overheating and tube rupture (scale is an insulator)
- **Steam contamination** → deposits on superheater tubes and turbine/process equipment
- **Pitting** during lay-up → accelerated metal loss

At 9.81 MPa operating pressure, water chemistry requirements are stringent — even minor contamination can cause significant damage over months of operation.

---

## 2. Feedwater Specifications (At Economizer Inlet)

| Parameter | Specification | Test Frequency |
|-----------|-------------|----------------|
| pH (at 25°C) | 9.0–9.5 | Daily |
| Dissolved oxygen (DO) | < 7 ppb | Daily |
| Total hardness (as CaCO₃) | < 2 µg/kg | Daily |
| Total dissolved solids (TDS) | < 100 µg/kg | Daily |
| Iron (Fe) | < 20 µg/kg | Weekly |
| Copper (Cu) | < 5 µg/kg | Weekly |
| Silica (SiO₂) | < 20 µg/kg | Weekly |
| Conductivity (specific) | < 0.3 µS/cm | Daily (online) |
| Oil/grease | Non-detectable | Weekly (or on suspicion) |

---

## 3. Boiler Water Specifications (Steam Drum Sample)

| Parameter | Specification | Test Frequency |
|-----------|-------------|----------------|
| pH (at 25°C) | 9.5–10.5 | Daily |
| Total dissolved solids (TDS) | < 2,000 µg/kg | Daily (via conductivity) |
| Phosphate (PO₄, as Na₃PO₄ treatment) | 5–15 mg/L | Daily |
| Silica (SiO₂) | < 1.5 mg/L | Daily |
| Conductivity (specific) | < 30 µS/cm | Continuous (online) |
| Sodium (Na) | < 200 µg/kg | Weekly |

---

## 4. Steam Purity Specifications (Outlet)

| Parameter | Specification | Test Frequency |
|-----------|-------------|----------------|
| Sodium (Na) | < 10 µg/kg | Weekly |
| Silica (SiO₂) | < 20 µg/kg | Weekly |
| Iron (Fe) | < 20 µg/kg | Monthly |
| Conductivity (at 25°C, cation conductivity) | < 0.3 µS/cm | Continuous (online) |

---

## 5. Chemical Treatment Program

The boiler water treatment program uses two chemical dosing streams:

### 5.1 Oxygen Scavenger (Deaerator Outlet)
- **Chemical:** Sodium sulfite (Na₂SO₃) or Hydrazine (N₂H₄) — confirm with water treatment supplier
- **Dosing point:** Deaerator outlet/boiler feedwater pump suction
- **Target DO in feedwater:** < 7 ppb
- **Typical dosing rate:** 3–5 mg/L as Na₂SO₃ (excess)

### 5.2 Alkalinity/Phosphate Treatment (Steam Drum)
- **Chemical:** Trisodium phosphate (Na₃PO₄)
- **Dosing point:** Direct drum injection via chemical dosing pump
- **Purpose:** pH control, scale prevention (converts hardness to sludge), corrosion inhibition
- **Target phosphate:** 5–15 mg/L in drum water

---

## 6. Blowdown for TDS Control

Blowdown removes dissolved solids that concentrate in the drum water as steam is generated. Two types:

### 6.1 Continuous Blowdown
- Location: Steam drum, near water surface (removes highest-TDS water)
- Rate: adjusted to maintain drum water TDS < 2,000 µg/kg
- Typical rate: 1–3% of steam flow (1.3–3.9 t/h)
- Heat recovery: blowdown routed to heat recovery vessel (not discharged directly)

### 6.2 Intermittent (Manual) Blowdown
Per ZJP-CHEM-002 (Blowdown Procedure):
- Frequency: every 8 hours (3× per day)
- Duration: 30 seconds per blowdown valve
- Location: Steam drum bottom (removes settled sludge)
- Timing: do not blow down during rapid load changes

---

## 7. Out-of-Specification Actions

| Parameter | Out-of-Spec Condition | Action |
|-----------|----------------------|--------|
| pH < 8.5 | Low — corrosion risk | Increase Na₃PO₄ dosing; notify chemistry team immediately |
| DO > 15 ppb | High — pitting risk | Increase oxygen scavenger; check deaerator operation |
| TDS > 3,000 µg/kg | High — carryover risk | Increase blowdown rate; notify chemistry team |
| Silica > 2 mg/L | High — deposition risk | Increase blowdown; reduce load if not resolving |
| Oil detected | Contamination | Stop boiler immediately — oil contamination causes severe carryover and fire risk |

---

## 8. Lay-Up Chemistry

For planned outages:

### Short Outage (< 2 weeks): Wet Lay-Up
- Fill drum to normal level with treated, deoxygenated water (DO < 5 ppb)
- Add nitrogen blanket over drum (0.05 MPa positive pressure) to prevent air ingress
- Maintain water chemistry within normal specifications
- Check weekly during lay-up

### Long Outage (> 2 weeks): Dry Lay-Up
- Drain, flush, and dry all pressure parts
- Place silica gel or moisture absorbing desiccant inside drum
- Seal all nozzles with blanks
- Inspect monthly for moisture ingress

---

## 9. Revision History

| Rev | Date | Change |
|-----|------|--------|
| 1.0 | 2019-03-01 | Initial issue |
| 2.0 | 2021-03-01 | Silica limits revised per OEM recommendation after HTSH tube inspection finding |
| 2.2 | 2021-09-01 | Added oil contamination emergency action |
