---
doc_id: ds_high_temp_superheater
doc_type: datasheet
equipment: [high_temp_superheater]
tags: [TE_8332A]
title: Equipment Datasheet — High Temperature Superheater
revision: 1.2
date: 2020-08-01
---

# Equipment Datasheet — High Temperature Superheater (HTSH)

**Document No.:** ZJP-DS-011  
**Equipment Tag:** HTSH-1  
**P&ID Reference:** P&ID-8300-013  
**Revision:** 1.2 | **Date:** 2020-08-01

---

## 1. Equipment Description

The High Temperature Superheater (HTSH) is the final superheating stage. Steam enters from the primary desuperheater at approximately 510–520°C and is heated to the target outlet temperature of 540°C. The HTSH tubes are exposed to the highest flue gas temperatures in the convective backpass and operate closest to their design metal temperature limits. TE_8332A, the primary KPI for the entire boiler, measures the final steam temperature at the HTSH outlet.

**System:** Steam Generation & Superheating System  
**Criticality:** High — tube overheating can cause rapid failure

---

## 2. Design Specifications

| Parameter | Value |
|-----------|-------|
| Type | Counter-flow, pendant tube bank |
| Manufacturer | Jiangnan Boiler Co., Ltd. |
| Tube Material | SA-213 T91 (9Cr-1Mo-V alloy steel) |
| Tube OD / Wall | 42 mm / 6.0 mm |
| Number of Tubes | 160 |
| Heat Transfer Area | 820 m² |
| Steam Inlet Temperature | 510–520°C |
| Steam Outlet Temperature (design) | 540°C |
| Steam Pressure at Outlet | 9.5 MPa |
| Design Pressure | 10.8 MPa |
| Maximum Allowable Metal Temperature | 600°C |
| Normal Tube Metal Temperature | 560–580°C |
| Flue Gas Inlet Temperature | 760–830°C |
| Flue Gas Outlet Temperature | 580–640°C |

T91 material is used for its superior creep resistance at elevated temperatures. It requires post-weld heat treatment (PWHT) for all weld repairs.

---

## 3. Steam Outlet Temperature — TE_8332A

| Parameter | Value |
|-----------|-------|
| Instrument Tag | TE_8332A |
| Description | Boiler outlet steam temperature — PRIMARY KPI |
| Measurement Type | Type K thermocouple with thermowell |
| Normal Operating Range | 530–545°C |
| Low Alarm | 528°C |
| High Alarm | 548°C |
| High-High Alarm | 558°C |
| High-High Trip (BPS) | 565°C |
| Units | °C |

TE_8332A is the most important single measurement in the entire historian dataset. It integrates the effects of combustion intensity, air flow, steam flow, and desuperheater operation.

---

## 4. Tube Failure Modes and Warning Signs

| Failure Mode | Cause | Warning Sign |
|-------------|-------|-------------|
| Creep rupture | Long-term metal overtemperature | TE_8332A > 548°C sustained; tube swelling visible |
| Short-term overheating | Loss of steam flow through tube (blocked, low load) | Rapid TE_8332A spike |
| Fireside corrosion | Reducing atmosphere at tube surface | High sulfur deposit, metal wastage on downstream face |
| Erosion by fly ash | High ash loading, high gas velocity | Uniform thinning on leading tube faces |
| Thermal fatigue | Frequent desuperheater water injection onto tubes | Circumferential cracking near nozzle entry |

---

## 5. Operating Limits

| Condition | Limit | Action |
|-----------|-------|--------|
| TE_8332A > 548°C | High | Open TV_8329ZC; reduce firing if no improvement |
| TE_8332A > 558°C | High-High | Manual intervention; reduce load significantly |
| TE_8332A > 565°C | Trip | BPS automatic trip |
| TE_8332A < 528°C | Low | Increase firing; check desuperheater not stuck open |

---

## 6. Maintenance Schedule

| Task | Frequency | Reference |
|------|-----------|-----------|
| External visual inspection | Annual | ZJP-MNT-011 |
| Tube UT thickness measurement (all leading rows) | Annual | ZJP-MNT-011 |
| TE_8332A calibration and thermowell inspection | 6 months | Instrument maintenance |
| Metallurgical sampling (replica) if creep suspected | As indicated | Specialist |

---

## 7. Revision History

| Rev | Date | Description |
|-----|------|-------------|
| 1.0 | 2019-03-01 | Initial issue |
| 1.2 | 2020-08-01 | Thermal fatigue failure mode added after desuperheater inspection finding (Rev 1.3 of DESUP-1 datasheet) |
