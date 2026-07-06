---
doc_id: mnt_idf_bearing_inspection
doc_type: maintenance
equipment: [induced_draft_fan]
tags: [YFJ3_ZD1, YFJ3_ZD2, YFJ3_AI]
title: IDF Bearing Shell Inspection and Vibration Check
revision: 2.1
date: 2021-05-10
---

# Maintenance Procedure: IDF Bearing Shell Inspection and Vibration Check

**Document No.:** ZJP-MNT-003  
**Revision:** 2.1 | **Date:** 2021-05-10  
**Applicability:** Unit 1 Induced Draft Fan (YFJ3)  
**Maintenance Type:** Planned — Annual Outage  
**Estimated Duration:** 8 hours (2-person crew)

---

## 1. Scope

This procedure covers the annual bearing inspection for the Unit 1 Induced Draft Fan during planned outage. It includes: bearing removal, visual and dimensional inspection, lubrication system check, and reassembly with acceptance testing.

The IDF is the single most critical rotating machine in the plant. Bearing failure leads to immediate boiler trip and potential catastrophic damage. This procedure must not be deferred beyond the 12-month interval.

---

## 2. Prerequisites

### 2.1 Isolation Requirements
- [ ] IDF isolated per LOTO procedure ZJP-SAFE-001
  - Motor de-energized and locked out at MCC (lock #: ______)
  - VFD isolated at input breaker
  - Inlet and outlet dampers mechanically blocked open (for ventilation)
- [ ] Vibration transmitters YFJ3_ZD1 and YFJ3_ZD2 isolated from DCS (maintenance mode) to avoid spurious alarms during work
- [ ] Lubrication oil system shut down and cooled (oil temperature < 40°C before draining)

### 2.2 Tools and Materials Required
- Bearing puller (hydraulic, minimum 50-tonne capacity)
- Dial indicator and magnetic base
- Feeler gauges (0.02–2.0 mm)
- Torque wrench (0–500 Nm)
- Ultrasonic thickness gauge
- Vibration analyzer (portable, with route data for YFJ3_ZD1 and YFJ3_ZD2 trend)
- Replacement bearings (see ZJP-DS-012 for part numbers — have on-site before starting)
- ISO VG 100 turbine oil (20 L minimum)
- Coupling alignment tools (laser preferred)
- PPE: hearing protection, safety glasses, hard hat, steel-toe boots

---

## 3. Pre-Work Condition Verification

Before starting work, record the following from the last known DCS readings:
- Last YFJ3_ZD1 reading: _______ mm/s (date: _______)
- Last YFJ3_ZD2 reading: _______ mm/s (date: _______)
- Last YFJ3_AI (motor current): _______ A

If either vibration reading was > 3.5 mm/s before shutdown, flag this to the engineer — bearing replacement is mandatory regardless of inspection finding.

---

## 4. Bearing Removal

1. Remove coupling guard — inspect coupling for cracks, wear, or misalignment signs before disassembling
2. Disconnect coupling (drive end) — do not use heat; use hydraulic puller only
3. Drain oil from drive-end bearing housing via drain plug — collect in labeled waste oil container
4. Remove bearing housing cover (typically 24 × M20 bolts)
5. Photograph bearing position and orientation before removal (reference for reassembly)
6. Use hydraulic bearing puller to remove bearing from shaft — do not hammer
7. Clean shaft journal with fine emery cloth — record any scoring or fretting marks on inspection sheet
8. Repeat steps 3–7 for non-drive-end bearing

---

## 5. Bearing Inspection

For each bearing removed, record the following on the Inspection Record Form (ZJP-F-002):

### 5.1 Visual Inspection
- [ ] Raceways (inner and outer): no spalling, pitting, flaking, or fatigue cracks
- [ ] Rolling elements: no flat spots, etching, or visible wear
- [ ] Cage: intact, no cracks or deformation
- [ ] Retaining ring: not deformed, correctly seated in groove

### 5.2 Dimensional Check
- Radial clearance (before cleaning): _______ mm (specification: 0.15–0.35 mm for this bearing size)
- Shaft journal diameter: _______ mm (design: 240.000–240.030 mm)
- Bearing housing bore: _______ mm (design: 260.000–260.025 mm)

### 5.3 Acceptance Criteria
| Finding | Action |
|---------|--------|
| Spalling or pitting on raceway | Replace bearing mandatory |
| Radial clearance > 0.50 mm | Replace bearing mandatory |
| Cage cracks | Replace bearing mandatory |
| Surface etching (false brinelling) | Replace bearing mandatory |
| Minor polishing, no structural damage | May re-use at engineer's discretion |

---

## 6. Lubrication System Inspection

1. Drain and inspect oil from both housing sumps — record color, clarity, and any metallic particles:
   - Normal oil: amber, transparent, no metallic sheen
   - Abnormal: dark/black (oxidation), milky (water contamination), metallic glitter (bearing wear)
2. Flush bearing housings with clean flush oil
3. Inspect oil pump strainer — clean if partially blocked
4. Check oil cooler for fouling (measure water-side ΔP if possible)
5. Replace oil filter cartridge (always replace at annual inspection regardless of condition)
6. Oil reservoir: clean interior, check level gauge calibration

---

## 7. Reassembly

1. Install new/inspected bearings using hydraulic press or induction heater (heat to 100°C max for interference fit installation — do not use open flame)
2. Confirm correct bearing seating — zero gap between bearing inner race and shaft shoulder
3. Install bearing housing covers with new gaskets — torque to 150 Nm in cross pattern
4. Fill bearing housings with ISO VG 100 turbine oil to sight glass level
5. Reinstall coupling — confirm alignment within specification:
   - Parallel misalignment: < 0.05 mm
   - Angular misalignment: < 0.05 mm/100 mm
6. Reinstall coupling guard

---

## 8. Post-Maintenance Acceptance Test

1. Remove LOTO, notify control room of test start
2. Start IDF in local control at minimum speed (15% VFD) — 2-minute coast-up
3. Observe by ear and hand (not touch rotating parts) — no metallic sounds, no excessive heat after 10 minutes
4. Read vibration via portable analyzer at both YFJ3_ZD1 and YFJ3_ZD2 locations:
   - Acceptance criterion: < 2.5 mm/s at any speed up to full operating speed
5. Ramp to 50% speed — hold 10 minutes — record vibration and current
6. Ramp to full operating speed (100%) — hold 30 minutes — record:
   - YFJ3_ZD1: _______ mm/s
   - YFJ3_ZD2: _______ mm/s
   - YFJ3_AI: _______ A
   - Bearing housing temperature (IR gun): _______ °C (acceptance: < 65°C)
7. Confirm DCS readings match portable analyzer readings for both vibration points

**Acceptance criterion for return to service:** All vibration readings < 2.5 mm/s, bearing temperature < 65°C, no abnormal noise.

---

## 9. Sign-Off

**Work performed by:** ________________________  
**Date completed:** ____________  
**Inspection findings:** (attach ZJP-F-002 completed form)  
**Bearings replaced:** ☐ Yes (part numbers: ________________) / ☐ No  
**Return to service approved by:** ________________________ (Engineer/Supervisor)  
**Date returned to service:** ____________
