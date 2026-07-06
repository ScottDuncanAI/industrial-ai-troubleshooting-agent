---
doc_id: mnt_idf_motor_inspection
doc_type: maintenance
equipment: [induced_draft_fan]
tags: [YFJ3_AI]
title: IDF Motor Inspection and Current Check
revision: 1.2
date: 2021-05-10
---

# Maintenance Procedure: IDF Motor Inspection and Current Check

**Document No.:** ZJP-MNT-003B  
**Revision:** 1.2 | **Date:** 2021-05-10  
**Applicability:** Unit 1 IDF Motor (1,800 kW, 6 kV)  
**Maintenance Type:** Annual Outage  
**Estimated Duration:** 6 hours (electrical team)

---

## 1. Scope

Annual inspection of the IDF motor including: insulation resistance testing, winding inspection, coupling and alignment check, terminal box inspection, and VFD interface verification. Motor current during operation is monitored continuously via YFJ3_AI.

---

## 2. Safety Requirements

- IDF fully isolated per LOTO ZJP-SAFE-001
- High-voltage work: qualified HV electrician required (6 kV)
- Electrical lock applied at 6 kV switchgear — key retained by electrical supervisor
- VFD DC bus discharged before opening VFD cabinet (minimum 15-minute discharge time after power off)

---

## 3. Insulation Resistance Test (Megger Test)

Perform insulation resistance (IR) test with 1,000 V megger (stator winding to earth):

| Test | Minimum Acceptable IR | Notes |
|------|----------------------|-------|
| Cold IR (at ambient) | > 100 MΩ | Measured after LOTO, before any work |
| After cleaning and heating (if done) | > 200 MΩ | |
| Polarization Index (PI = IR at 10 min / IR at 1 min) | > 2.0 | PI < 2.0 indicates contamination |

Record: Cold IR = _______ MΩ, PI = _______

If IR < 50 MΩ: do not return to service — notify electrical engineer for winding assessment.

---

## 4. Visual Inspection

- [ ] Motor stator winding end-turns: no visible charring, cracking, or moisture damage (access via bearing housings end covers if removable without full teardown)
- [ ] Terminal box: clean, dry, no carbonization on terminal blocks, all connections torqued to specification
- [ ] Motor frame: no cracks, no missing cooling fin sections
- [ ] Space heaters: verify operational (resistance check between heater terminals)
- [ ] Cooling fan guard: intact, no obstruction to airflow

---

## 5. Motor Current Reference — YFJ3_AI

Normal operating current at various load levels:

| Boiler Load | Expected YFJ3_AI |
|------------|-----------------|
| 100% (full load) | 220–250 A |
| 75% | 175–200 A |
| 50% | 140–165 A |
| Start-up (in-rush, first 5 sec) | Up to 600 A (transient) |

Alarms:
- High current: YFJ3_AI > 280 A sustained (> 30 sec) → Investigate (mechanical binding, high flue gas density, VFD issue)
- High-High / Trip: YFJ3_AI > 310 A → IDF trip

If YFJ3_AI has been consistently tracking 10% above baseline trend, investigate: impeller fouling (ash buildup), increased system resistance (blocked ductwork), or VFD efficiency degradation.

---

## 6. VFD Inspection (Coordinate with Electrical Team)

- [ ] VFD cooling fans running (all units — typically 4–6 internal fans)
- [ ] VFD filter media cleaned (washable foam pads)
- [ ] VFD control board connection check — reseat any ribbon connectors
- [ ] VFD parameter backup completed (save to USB/DCS)
- [ ] VFD output current matches motor current meter (YFJ3_AI cross-check)

---

## 7. Post-Maintenance Motor Test

1. Remove LOTO, re-energize at MCC
2. Start IDF via DCS in manual at 15% speed
3. Monitor YFJ3_AI — should reach steady state within 30 seconds
4. Confirm current reading on local ammeter matches DCS YFJ3_AI ± 5%
5. Ramp to 100% over 5 minutes — confirm current tracks expected profile

**Acceptance criterion:** YFJ3_AI within normal range at each load step; no unusual motor sounds; motor body temperature rise < 40°C above ambient after 30 minutes at full speed.

---

## 8. Sign-Off

**Electrical work performed by:** ________________________  
**Date:** ____________  
**IR test result:** _______ MΩ (PI: _______)  
**Engineer approval:** ________________________
