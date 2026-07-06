---
doc_id: safe_loto_induced_draft_fan
doc_type: safety
equipment: [induced_draft_fan]
tags: [YFJ3_AI, YFJ3_ZD1, YFJ3_ZD2]
title: LOTO Procedure — Induced Draft Fan (YFJ3)
revision: 2.0
date: 2021-08-01
---

# Lockout/Tagout Procedure: Induced Draft Fan (YFJ3)

**Document No.:** ZJP-SAFE-001  
**Equipment:** Unit 1 Induced Draft Fan (YFJ3)  
**Revision:** 2.0 | **Date:** 2021-08-01  
**Regulatory Basis:** GB/T 33579-2017 (Lockout/Tagout Safety Standard)

> **WARNING:** The IDF motor operates at 6,000 V. Only qualified high-voltage electricians may perform the electrical isolation steps. All other personnel must wait until electrical isolation is confirmed complete before approaching the IDF.

---

## 1. Energy Sources to be Controlled

| Energy Source | Type | Location | Isolation Device |
|--------------|------|----------|-----------------|
| IDF motor power | Electrical — 6 kV AC | 6 kV switchgear Panel 3, Breaker B-03 | Motorized circuit breaker — open and lock |
| VFD input supply | Electrical — 6 kV AC | VFD input isolator, IDF VFD room | Isolator switch — open and lock |
| VFD DC bus | Electrical — residual DC | VFD cabinet | 15-minute discharge wait mandatory — verify with meter |
| Instrument air (inlet damper actuator) | Pneumatic | Instrument air isolation valve, IDF deck | Quarter-turn valve — close and lock |
| Instrument air (outlet damper actuator) | Pneumatic | Instrument air isolation valve, IDF outlet | Quarter-turn valve — close and lock |
| Flue gas (inlet duct) | Thermal / process gas | Inlet damper | Damper mechanically blocked open for ventilation |
| Flue gas (outlet duct) | Thermal / process gas | Outlet damper | Damper mechanically blocked open for ventilation |

---

## 2. Pre-Isolation Confirmation

Before beginning LOTO:
- [ ] Confirm with control room that IDF has been stopped (IDF running status = OFF on DCS)
- [ ] Confirm YFJ3_ZD1 and YFJ3_ZD2 = 0 mm/s (fan stopped — confirm shaft is stationary)
- [ ] Confirm YFJ3_AI = 0 A (motor de-energized)
- [ ] Notify shift supervisor that LOTO is beginning — enter in isolation register

---

## 3. Isolation Sequence

**Step 1 — IDF Motor (HV Electrician required)**
1. Open 6 kV switchgear breaker B-03 (Panel 3) — confirm OPEN position indicator
2. Apply electrical lock to breaker with personal padlock (Color: RED)
3. Apply danger tag: "DANGER — DO NOT ENERGIZE — MAINTENANCE IN PROGRESS"
4. Open VFD input isolator — confirm OPEN
5. Apply lock to VFD isolator
6. Wait 15 minutes minimum for VFD DC bus to discharge
7. Verify VFD DC bus voltage with calibrated meter: must be < 50 V before proceeding
8. Sign and date isolation register — HV electrician signature required

**Step 2 — Pneumatic (Instrument Technician)**
1. Close instrument air isolation valve at inlet damper actuator — lock with padlock
2. Close instrument air isolation valve at outlet damper actuator — lock with padlock
3. Confirm dampers: actuators will fail to last position when air is removed; verify damper position is safe (open for ventilation is preferred)

**Step 3 — Mechanical (Mechanical Technician)**
1. Manually open inlet damper fully and install mechanical block (scaffold pipe through damper frame — prevents accidental closure)
2. Manually open outlet damper fully and install mechanical block
3. Confirm flue gas path is open for ventilation — allows cooling and prevents CO accumulation

---

## 4. Verification (Try-Out)

Before permitting any work on the IDF:
- [ ] Confirm motor de-energized by attempting DCS start command — motor must NOT start
- [ ] Confirm IDF shaft is stationary — touch shaft with fingertip (not hand — confirm by sight/feel that it is not moving)
- [ ] All locks in place — count locks: minimum 3 locks (1 electrical, 1 inlet air, 1 outlet air)
- [ ] Danger tags affixed at all isolation points

Work may now begin. Hand over to maintenance supervisor with signed isolation register.

---

## 5. Restoration After Work

After work is complete:
1. Maintenance supervisor confirms all work is complete, all personnel clear, all tools removed
2. Remove mechanical blocks from dampers
3. Remove all padlocks in reverse order of installation
4. Remove danger tags
5. HV electrician closes VFD isolator and 6 kV breaker
6. Sign off isolation register — return to shift supervisor
7. Notify control room: IDF is available for restart
8. Perform post-maintenance acceptance test (ZJP-MNT-003, Section 8)

---

## 6. Revision History

| Rev | Date | Change |
|-----|------|--------|
| 1.0 | 2019-03-01 | Initial issue |
| 2.0 | 2021-08-01 | Added VFD DC discharge wait time (15 min) after near-miss during 2020 maintenance |
