---
doc_id: mnt_feedwater_pump_check
doc_type: maintenance
equipment: [economizer, steam_drum]
tags: [PTCA_8322A]
title: Feedwater System Pre-Startup Check
revision: 1.1
date: 2021-06-01
---

# Maintenance Procedure: Feedwater System Pre-Startup Check

**Document No.:** ZJP-MNT-014  
**Revision:** 1.1 | **Date:** 2021-06-01  
**Maintenance Type:** Annual Outage and Before Every Cold Start  
**Estimated Duration:** 3 hours

---

## 1. Scope

Confirms the feedwater system — deaerator, feedwater pumps, economizer inlet line, and drum fill connection — is ready for boiler startup. A feedwater system failure during startup is a leading cause of drum low-level trips.

---

## 2. Deaerator Check

- [ ] Deaerator water level: ≥ 60% (sufficient volume for startup and initial ramp)
- [ ] Deaerator operating pressure: 0.12 MPa (correct temperature for oxygen removal)
- [ ] Deaerator vent valve: partly open during startup to release oxygen
- [ ] Water chemistry: dissolved oxygen < 7 ppb, conductivity within specification (see ZJP-CHEM-001)

---

## 3. Feedwater Pump Check

| Item | Acceptable | Measured |
|------|-----------|---------|
| Pump A — bearing temperature | < 70°C | _______ °C |
| Pump A — vibration (local) | < 3.0 mm/s | _______ mm/s |
| Pump A — mechanical seal: no visible leakage | No drip | ☐ OK |
| Pump A — suction pressure | > 0.08 MPa | _______ MPa |
| Pump B (standby) — same checks | — | ☐ OK |

- [ ] Standby pump on auto-start interlock confirmed (test auto-start at minimum flow)
- [ ] Recirculation valve: opens automatically below minimum flow (15 t/h) — confirm function

---

## 4. Feedwater Control Valve

- [ ] FCV position feedback matches DCS display
- [ ] Full travel test (0–100%): no sticking, smooth travel
- [ ] Fail-open confirmed (spring-to-open — fail safe for drum level protection)

---

## 5. Economizer Inlet Line

- [ ] Isolation valve: confirmed OPEN
- [ ] Check valve: free to open in correct flow direction
- [ ] Air vent on economizer: confirm will be opened at start of fill

---

## 6. Drum Level Instruments

- [ ] Both drum level transmitters reading same value (± 10 mm is acceptable)
- [ ] Drum level gauge glass: clean glass, water/steam interface visible and stable
- [ ] High-level and low-level alarm lights tested — confirm audible alarm

---

## 7. Sign-Off

**Performed by:** ________________________  
**Date:** ____________  
**Both feedwater pumps confirmed ready:** ☐ Yes  
**Drum level instruments confirmed:** ☐ Yes  
**Approval to proceed with startup:** ________________________
