---
doc_id: ds_low_temp_superheater
doc_type: datasheet
equipment: [low_temp_superheater]
tags: []
title: Equipment Datasheet — Low Temperature Superheater
revision: 1.1
date: 2020-08-01
---

# Equipment Datasheet — Low Temperature Superheater (LTSH)

**Document No.:** ZJP-DS-009  
**Equipment Tag:** LTSH-1  
**P&ID Reference:** P&ID-8300-011  
**Revision:** 1.1 | **Date:** 2020-08-01

---

## 1. Equipment Description

The Low Temperature Superheater (LTSH) is the first superheating stage. It receives saturated steam from the steam drum and raises it above the saturation point by absorbing heat from the flue gas passing through the boiler backpass. Steam exits the LTSH and enters the primary desuperheater for temperature trimming before proceeding to the high temperature superheater.

**System:** Steam Generation & Superheating System  
**Criticality:** High

---

## 2. Design Specifications

| Parameter | Value |
|-----------|-------|
| Type | Counter-flow, pendant (hanging) tube bank |
| Manufacturer | Jiangnan Boiler Co., Ltd. |
| Tube Material | SA-213 T12 (Cr-Mo alloy steel) |
| Tube OD / Wall | 42 mm / 5.5 mm |
| Number of Tubes | 240 (12 rows × 20 tubes per row) |
| Heat Transfer Area | 1,250 m² |
| Steam Inlet (from drum) | Saturated, 311°C at 9.8 MPa |
| Steam Outlet (design) | 430°C at 9.6 MPa |
| Flue Gas Inlet Temperature | 580–640°C |
| Flue Gas Outlet Temperature | 420–460°C |
| Design Pressure (steam side) | 11.0 MPa |
| Design Temperature (tube metal) | 460°C maximum |
| Expected Tube Metal Temperature | 430–445°C (normal operation) |

---

## 3. Temperature Monitoring

No direct steam temperature sensor is located at the LTSH outlet in the standard instrumentation set. Steam temperature is inferred from the desuperheater behavior:
- **TV_8329ZC nearly closed (< 10%)** and TE_8332A low: LTSH or desuperheater outlet temperature is low — suspect low firing rate, excess desuperheating
- **TV_8329ZC wide open (> 80%)** with TE_8332A still low: LTSH outlet temperature may be low — check flue gas temperature at this level

The absence of a direct LTSH outlet thermocouple is a known instrumentation gap — consider adding during next capital outage.

---

## 4. Tube Failure Modes

| Failure Mode | Cause | Early Indicators |
|-------------|-------|-----------------|
| Long-term overheating (creep) | Tube metal temperature chronically too high | Swelling visible on tube OD, wall thinning on UT |
| Short-term overheating | Steam flow stoppage (e.g., blocked drain) | Rapid temperature spike, tube rupture |
| Corrosion (flue gas side) | High sulfur coal, low temperature acidic deposits | Wall thinning, pitting on external surface |
| Erosion | High fly ash loading, high gas velocity | Uniform thinning on leading face of tubes |

---

## 5. Maintenance Schedule

| Task | Frequency | Reference |
|------|-----------|-----------|
| External visual inspection | Annual | ZJP-MNT-011 |
| Tube UT thickness survey (selected) | Annual | ZJP-MNT-011 |
| Sootblower operation (online) | Daily | Normal operations |

---

## 6. Revision History

| Rev | Date | Description |
|-----|------|-------------|
| 1.0 | 2019-03-01 | Initial issue |
| 1.1 | 2020-08-01 | Added note on instrumentation gap (no LTSH outlet thermocouple) |
