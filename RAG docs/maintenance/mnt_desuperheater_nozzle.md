---
doc_id: mnt_desuperheater_nozzle
doc_type: maintenance
equipment: [primary_desuperheater]
tags: [TV_8329ZC, YJJWSLL]
title: Desuperheater Spray Nozzle Inspection and Cleaning
revision: 1.2
date: 2021-06-15
---

# Maintenance Procedure: Desuperheater Spray Nozzle Inspection and Cleaning

**Document No.:** ZJP-MNT-012  
**Revision:** 1.2 | **Date:** 2021-06-15  
**Applicability:** Primary Desuperheater (DESUP-1)  
**Maintenance Type:** Annual Outage  
**Estimated Duration:** 4 hours

---

## 1. Scope

The desuperheater spray nozzle injects fine water droplets into the steam stream. A partially blocked nozzle creates uneven spray distribution, larger droplets that may not evaporate before the HTSH inlet, and erratic TV_8329ZC behavior. This inspection cleans the nozzle and checks the downstream pipe for water deposition.

---

## 2. Isolation

- [ ] Steam side of desuperheater depressurized and drained
- [ ] Spray water supply isolation valve closed and locked (lock on TV_8329ZC upstream isolation)
- [ ] Confirm no pressure on YJJWSLL (flowmeter should read zero)
- [ ] Steam pipe cooled to < 60°C before opening

---

## 3. Nozzle Removal and Inspection

1. Unbolt nozzle body from steam pipe flange — typically 8 × M16 bolts
2. Withdraw nozzle assembly — wrap in clean cloth to protect nozzle tip
3. Flush nozzle from water inlet end with clean water — observe spray pattern:
   - **Correct:** Full-cone, uniform droplet distribution
   - **Blocked:** Non-uniform, partial cone, or no flow from some orifices
4. Inspect nozzle orifice plate under magnification (5–10×):
   - [ ] Orifices: not enlarged (erosion) or plugged (scale)
   - [ ] Nozzle tip: no cracking or deformation
   - [ ] O-ring / gasket contact face: smooth, no pitting
5. If blocked: soak in 10% citric acid solution for 30 minutes, then flush — do not use wire to clear orifices (causes enlargement)
6. Measure orifice diameter with calibrated pin gauge:
   - Design orifice diameter: 3.2 mm each (12 orifices)
   - Replace nozzle if any orifice > 3.8 mm (25% enlargement from erosion)

---

## 4. Downstream Pipe Inspection

The 5 m pipe section downstream of the nozzle is critical — water droplets that fail to evaporate impinge on this pipe and the HTSH inlet header.

1. Open inspection port on downstream pipe (300 mm from nozzle exit)
2. Inspect inner surface with endoscope:
   - [ ] No pitting or erosion craters (water droplet impingement)
   - [ ] No scale deposits > 1 mm thick (indicates chronic incomplete evaporation)
3. If heavy impingement marks found: increase downstream nozzle spray distance review with process engineer — operating with smaller water flow per injection may be needed

---

## 5. TV_8329ZC Valve Inspection

1. With valve isolated, manually stroke valve from 0–100% (using hand-operated test facility or portable air supply):
   - Confirm smooth travel — no sticking or hysteresis > 3%
   - Confirm closed position: zero leakage through valve when YJJWSLL = 0
2. Actuator diaphragm: no visible cracks or deformation
3. Positioner: zero and span calibration check per calibration procedure
4. Confirm fail-safe position: spring forces valve closed on loss of instrument air

---

## 6. YJJWSLL Flow Meter Verification

1. Remove vortex element for inspection:
   - Bluff body (vortex shedder): no erosion, no scale buildup
   - Meter body inner surface: clean
2. Zero check: flow meter reads 0.0 t/h with valve closed
3. If available, compare reading to plant water balance calculation at known flow rate

---

## 7. Reassembly

1. Install new gaskets on nozzle flange (spiral-wound, PN 16 MPa rated)
2. Reinstall nozzle — torque bolts to 180 Nm in cross pattern
3. Pressure test: apply 1 MPa water pressure to spray water circuit — confirm zero leakage before steam side closed

---

## 8. Sign-Off

**Performed by:** ________________________  
**Date:** ____________  
**Nozzle replaced:** ☐ Yes (PN: ________________) / ☐ No (cleaned only)  
**Impingement found on downstream pipe:** ☐ Yes (reported to engineer) / ☐ No  
**TV_8329ZC calibrated:** ☐ Yes  
**YJJWSLL verified:** ☐ Yes  
**Approval:** ________________________
